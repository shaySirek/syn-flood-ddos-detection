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

## Ideas

### Change the threshold on d_sample length
As the threshold is lower, the sensitivity is higher.

### Bit Counter threshold
neglect smaller counts

### Timeliness
naive: Reset the sketch every x minutes.
> But we can reset the sketch in the middle of syn-flood ddos attack.

Let's assume that syn-flood ddos attack occurs in 30 seconds interval.
Therefore, we can maintain two intances of the data structure:
- Reset every 1 minute.
- Reset every 1 minute, offset by 30 seconds.

### First-level bucket space complexity optimization

### Discuss original parameters
- r=128 ?
- s depends on f_(v_k) which we want to estimate in this algorithm

### Time complexity optimization

### Collisions

Example:
dest_ip 1 has 5 src_ip in bucket 9
Bucket 9 has 50% collisions = collision_number / (collision_number + ip_number)
Staticically, dest_ip 1 has 5 * (1/0.5) = 10

### Calculate Source of Truth using Naive approach