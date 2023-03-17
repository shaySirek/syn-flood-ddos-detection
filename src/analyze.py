import pandas as pd
import numpy as np

from dcs import ip2int


def analyze(top_k_ddos_victims, sources_per_dest: pd.Series, result_file_name: str):
    print(f"analyze {result_file_name} ...")
    
    ips = []
    reals = []
    real_idxs = []
    ests = []
    est_idxs = []
    rel_errs = []
    # analyze results
    for i, victim in enumerate(top_k_ddos_victims):
        ip, est_f = victim
        int_ip = ip2int(ip)

        # get real frequency
        idx = np.argwhere(sources_per_dest.index == int_ip)
        real_f = sources_per_dest.values[idx]
        idx, real_f = idx[0][0], real_f[0][0]

        relative_error = np.abs(est_f - real_f) / real_f

        ips.append(ip)
        reals.append(real_f)
        real_idxs.append(idx)
        ests.append(est_f)
        est_idxs.append(i)
        rel_errs.append(relative_error)

    df_results = pd.DataFrame(data={
        'dst_ip': ips,
        'real_sources_per_dest': reals,
        'real_idx': real_idxs,
        'est_sources_per_dest': ests,
        'est_idx': est_idxs,
        'relative_error': rel_errs
    })
    df_results.to_csv(result_file_name)
