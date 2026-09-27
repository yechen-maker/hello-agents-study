"""第 3 章练习 2：用二维词向量观察语义相似度。

本练习只使用 Python 标准库，不需要安装 NumPy。
请亲手完成所有 TODO，然后运行本文件和 check_vector.py。
"""

import math


# 这些二维数字是为了教学而人工设计的，不是真实模型训练出的词向量。
WORD_VECTORS = {
    "小猫": (0.9, 0.8),
    "小狗": (0.8, 0.7),
    "汽车": (-0.8, 0.2),
}


def dot_product(vector_a: tuple[float, float], vector_b: tuple[float, float]) -> float:
    """计算两个二维向量的点积。"""
    # TODO 1：对应位置相乘后再相加。
    # 公式：(a1, a2) · (b1, b2) = a1*b1 + a2*b2
    dot_result = vector_a[0] * vector_b[0] + vector_a[1] * vector_b[1]
    return dot_result


def vector_length(vector: tuple[float, float]) -> float:
    """计算二维向量的长度。"""
    # TODO 2：使用 math.sqrt(...) 计算 sqrt(x*x + y*y)。
    length = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    return length


def cosine_similarity(
    vector_a: tuple[float, float],
    vector_b: tuple[float, float],
) -> float:
    """计算余弦相似度，越接近 1 表示两个向量方向越接近。"""
    length_a = vector_length(vector_a)
    length_b = vector_length(vector_b)

    if length_a == 0 or length_b == 0:
        return 0.0

    # TODO 3：套用公式：点积 /（向量A长度 * 向量B长度）。
    similarity = dot_product(vector_a, vector_b) / (length_a * length_b)
    return similarity



def compare_words(word_a: str, word_b: str) -> float:
    """从词向量表中取出两个词，并返回它们的余弦相似度。"""
    # TODO 4：
    # 1. 使用 WORD_VECTORS[word_a] 取出第一个词的向量。
    vector_a = WORD_VECTORS[word_a]
    # 2. 使用 WORD_VECTORS[word_b] 取出第二个词的向量。
    vector_b = WORD_VECTORS[word_b]
    # 3. 调用 cosine_similarity(...) 并返回结果。
    return cosine_similarity(vector_a, vector_b)


if __name__ == "__main__":
    print("词向量：")
    for word, vector in WORD_VECTORS.items():
        print(f"  {word}: {vector}")

    cat_dog = compare_words("小猫", "小狗")
    cat_car = compare_words("小猫", "汽车")

    print(f"\n小猫与小狗的余弦相似度：{cat_dog:.3f}")
    print(f"小猫与汽车的余弦相似度：{cat_car:.3f}")
    print(f"小猫和小狗是否更相似：{cat_dog > cat_car}")
