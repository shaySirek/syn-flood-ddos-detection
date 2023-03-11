from collections import defaultdict, Counter
from typing import Callable, Any
import json

import numpy as np
import pandas as pd

from .utils import (
    int2ip,
    bit_array,
    bit_array_to_pair,
    LOG_M,
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
        # self.collisions = defaultdict(
        #     lambda: defaultdict(lambda: defaultdict(set)))

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

        # init first-level bucket
        if self.X[first_lvl_idx] is None:
            self.X[first_lvl_idx] = np.zeros(
                (self.r, self.s, self.n_bit_cnt), dtype=int)

        self.h_recorder[first_lvl_idx].add((src_ip, dest_ip))

        for j in range(self.r):
            # second-level bucket
            second_lvl_idx = g(j, src_ip, dest_ip)

            # self.collisions[str(first_lvl_idx)][str(j)][str(
            #     second_lvl_idx)].add((src_ip, dest_ip))

            self.X[first_lvl_idx][j, second_lvl_idx] += flag * \
                bit_array(src_ip, dest_ip)

        # with open('collisions.json', 'wt') as f:
        #     ser_col = {k: [f"{int2ip(x[0])} -> {int2ip(x[1])}" for x in v]
        #                for k, v in self.collisions.items()}
        #     json.dump(ser_col, f)

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

    def top_k(self, epsilon: float, k: int, threshold: float | None = None):
        print(100*'*')
        print(f"top_k with threshold={threshold}")
        
        b = self.first_lvl_hash_buckets - 1
        d_sample: set[tuple[int, int]] = set()

        if threshold is None:
            threshold = (1 + epsilon) * (self.s / 16)

        while (b >= 0 and len(d_sample) < threshold):
            if self.X[b] is not None:  # the bucket is not empty
                d_sample.update(self.get_d_sample(b))
            b -= 1

        print(f"b={b}")

        # d_sample = distinct sample of source-dest (u, v) pairs
        print(100*"-")
        print("d_sample")
        print(d_sample)

        cnt = Counter()
        for _, v in d_sample:
            cnt[v] += 1

        print(100*"-")
        print("cnt")
        print(cnt)

        return [(int2ip(v), (2**b) * f) for v, f in cnt.most_common(k)]

    def get_d_sample(self, b: int) -> set[tuple[int, int]]:
        ds = set()

        for j in range(self.r):
            for k in range(self.s):
                pair = self.return_singleton(b, j, k)
                if pair is not None:
                    ds.add(pair)

        return ds

    def return_singleton(self, b: int, j: int, k: int) -> tuple[int, int] | None:
        return bit_array_to_pair(self.X[b][j, k], self.bit_counter_threshold)
