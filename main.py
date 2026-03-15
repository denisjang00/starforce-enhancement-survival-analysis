import random
import numpy as np
import pandas as pd

from experiment.ab_test import run_ab_test
from evaluation.statistical_test import run_stat_tests
from evaluation.survival_analysis import (
    run_survival_analysis,
    compute_kaplan_meier,
    compute_median_survival,
    compute_goal_survival
)
from evaluation.cox_regression import run_cox_regression
from optimization.bayesian_optimizer import run_bayesian
from utils.export_to_csv import export_results


if __name__ == "__main__":

    # 재현성 확보
    random.seed(42)
    np.random.seed(42)

    print("===== Starforce Policy Optimization Pipeline Start =====")

    # A/B 테스트 실행
    print("\n[1] Running A/B Test Simulation...")
    results = run_ab_test(n=2000)

    # CSV 저장
    print("[2] Exporting A/B Results...")
    export_results(results)

    # DataFrame 변환
    df = pd.DataFrame(results)

    # 통계 검정
    print("[3] Running Statistical Tests...")
    run_stat_tests(df)

    # Survival 분석 (lifelines 시각화)
    print("[4] Running Survival Analysis (lifelines)...")
    run_survival_analysis(df)

    # Kaplan-Meier Survival Table 생성
    print("[5] Generating Survival Probability Table...")
    km_df = compute_kaplan_meier(df)
    km_df.to_csv("output/survival_results.csv", index=False)
    print("Survival results saved to output/survival_results.csv")

    # Median Survival Time 계산
    median_df = compute_median_survival(km_df)
    median_df.to_csv("output/median_survival_summary.csv", index=False)

    print("\nMedian Survival Time Summary")
    print(median_df)

    # Goal Survival Probability 계산
    goal_df = compute_goal_survival(km_df, goal=22)
    goal_df.to_csv("output/goal_survival_summary.csv", index=False)

    print("\nGoal Survival Probability (at 22)")
    print(goal_df)

    # Median + Goal Survival 통합 요약
    summary_df = median_df.merge(
        goal_df,
        on=["union_segment", "policy"],
        how="left"
    )

    summary_df.to_csv("output/policy_summary.csv", index=False)

    print("\nPolicy Summary (Median + Goal Survival)")
    print(summary_df)

    # Cox Regression 실행
    print("[6] Running Cox Proportional Hazards Model...")
    run_cox_regression(df)

    # Bayesian 최적화
    print("[7] Running Bayesian Optimization...")
    run_bayesian(n_trials=15)

    print("\n===== Pipeline Completed Successfully =====")