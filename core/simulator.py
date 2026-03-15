import random
import numpy as np

from config.probabilities import (
    STARFORCE_SUCCESS_PROB,
    STARFORCE_DESTROY_PROB
)
from config.dropout_config import UNION_THRESHOLD
from core.stress_model import update_stress


def simulate_player(policy, union_segment, max_star=27):
    """
    Threshold 기반 강화 시뮬레이션

    스타포스 확률 테이블 사용
    누적 스트레스가 threshold 도달 시 즉시 이탈
    """

    star = 15
    tries = 0
    fails = 0
    destroy = 0
    stress = 0
    consecutive_fail = 0
    max_consecutive_fail = 0

    threshold = np.random.normal(UNION_THRESHOLD[union_segment], 20)

    threshold = max(50, threshold)

    while star < max_star:

        tries += 1

        # 성공/파괴 확률 로드
        base_success = STARFORCE_SUCCESS_PROB.get(star, 0.01)
        base_destroy = STARFORCE_DESTROY_PROB.get(star, 0.0)

        # 정책 보정 적용
        success_prob = min(
            base_success + policy.get("success_bonus", 0),
            0.95
        )

        destroy_prob = max(
            base_destroy - policy.get("destroy_reduction", 0),
            0
        )

        # 이번 턴 이벤트 초기화
        fail_occurred = 0
        destroy_occurred = 0

        # 강화 시도
        if random.random() < success_prob:
            star += 1
            consecutive_fail = 0

        else:
            fails += 1
            consecutive_fail += 1
            fail_occurred = 1

            if random.random() < destroy_prob:
                destroy += 1
                star = max(15, star - 1)
                destroy_occurred = 1
        
        max_consecutive_fail = max(max_consecutive_fail, consecutive_fail)

        # 스트레스 누적 (이번 턴 기준)
        stress = update_stress(
            stress,
            fail_occurred,
            destroy_occurred,
            consecutive_fail
        )

        # Threshold 도달 -> 즉시 이탈
        if stress >= threshold:
            return {
                "final_star": star,
                "tries_until_dropout": tries,
                "dropout": 1,
                "union_segment": union_segment,
                "policy": policy["name"],
                "total_fails": fails,
                "total_destroy": destroy,
                "max_consecutive_fail": max_consecutive_fail,
                "threshold": threshold
            }

    # 목표 도달 (생존)
    return {
        "final_star": star,
        "tries_until_dropout": tries,
        "dropout": 0,
        "union_segment": union_segment,
        "policy": policy["name"],
        "total_fails": fails,
        "total_destroy": destroy,
        "max_consecutive_fail": max_consecutive_fail,
        "threshold": threshold
    }