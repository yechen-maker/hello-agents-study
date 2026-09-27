"""attention_demo.py 的检查器。"""

import math

from attention_demo import (
    attention_scores_shape,
    scaled_scores,
    softmax_rows,
    split_heads_shape,
)


def main() -> None:
    passed = 0

    def check(name: str, condition: bool) -> None:
        nonlocal passed
        if condition:
            passed += 1
            print(f"[通过] {name}")
        else:
            print(f"[未通过] {name}")

    head_shape = split_heads_shape((2, 3, 4), 2)
    check(
        "拆成两个头（每个维度都是整数）",
        head_shape == (2, 2, 3, 2)
        and all(type(dimension) is int for dimension in head_shape),
    )
    check(
        "Q 与转置后的 K 相乘后的形状",
        attention_scores_shape((2, 2, 3, 2), (2, 2, 5, 2)) == (2, 2, 3, 5),
    )

    queries = [[1.0, 0.0], [0.0, 1.0]]
    keys = [[1.0, 0.0], [0.0, 1.0]]
    scores = scaled_scores(queries, keys)
    correct_scores = (
        isinstance(scores, list)
        and len(scores) == 2
        and all(len(row) == 2 for row in scores)
        and math.isclose(scores[0][0], 1 / math.sqrt(2), abs_tol=1e-9)
        and math.isclose(scores[0][1], 0.0, abs_tol=1e-9)
        and math.isclose(scores[1][0], 0.0, abs_tol=1e-9)
        and math.isclose(scores[1][1], 1 / math.sqrt(2), abs_tol=1e-9)
    )
    check("缩放点积分数", correct_scores)

    weights = softmax_rows(scores) if correct_scores else None
    correct_weights = (
        isinstance(weights, list)
        and len(weights) == 2
        and all(len(row) == 2 for row in weights)
        and all(math.isclose(sum(row), 1.0, abs_tol=1e-9) for row in weights)
        and weights[0][0] > weights[0][1]
        and weights[1][1] > weights[1][0]
    )
    check("Softmax 逐行归一化", correct_weights)
    print(f"\n完成情况：{passed}/4")


if __name__ == "__main__":
    main()
