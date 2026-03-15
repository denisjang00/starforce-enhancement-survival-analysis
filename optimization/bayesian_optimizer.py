import optuna
import pandas as pd

from pathlib import Path
from core.simulator import simulate_player
from config.union_config import UNION_SEGMENTS

def objective(trial):
    """
    Objective:
    임계점 도달까지 평균 강화 횟수 최대화
    """

    policy = {
        "name": "optimized",
        "success_bonus": trial.suggest_float("success_bonus", 0, 0.1),
        "destroy_reduction": trial.suggest_float("destroy_reduction", 0, 0.05),
    }

    results = []

    for segment in UNION_SEGMENTS:
        for _ in range(1000):
            results.append(simulate_player(policy, segment))

    df = pd.DataFrame(results)

    mean_tries = df["tries_until_dropout"].mean()

    # 최대화 -> 음수 반환
    return -mean_tries


def run_bayesian(n_trials=20):
    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=n_trials)

    # Trial 결과 정리
    trials_data = []

    for trial in study.trials:
        trials_data.append({
            "trial": trial.number,
            "success_bonus": trial.params.get("success_bonus"),
            "destroy_reduction": trial.params.get("destroy_reduction"),
            "mean_tries": -trial.value  # 음수 복원
        })

    optimization_results = pd.DataFrame(trials_data)

    # csv 저장
    BASE_DIR = Path(__file__).resolve().parent.parent
    OUTPUT_DIR = BASE_DIR / "output"
    OUTPUT_DIR.mkdir(exist_ok=True)

    optimization_results.to_csv(
        OUTPUT_DIR / "optimization_results_raw.csv",
        index=False
    )

    print("optimization_results_raw.csv 저장 완료")

    # Best 결과 출력
    print("Best Params:", study.best_params)
    print("Best Mean Tries:", -study.best_value)

    return study