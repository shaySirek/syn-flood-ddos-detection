from math import log2 as log

import pandas as pd

from dcs import ip2int


class Dataset:
    def __init__(self, path: str, cols: dict[str, str], load: bool = True):
        self.path = path
        self.cols = cols

        if load:
            self.load()

    def load(self):
        print(100*'*')
        print(f"Load {self.path}...")
        df = pd.read_csv(self.path, usecols=list(
            self.cols.values()))
        
        df[self.cols['src_ip']] = df[self.cols['src_ip']].apply(ip2int)
        df[self.cols['dest_ip']] = df[self.cols['dest_ip']].apply(ip2int)

        self.df = df

    def get_row(self, row) -> tuple[int, int, int] | None:
        src_ip = row[self.cols['src_ip']]
        dest_ip = row[self.cols['dest_ip']]
        syn_flag = row[self.cols['syn']]
        ack_flag = row[self.cols['ack']]

        if syn_flag == 1:  # SYN
            return src_ip, dest_ip, 1
        elif ack_flag == 1:  # ACK
            return src_ip, dest_ip, -1

        # NO SYN, NO ACK -> not relevant
        return None

    def calc_params(self, delta: float, epsilon: float, k: int) -> dict:
        print(100*'*')
        print(f"delta={delta}, epsilon={epsilon}, k={k}")
        print(f"calc_params...")
        
        n = len(self.df)
        freqs = self.df.groupby([self.cols['dest_ip']])[
            self.cols['src_ip']].unique().map(len).sort_values(ascending=False)
        U = freqs.sum()
        f_k = freqs.values[k - 1]
        
        pairs = self.df[self.cols['src_ip']] + self.df[self.cols['dest_ip']]

        # log(m) = 32
        s = round((U * log((n + 32) / delta)) / (f_k * (epsilon**2)))
        r = round(log(n / delta))
        
        print(100*'*')
        print(f"f_1...k=f_1...{k}={freqs.values[:k]}")
        print(f"n={n}, U={U}, f_k=f_{k}={f_k}")
        print(f"skew={pairs.skew()}")
        print(f"r={r}, s={s}")

        return dict(r=r, s=s)

    def naive_syn_flood_detection(self) -> pd.Series:
        print(100*'*')
        print(f"naive_syn_flood_detection...")
        df = self.df.groupby([self.cols['src_ip'], self.cols['dest_ip']]).sum()
        df['diff'] = df[self.cols['syn']] - df[self.cols['ack']]
        df = df[df['diff'] > 0]
        sources_per_dest = df.groupby(self.cols['dest_ip'])[
            'diff'].count().rename('sources_per_dest')
        sources_per_dest = sources_per_dest.sort_values(ascending=False)

        return sources_per_dest
