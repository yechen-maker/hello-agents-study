"""第 3 章练习 3：用标准库观察注意力权重和形状。

先完成 TODO，再运行本文件和 check_attention.py。
数值部分只有两个 Token、一个头；形状部分模拟多头注意力。
"""

import math


def split_heads_shape(
    input_shape: tuple[int, int, int], num_heads: int
) -> tuple[int, int, int, int]:
    """(批次, Token 数, d_model) → (批次, 头数, Token 数, 每头维度)。"""
    batch_size, seq_length, d_model = input_shape
    if d_model % num_heads != 0:
        raise ValueError("d_model 必须能被 num_heads 整除")

    # TODO 1：算出每个头的维度，并返回拆头后的形状。
    d_k = d_model // num_heads
    return (batch_size, num_heads, seq_length, d_k)
    pass


def attention_scores_shape(
    q_shape: tuple[int, int, int, int],
    k_shape: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    """Q @ Kᵀ 的输出形状：每个查询 Token 对每个 Key Token 都有一个分数。"""
    batch_size, num_heads, query_length, d_k = q_shape
    _, _, key_length, _ = k_shape

    # TODO 2：返回 (批次, 头数, 查询 Token 数, Key Token 数)。
    return (batch_size, num_heads, query_length, key_length)
    pass


def scaled_scores(
    queries: list[list[float]], keys: list[list[float]]
) -> list[list[float]]:
    """计算每个 Q 与每个 K 的点积，再除以 sqrt(d_k)。"""
    d_k = len(keys[0])
    result = []

    for query in queries:
        row = []
        for key in keys:
            # TODO 3：用 zip(query, key) 逐项相乘后求和，
            dot_product = 0
            for q, k in zip(query, key):
                dot_product += q * k
            # 再除以 math.sqrt(d_k)，把分数加入 row。
            score = dot_product / math.sqrt(d_k)
            row.append(score)
            pass
        result.append(row)

    return result


def softmax_rows(scores: list[list[float]]) -> list[list[float]]:
    """逐行做 Softmax：一行表示某个 Q 对所有 K 的关注比例。"""
    probabilities = []

    for row in scores:
        # TODO 4：
        exp_sum = 0
        score_probability = []
        for score in row:
            # 1. 用 math.exp(score) 算出这一行每个分数的指数。
            score_exp = math.exp(score)
            exp_sum += score_exp
        for score in row:
            # 2. 每个指数除以这一行所有指数之和。
            score_exp = math.exp(score)
            score_probability.append(score_exp / exp_sum)
        # 3. 把得到的一行概率加入 probabilities。
        probabilities.append(score_probability)
        pass

    return probabilities


if __name__ == "__main__":
    input_shape = (2, 3, 4)
    head_shape = split_heads_shape(input_shape, num_heads=2)
    score_shape = attention_scores_shape(head_shape, head_shape)
    print(f"输入形状：{input_shape}")
    print(f"拆头形状：{head_shape}")
    print(f"注意力分数形状：{score_shape}")

    # 数值例子：两个 Token，各用两个数字表示。
    queries = [[1.0, 0.0], [0.0, 1.0]]
    keys = [[1.0, 0.0], [0.0, 1.0]]
    scores = scaled_scores(queries, keys)
    probabilities = softmax_rows(scores)
    print(f"注意力分数：{scores}")
    print(f"注意力权重：{probabilities}")
