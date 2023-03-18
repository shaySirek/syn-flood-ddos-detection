from collections import Counter
from typing import Callable, Any

import numpy as np
import pandas as pd

from .utils import (
    int2ip,
    bit_array,
    bit_array_to_pair,
    LOG_M,
    BucketStatus
)
from .hash import h, g


class DistinctCountSketch:

    def __init__(self, log_m: int = LOG_M, r: int = 3, s: int = 128, bit_counter_threshold: int = 0):
        """
            Params:
                log_m: number of bits in IP address ->
                        number of buckets in first-level hash
                r: number of second-level hash tables
                s: number of buckets in second-level hash
                bit_counter_threshold: threshold for the bit counter
        """
        print(100*'*')
        print("init DistinctCountSketch")
        self.log_m = log_m
        self.first_lvl_hash_buckets = 2 * log_m
        self.r = r
        self.s = s
        self.n_bit_cnt = 2 * log_m + 1
        self.bit_counter_threshold = bit_counter_threshold

        self.X = [None for _ in range(self.first_lvl_hash_buckets)]
        self.h_recorder = [set() for _ in range(self.first_lvl_hash_buckets)]

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
        b = h(src_ip, dest_ip)

        # init first-level bucket
        if self.X[b] is None:
            self.X[b] = [[None for _ in range(self.s)] for _ in range(self.r)]

        self.h_recorder[b].add((src_ip, dest_ip))

        for j in range(self.r):
            # second-level bucket
            k = g(j, src_ip, dest_ip)
            # init second-level bucket
            if self.X[b][j][k] is None:
                self.X[b][j][k] = np.zeros((self.n_bit_cnt), dtype=int)
            self.X[b][j][k] += flag * bit_array(src_ip, dest_ip)

    def record_stream(self, stream: pd.DataFrame, get_row: Callable[[Any], tuple[int, int, int] | None]):
        def record_row(row):
            # load params from df row
            row_record = get_row(row)

            if row_record is not None:
                src_ip, dest_ip, flag = row_record
                self.record(src_ip, dest_ip, flag)

        print(100*'*')
        print("record_stream")
        stream.apply(record_row, axis=1)
        
        # print First-level buckets
        print(100*'*')
        print("First-level buckets:")
        for b, s in enumerate(self.h_recorder):
            print(f"{b} -> {len(s)} pairs")
        
    def top_k(self, epsilon: float, k: int, threshold: float | None = None, fix_collision: bool = False):
        if threshold is None:
            threshold = (1 + epsilon) * (self.s / 16)
        
        print(100*'*')
        print(f"top_k with threshold={threshold}")
        
        b = self.first_lvl_hash_buckets - 1
        d_sample: set[tuple[int, int]] = set()
        cnt = Counter()

        while (b >= 0 and len(d_sample) < threshold):
            if self.X[b] is not None:  # the bucket is not empty
                pairs, uncollisioned_rate = self.get_d_sample(b)
                print(f"b={b}, uncollisioned_rate={uncollisioned_rate}")
                
                # count sources for each destination in current first bucket b
                b_cnt = Counter()
                for _, v in pairs:
                    b_cnt[v] += 1
                
                # divide by the collision rate in this bucket if the option is enabled
                if fix_collision:
                    for v in cnt.keys():
                        b_cnt[v] /= uncollisioned_rate
                
                # sum up
                cnt = cnt + b_cnt
                d_sample.update(pairs)
            
            b -= 1

        # d_sample = distinct sample of source-dest (u, v) pairs

        print(100*"-")
        distinct_dests = len(cnt)
        print(f"exit with b={b}, {distinct_dests} distinct destinations")
        print(f"f: {[(int2ip(v), f) for v, f in cnt.most_common(distinct_dests)]}")
        print(100*"-")

        return [(int2ip(v), (2**b) * f) for v, f in cnt.most_common(k)]

    def get_d_sample(self, b: int) -> tuple[set[tuple[int, int]], float]:
        ds = set()
        collisions = 0
        
        for j in range(self.r):
            for k in range(self.s):
                if self.X[b][j][k] is not None:  # the bucket is not empty
                    status, pair = self.return_singleton(b, j, k)
                    if status == BucketStatus.PAIR:
                        ds.add(pair)
                    elif status == BucketStatus.COLLISION:
                        collisions += 1

        uncollisioned_rate = 1.
        denom = collisions + len(ds)
        if denom > 0:
            uncollisioned_rate = len(ds) / denom
            
        return ds, uncollisioned_rate

    def return_singleton(self, b: int, j: int, k: int) -> tuple[BucketStatus, tuple[int, int] | None]:
        return bit_array_to_pair(self.X[b][j][k], self.bit_counter_threshold)
