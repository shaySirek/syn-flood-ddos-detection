import pandas as pd
import numpy as np

from dcs import DistinctCountSketch, ip2int, int2ip
from settings import *
from dataset import Dataset
from analyze import analyze


def main():
    for a in zipf_a:
        # load the stream
        dataset = Dataset(dataset_name.format(a), COLS)
        sources_per_dest: pd.Series = dataset.naive_syn_flood_detection()
        sources_per_dest.apply(int2ip).to_csv(naive_result.format(a))

        # calculate sketch params - driven by the data
        sketch_params = dataset.calc_params(delta, epsilon, k)
        print(sketch_params)

        # init the sketch
        sketch = DistinctCountSketch()
        # sketch = DistinctCountSketch(**sketch_params)

        # sketch the stream
        sketch.record_stream(dataset.df, dataset.get_row)

        print(100*'*')
        print("Estimations:")

        # try with different thresholds
        for threshold in [None, 50, 100, 200]:
            for fix_collision in [False, True]:
                # query the sketch
                top_k_ddos_victims = sketch.top_k(epsilon, k, threshold=threshold, fix_collision=fix_collision)
                result_file_name = estimation_result.format(a, threshold or 'default', fix_collision)
                analyze(top_k_ddos_victims, sources_per_dest, result_file_name)


if __name__ == '__main__':
    main()
