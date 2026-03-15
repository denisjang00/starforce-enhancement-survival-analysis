from core.simulator import simulate_player
from config.union_config import UNION_SEGMENTS

def run_ab_test(n=2000):

    baseline = {
        "name": "baseline",
        "success_bonus": 0,
        "destroy_reduction": 0,
    }

    advantage = {
        "name": "advantage",
        "success_bonus": 0.03,
        "destroy_reduction": 0.03,
    }

    results = []

    for segment in UNION_SEGMENTS:
        for _ in range(n):
            results.append(simulate_player(baseline, segment))
            results.append(simulate_player(advantage, segment))

    return results