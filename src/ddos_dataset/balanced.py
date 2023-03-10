import os

from .dataset import Dataset


class BalancedDataset(Dataset):
    def __init__(self, root_dir: str = 'datasets', load: bool = True):
        super(BalancedDataset, self).__init__(
            root_dir,
            path=os.path.join(root_dir, 'ddos_balanced', 'final_dataset.csv'),
            cols={
                'src_ip': "Src IP",
                'dest_ip': "Dst IP",
                'syn': "SYN Flag Cnt",
                'ack': "ACK Flag Cnt",
            },
            load=load)
