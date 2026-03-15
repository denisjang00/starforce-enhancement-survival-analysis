import pandas as pd

from pathlib import Path

# 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
DASHBOARD_DIR = BASE_DIR / "dashboard_data"

DASHBOARD_DIR.mkdir(exist_ok=True)

print(f"OUTPUT DIR: {OUTPUT_DIR}")
print(f"DASHBOARD DIR: {DASHBOARD_DIR}")

# 원본 CSV 로드
try:
    ab_results = pd.read_csv(OUTPUT_DIR / "ab_results.csv")
    survival_results = pd.read_csv(OUTPUT_DIR / "survival_results.csv")
    median_survival = pd.read_csv(OUTPUT_DIR / "median_survival_summary.csv")
    goal_survival = pd.read_csv(OUTPUT_DIR / "goal_survival_summary.csv")
    cox_results = pd.read_csv(OUTPUT_DIR / "cox_results.csv")
    optimization_results = pd.read_csv(OUTPUT_DIR / "optimization_results_raw.csv")

except FileNotFoundError:
    print("필요한 output CSV가 없습니다. 먼저 main.py를 실행하세요.")
    raise

# survival_curve.csv 생성
survival_results.to_csv(
    DASHBOARD_DIR / "survival_curve.csv",
    index=False
)

print("survival_curve.csv 생성 완료")

# summary_metrics.csv 생성
summary_from_ab = (
    ab_results
    .groupby(["union_segment", "policy"])
    .agg(
        mean_tries=("tries_until_dropout", "mean"),
        dropout_rate=("dropout", "mean")
    )
    .reset_index()
)

summary_metrics = (
    summary_from_ab
    .merge(median_survival, on=["union_segment", "policy"], how="left")
    .merge(goal_survival, on=["union_segment", "policy"], how="left")
)

summary_metrics.to_csv(
    DASHBOARD_DIR / "summary_metrics.csv",
    index=False
)

print("summary_metrics.csv 생성 완료")

# cox_hazard_ratio.csv 생성
cox_results.to_csv(
    DASHBOARD_DIR / "cox_hazard_ratio.csv",
    index=False
)

print("cox_hazard_ratio.csv 생성 완료")

# optimization 결과 정렬
optimization_results = optimization_results.sort_values(
    by="mean_tries",
    ascending=True
)

# optimization_results.csv 생성
optimization_results.to_csv(
    DASHBOARD_DIR / "optimization_results.csv",
    index=False
)

print("optimization_results.csv 생성 완료")

print("\nDashboard용 데이터 생성 완료")