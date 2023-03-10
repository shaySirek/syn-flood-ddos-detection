import ipaddress

import pandas as pd


def ip2int(ip): return int(ipaddress.IPv4Address(ip))


class Dataset:
    def __init__(self, root_dir: str, path: str, cols: dict[str, str], load: bool):
        self.root_dir = root_dir
        self.path = path
        self.cols = cols
        
        if load:
            self.load()

    def load(self):
        df = pd.read_csv(self.path, usecols=list(self.cols.values()))

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
