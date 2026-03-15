def update_stress(stress, fail_occurred, destroy_occurred, consecutive_fail):
    """
    스트레스 누적 공식 (턴 단위)

    이번 실패 여부
    이번 파괴 여부
    연속 실패 제곱 패널티
    """

    stress += (
        1.2 * fail_occurred +
        3 * destroy_occurred +
        0.4 * (consecutive_fail ** 2)
    )

    return stress