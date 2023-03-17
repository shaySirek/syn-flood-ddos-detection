import pandas as pd

from settings import *


for a in zipf_a:
    ths = []
    fcs = []
    min_rel_errs = []
    max_rel_errs = []
    mean_rel_errs = []
    emp = []

    for threshold in [None, 50, 100, 200]:
        for fix_collision in [False, True]:
            result_file_name = estimation_result.format(
                a, threshold or 'default', fix_collision)
            df_results = pd.read_csv(result_file_name)

            ths.append(threshold or 'Theirs')
            fcs.append(fix_collision)
            min_rel_errs.append(round(df_results['relative_error'].min(), 3))
            max_rel_errs.append(round(df_results['relative_error'].max(), 3))
            mean_rel_errs.append(round(df_results['relative_error'].mean(), 3))
            emp.append('')

    summarized = pd.DataFrame(data={
        'threshold': ths,
        'last_bucket': emp,
        'distinct destinations in dSample': emp,
        'fix_collision': fcs,
        'min relative error': min_rel_errs,
        'max relative error': max_rel_errs,
        'mean relative error': mean_rel_errs
    })
    summarized.to_csv(f"summarized/zipf_{a}_results.csv")
