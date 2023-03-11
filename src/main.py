from math import log2 as log

import numpy as np

from dcs import DistinctCountSketch, int2ip, ip2int
from ddos_dataset import BalancedDataset


def main():
    # user defined parameters
    delta = 0.05
    epsilon = 1 / 3
    k = 3
    print(f"delta={delta}, epsilon={epsilon}, k={k}")

    # load the stream
    balanced = BalancedDataset()
    params, freqs = balanced.calc_params(delta, epsilon, k)

    """
    df = balanced.df

    df['pair'] = df[balanced.cols['src_ip']].astype(
        str) + '-' + df[balanced.cols['dest_ip']].astype(str)
    U = len(df['pair'].unique())
    
    df = df.groupby([balanced.cols["dest_ip"]]).sum()
    df['diff'] = df[balanced.cols['syn']] - df[balanced.cols['ack']]
    # df = df[df['diff'] > 0]
    df = df.sort_values(by='diff', ascending=False)
    print(df)

    print(df[df.index == ip2int("44.31.65.33")])

    return
    """
    
    # init the sketch
    sketch = DistinctCountSketch()
    # sketch = DistinctCountSketch(**params)

    # sketch the stream
    sketch.record_stream(balanced.df, balanced.get_row)
    for b, s in enumerate(sketch.h_recorder):
        print(f"{b} -> {len(s)} pairs")

    for t in [None, 50, 100, 200]:
        print(f"threshold={t}")
        
        # query the sketch
        top_k_ddos_victims = sketch.top_k(epsilon, k, threshold=t)

        # analyze results
        print(freqs.index)
        for victim in top_k_ddos_victims:
            ip, est_f = victim
            int_ip = ip2int(ip)
            print(int_ip)

            # get real frequency
            idx = np.argwhere(freqs.index == int_ip)
            real_f = freqs.values[idx]

            print(f"ip={ip}, idx={idx}, f={real_f}, estimated={est_f}")


if __name__ == '__main__':
    main()
