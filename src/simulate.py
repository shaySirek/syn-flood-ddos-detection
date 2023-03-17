import random

import pandas as pd
import numpy as np

from dcs import int2ip, ip2int
from settings import *


def generate_ips_in_range(from_ip, to_ip, n_ips):
    from_int = ip2int(from_ip)
    to_int = ip2int(to_ip)

    generated = set()
    for _ in range(n_ips):
        rand_ip_int = random.randint(from_int, to_int)
        rand_ip = int2ip(rand_ip_int)
        generated.add(rand_ip)

    return list(generated)


def simulate_attack(our, outside, our_attacked, outside_attackers, n_exchanges, attacker_percent, attacked_probs):
    from_ip_arr = []
    to_ip_arr = []
    syn_arr = []
    ack_arr = []

    for _ in range(n_exchanges):
        if (random.random() < attacker_percent):  # Attack -> only SYN
            from_ip_arr.append(random.choice(outside_attackers))
            to_ip_arr.append(random.choices(our_attacked, weights=attacked_probs)[0])
            syn_arr.append(1)
            ack_arr.append(0)
        else:  # SYN, ACK
            from_ip = random.choice(outside)
            to_ip = random.choice(our)
            from_ip_arr.append(from_ip)
            to_ip_arr.append(to_ip)
            syn_arr.append(1)
            ack_arr.append(0)

            from_ip_arr.append(from_ip)
            to_ip_arr.append(to_ip)
            syn_arr.append(0)
            ack_arr.append(1)

    d = {'src_ip': from_ip_arr, 'dst_ip': to_ip_arr,
         'syn_flg': syn_arr, 'ack_flg': ack_arr}
    df = pd.DataFrame(data=d)

    return df


def main():
    our_subnet = ('44.160.0.1', '44.200.10.10')
    outside_subnet = ('45.0.0.0', '200.0.0.0')

    our = generate_ips_in_range(*our_subnet, n_ips_to_generate_our)
    outside = generate_ips_in_range(*outside_subnet, n_ips_to_generate_outside)

    our_attacked = random.choices(our, k=n_attacked)
    outside_attackers = random.choices(outside, k=n_attackers)

    for a in zipf_a:
        print(f"zipf({a}, {n_attacked})")
        attacked_probs = np.random.zipf(a, n_attacked)
        attacked_probs = attacked_probs / sum(attacked_probs)
        print(f"attacked_probs={sorted(attacked_probs, reverse=True)}")

        print(f"Simulating DDoS attack...")
        df = simulate_attack(our, outside, our_attacked, outside_attackers,
                             n_exchanges, attacks_percent, attacked_probs)
        df.to_csv(dataset_name.format(a))


if __name__ == '__main__':
    main()
