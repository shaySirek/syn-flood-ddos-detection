from dcs import DistinctCountSketch
from ddos_dataset import BalancedDataset, ip2int


def main():
    balanced = BalancedDataset()    
    sketch = DistinctCountSketch(balanced.get_row)
    
    # sketch the stream
    balanced.df.apply(sketch.record_row, axis=1)
    
    # query the sketch
    top_10_ddos_victims = sketch.top_k(0.05, 10)

    print(top_10_ddos_victims)


if __name__ == '__main__':
    main()
