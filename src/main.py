import numpy as np

from dcs import DistinctCountSketch, int2ip, ip2int
from ddos_dataset import (
    BalancedDataset,
    SynthDataset,
)


def main():
    # load the stream
    dataset = SynthDataset()
    sources_per_dest = dataset.naive_syn_flood_detection()
    sources_per_dest.to_csv("synth_ddos_results.csv")
    
    """
    dataset = BOUN_DDoS_Dataset()
    sources_per_dest = dataset.naive_syn_flood_detection()
    sources_per_dest.to_csv("boun_ddos_results.csv")
    """
    
    """
    dataset = BalancedDataset()
    sources_per_dest = dataset.naive_syn_flood_detection()
    sources_per_dest.to_csv("balanced_ddos_results.csv")
    """
   
    # user defined parameters
    delta = 0.05
    epsilon = 1 / 3
    k = 3
    print(f"delta={delta}, epsilon={epsilon}, k={k}")

    params, freqs = dataset.calc_params(delta, epsilon, k)
    
    # init the sketch
    sketch = DistinctCountSketch()
    # sketch = DistinctCountSketch(**params)

    # sketch the stream
    sketch.record_stream(dataset.df, dataset.get_row)
    for b, s in enumerate(sketch.h_recorder):
        print(f"{b} -> {len(s)} pairs")

    for t in [None, 50, 100, 200]:
        print(f"threshold={t}")
        
        # query the sketch
        top_k_ddos_victims = sketch.top_k(epsilon, k, threshold=t)

        # analyze results
        for victim in top_k_ddos_victims:
            ip, est_f = victim
            int_ip = ip2int(ip)

            # get real frequency
            idx = np.argwhere(freqs.index == int_ip)
            real_f = freqs.values[idx]

            print(f"ip={ip}, idx={idx}, f={real_f}, estimated={est_f}")
            
        print(100*'*')


if __name__ == '__main__':
    main()
