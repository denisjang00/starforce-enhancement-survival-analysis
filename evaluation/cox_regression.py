import pandas as pd

from pathlib import Path
from lifelines import CoxPHFitter

def run_cox_regression(df):

    print("\n[Running Cox Proportional Hazards Model]")

    cox_df = df.copy()

    # 범주형 변수 더미화
    cox_df = pd.get_dummies(
        cox_df,
        columns=["policy", "union_segment"],
        drop_first=True
    )

    # 사용할 변수 선택
    cols = [
        "tries_until_dropout",
        "dropout",
        "total_fails",
        "total_destroy",
        "max_consecutive_fail",
    ] + [col for col in cox_df.columns if "policy_" in col or "union_segment_" in col]

    cox_df = cox_df[cols]

    # cox 모델 적합
    cph = CoxPHFitter()
    cph.fit(
        cox_df,
        duration_col="tries_until_dropout",
        event_col="dropout"
    )

    cph.print_summary()

    # 결과 정리 및 csv 저장
    summary = cph.summary.reset_index()

    cox_results = pd.DataFrame({
        "variable": summary["covariate"],
        "hazard_ratio": summary["exp(coef)"],
        "lower_ci": summary["exp(coef) lower 95%"],
        "upper_ci": summary["exp(coef) upper 95%"],
        "p_value": summary["p"]
    })

    #경로 설정
    BASE_DIR = Path(__file__).resolve().parent.parent
    OUTPUT_DIR = BASE_DIR / "output"
    OUTPUT_DIR.mkdir(exist_ok=True)

    cox_results.to_csv(
        OUTPUT_DIR / "cox_results.csv",
        index=False
    )

    print("cox_results.csv 저장 완료")

    return cph