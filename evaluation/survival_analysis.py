import pandas as pd
import numpy as np

from lifelines import KaplanMeierFitter

def run_survival_analysis(df):

    kmf = KaplanMeierFitter()

    for policy in df["policy"].unique():

        subset = df[df["policy"] == policy]

        kmf.fit(
            durations=subset["tries_until_dropout"],
            event_observed=subset["dropout"],
            label=policy
        )

        kmf.plot_survival_function()

def compute_kaplan_meier(df):
    results = []

    for (segment, policy), group in df.groupby(["union_segment", "policy"]):
        data = group.sort_values("tries_until_dropout")
        durations = data["tries_until_dropout"]
        events = data["dropout"]

        survival_prob = 1.0

        for t in np.sort(durations.unique()):
            at_risk = (durations >= t).sum()
            events_at_t = ((durations == t) & (events == 1)).sum()

            if at_risk > 0:
                survival_prob *= (1 - events_at_t / at_risk)

            results.append({
                "tries_until_dropout": t,
                "at_risk": at_risk,
                "events": events_at_t,
                "survival_probability": survival_prob,
                "union_segment": segment,
                "policy": policy
            })

    return pd.DataFrame(results)

def compute_median_survival(km_df):
    """
    Kaplan-Meier 결과에서 Median Survival Time 계산
    """
    medians = []

    for (segment, policy), group in km_df.groupby(["union_segment", "policy"]):
        group = group.sort_values("tries_until_dropout")

        # survival_probability가 0.5 이하가 되는 최초 시점
        median_row = group[group["survival_probability"] <= 0.5]

        if len(median_row) > 0:
            median_time = median_row.iloc[0]["tries_until_dropout"]
        else:
            median_time = None  # 0.5 이하로 떨어지지 않는 경우

        medians.append({
            "union_segment": segment,
            "policy": policy,
            "median_survival_time": median_time
        })

    return pd.DataFrame(medians)

def compute_goal_survival(km_df, goal=22):
    """
    목표 강화 수치까지 생존할 확률 계산
    """
    results = []

    for (segment, policy), group in km_df.groupby(["union_segment", "policy"]):
        group = group.sort_values("tries_until_dropout")

        # 목표 시점 이하 중 가장 큰 값 선택
        eligible = group[group["tries_until_dropout"] <= goal]

        if len(eligible) > 0:
            survival_at_goal = eligible.iloc[-1]["survival_probability"]
        else:
            survival_at_goal = 1.0

        results.append({
            "union_segment": segment,
            "policy": policy,
            "goal": goal,
            "goal_survival_probability": survival_at_goal
        })

    return pd.DataFrame(results)