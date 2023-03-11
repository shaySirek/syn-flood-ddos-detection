import os

from .dataset import Dataset


class SynthDataset(Dataset):
    def __init__(self, root_dir: str = 'datasets', load: bool = True):
        super(SynthDataset, self).__init__(
            root_dir,
            path=os.path.join(root_dir, 'syn_flood_dataset.csv'),
            cols={
                'src_ip': "src_ip",
                'dest_ip': "dst_ip",
                'syn': "syn_flg",
                'ack': "ack_flg",
            },
            load=load)
