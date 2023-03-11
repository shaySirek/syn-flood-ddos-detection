# TCP SYN Flood - DDoS attack detection

TCP SYN Flood DDoS attack detection with `Distinct-Count Sketch`.

### Paper
`Streaming Algorithms for Robust, Real-Time Detection of DDoS Attacks`

## Datasets
### General DDoS datasets
Download these datasets from [kaggle](https://www.kaggle.com/datasets/devendra416/ddos-datasets):
- Balanced Dataset (final_dataset.csv)
- Imbalanced Dataset (unbalaced_20_80_dataset.csv)

```shell
head -n 1 datasets/ddos_balanced/final_dataset.csv | cut -d ',' -f 3,5,8,52,55
```

### Synthetic Data
This [script](./src/simulate.py) generates:

```csv
src_ip,dst_ip,syn_flg,ack_flg
106.31.159.63,44.197.141.175,1,0
106.31.159.63,44.197.141.175,0,1
78.247.113.32,44.165.144.217,1,0
78.247.113.32,44.165.144.217,0,1
...
```

## Baseline
Calculate Source of Truth using Naive approach: [`naive_syn_flood_detection`](./src/ddos_dataset/dataset.py).

## Ideas
Our ideas for improvements.

### Thresholds
- Change the threshold on `d_sample` length: as the threshold is lower, the sensitivity is higher.
- `Bit Counter threshold`: neglect smaller counts.

### Space and Time Complexity
- First-level bucket `space complexity` optimization.
- Second-level bucket `space complexity` optimization.
- `Time complexity` optimization.

### Discuss Sketch Parameters
- `r=128`.
- `s` depends on `f_(v_k)`, which we want to estimate in this algorithm.

#### Timeliness
naive: Reset the sketch every x minutes.
> But we can reset the sketch in the middle of syn-flood ddos attack.

Let's assume that syn-flood ddos attack occurs in 30 seconds interval.
Therefore, we can maintain two intances of the data structure:
- Reset every 1 minute.
- Reset every 1 minute, offset by 30 seconds.

### Collisions density

Example:

- `dest_ip 1` has 5 `src_ip`s in `bucket` 9.
- `Bucket` 9 has 50% `collisions = n_collision_in_all_bucket / (n_collision_in_all_bucket + n_src_ip_in_all_bucket)`.
- So, staticically, `dest_ip 1` has `5 * (1/0.5) = 10` `src_ip`s in this bucket.

### Reduntant collision detection