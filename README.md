# TCP SYN Flood - DDoS attack detection

TCP SYN Flood DDoS attack detection with `Distinct-Count Sketch`.

### Paper
`Streaming Algorithms for Robust, Real-Time Detection of DDoS Attacks`

## Datasets
Download these datasets from [kaggle](https://www.kaggle.com/datasets/devendra416/ddos-datasets):
- Balanced Dataset (final_dataset.csv)
- Imbalanced Dataset (unbalaced_20_80_dataset.csv)

```shell
head -n 1 datasets/ddos_balanced/final_dataset.csv | cut -d ',' -f 3,5,8,52,55
```
