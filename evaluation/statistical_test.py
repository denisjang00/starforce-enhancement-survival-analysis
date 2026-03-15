import pandas as pd

from scipy.stats import ttest_ind
from statsmodels.stats.proportion import proportions_ztest


def run_stat_tests(df):

    for segment in df["union_segment"].unique():

        seg_df = df[df["union_segment"] == segment]

        base = seg_df[seg_df["policy"] == "baseline"]
        adv = seg_df[seg_df["policy"] == "advantage"]

        # 평균 강화 횟수 차이 (임계점 지연)
        t_stat, p_val = ttest_ind(
            base["tries_until_dropout"],
            adv["tries_until_dropout"]
        )

        print(f"\n[{segment}]")
        print("Mean Baseline:", base["tries_until_dropout"].mean())
        print("Mean Advantage:", adv["tries_until_dropout"].mean())
        print("p-value (t-test):", p_val)

        # 이탈률 차이
        count = [
            adv["dropout"].sum(),
            base["dropout"].sum()
        ]
        nobs = [
            len(adv),
            len(base)
        ]

        z_stat, p_val_z = proportions_ztest(count, nobs)

        print("p-value (dropout rate):", p_val_z)