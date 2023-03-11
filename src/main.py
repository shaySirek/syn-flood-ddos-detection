import numpy as np

from dcs import DistinctCountSketch, ip2int
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
    dataset = BalancedDataset()
    sources_per_dest = dataset.naive_syn_flood_detection()
    sources_per_dest.to_csv("balanced_ddos_results.csv")
    """

    # user defined parameters
    delta = 0.05
    epsilon = 1 / 3
    k = 3

    # calculate sketch params - driven by the data
    sketch_params = dataset.calc_params(delta, epsilon, k)

    # init the sketch
    sketch = DistinctCountSketch()
    # sketch = DistinctCountSketch(**sketch_params)

    # sketch the stream
    sketch.record_stream(dataset.df, dataset.get_row)
    
    # print First-level buckets
    print(100*'*')
    print("First-level buckets:")
    for b, s in enumerate(sketch.h_recorder):
        print(f"{b} -> {len(s)} pairs")
    
    print(100*'*')
    print("Estimations:")

    # try with different thresholds
    for threshold in [None, 50, 100, 200]:
        # query the sketch
        top_k_ddos_victims = sketch.top_k(epsilon, k, threshold=threshold)

        # analyze results
        for victim in top_k_ddos_victims:
            ip, est_f = victim
            int_ip = ip2int(ip)

            # get real frequency
            idx = np.argwhere(sources_per_dest.index == int_ip)
            real_f = sources_per_dest.values[idx]

            print(f"ip={ip}, idx={idx}, f={real_f}, estimated={est_f}")


if __name__ == '__main__':
    main()
