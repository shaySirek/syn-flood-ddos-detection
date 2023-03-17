# shared
zipf_a = [1.25, 1.5, 2.0]
dataset_name = 'datasets/zipf_{}_syn_flood_dataset.csv'

# simulate.py
our_subnet = ('44.160.0.1', '44.200.10.10')
n_ips_to_generate_our = 1000
outside_subnet = ('45.0.0.0', '200.0.0.0')
n_ips_to_generate_outside = 100000
n_attacked = 50
n_attackers = 3000
n_exchanges = 10_000_000
attacks_percent = 0.1

# main.py
COLS = {
    'src_ip': "src_ip",
    'dest_ip': "dst_ip",
    'syn': "syn_flg",
    'ack': "ack_flg",
}
naive_result = 'results/zipf_{}_naive.csv'
estimation_result = 'results/zipf_{}_dcs_threshold_{}_fix-coll_{}'

# user defined parameters for dcs algorithmn
delta = 0.05
epsilon = 1 / 3
k = 10
estimation_result += f'_k_{k}.csv'
