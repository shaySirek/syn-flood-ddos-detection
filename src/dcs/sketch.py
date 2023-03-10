from collections import defaultdict, Counter
from typing import Callable, Any

import numpy as np

from .utils import (
    bit_array,
    int2ip,
    unpair,
    LOG_M
)
from .hash import h, g


class DistinctCountSketch:

    def __init__(self, get_row: Callable[[Any], tuple[int, int, int] | None],
                 log_m: int = LOG_M, r: int = 3, s: int = 128):
        """
            Params:
                log_m: number of bits in IP address ->
                        number of buckets in first-level hash
                r: number of second-level hash tables
                s: number of buckets in second-level hash
        """
        self.log_m = log_m
        self.first_lvl_hash_buckets = 2 * log_m
        self.r = r
        self.s = s
        self.n_bit_cnt = 2 * log_m + 1

        self.X = np.zeros((self.first_lvl_hash_buckets,
                           self.r,
                           self.s,
                           self.n_bit_cnt), dtype=int)

        self.get_row = get_row

    def record(self, src_ip: int, dest_ip: int, flag: int):
        """Record incoming (src_ip, dest_ip) pair, with TCP flag of SYN/ACK
            Params:
                src_ip: source IP
                dest_ip: destination IP
                flag: TCP flag
                    1 for SYN,
                    -1 for ACK
        """
        # first-level bucket
        first_lvl_idx = h(src_ip, dest_ip)
        # np.arange(self.r), src, dest -> apply g

        for j in range(self.r):
            # second-level bucket
            second_lvl_idx = g(j, src_ip, dest_ip)
            self.X[first_lvl_idx, j, second_lvl_idx] += flag * \
                bit_array(src_ip, dest_ip)
                
    def record_row(self, row):
        # load params from df row
        row_record = self.get_row(row)
        
        if row_record is not None:
            src_ip, dest_ip, flag = row_record
            self.record(src_ip, dest_ip, flag)            

    def top_k(self, epsilon: float, k: int):
        b = self.first_lvl_hash_buckets - 1
        d_sample = []
        threshold = (1 + epsilon) * (self.s / 16)

        while (b >= 0 and len(d_sample) < threshold):
            d_sample.extend(self.get_d_sample(b))
            b -= 1

        # d_sample = distinct sample of source-dest (u, v) pairs

        vu = defaultdict(set)
        for u, v in d_sample:
            vu[v].add(u)

        cnt = Counter()
        for v in vu.keys():
            cnt[v] = len(vu[v])

        return [(int2ip(v), (2**(b+1)) * f) for v, f in cnt.most_common(k)]
        
    def get_d_sample(self, b: int) -> list[tuple[int, int]]:
        ds = []

        for j in range(self.r):
            for k in range(self.s):
                pair = self.return_singleton(b, j, k)
                if pair is not None:
                    ds.append(pair)

        return ds

    def return_singleton(self, b: int, j: int, k: int) -> tuple[int, int] | None:
        if self.X[b, j, k, 0] == 0:
            return None

        src_dest_pair = 0

        for l in range(1, self.n_bit_cnt):
            if self.X[b, j, k, l] == 1:  # set bit l of (u,v) pair
                src_dest_pair = src_dest_pair | (1 << (l-1))
            elif self.X[b, j, k, l] > 1:  # collision >=2 pairs in the bucket
                return None

        return unpair(src_dest_pair)
