"""vector_demo.py 的自动检查器。"""

import math

from vector_demo import (
    compare_words,
    cosine_similarity,
    dot_product,
    vector_length,
)


passed = 0
total = 0


def check(name: str, actual, expected, tolerance: float = 1e-9) -> None:
    """检查数值结果，并显示容易理解的反馈。"""
    global passed, total
    total += 1

    if actual is not None and math.isclose(actual, expected, abs_tol=tolerance):
        passed += 1
        print(f"[通过] {name}")
    else:
        print(f"[未通过] {name}")
        print(f"  你的结果：{actual}")
        print(f"  期望结果：{expected}")


def check_true(name: str, condition: bool) -> None:
    """检查一个判断是否成立。"""
    global passed, total
    total += 1

    if condition:
        passed += 1
        print(f"[通过] {name}")
    else:
        print(f"[未通过] {name}")


def main() -> None:
    check("点积", dot_product((1.0, 2.0), (3.0, 4.0)), 11.0)
    check("向量长度", vector_length((3.0, 4.0)), 5.0)
    check(
        "方向完全相同的向量",
        cosine_similarity((1.0, 1.0), (2.0, 2.0)),
        1.0,
    )
    check(
        "方向垂直的向量",
        cosine_similarity((1.0, 0.0), (0.0, 1.0)),
        0.0,
    )
    check("零向量不会引发除零错误", cosine_similarity((0.0, 0.0), (1.0, 1.0)), 0.0)

    cat_dog = compare_words("小猫", "小狗")
    cat_car = compare_words("小猫", "汽车")
    relation_is_correct = (
        cat_dog is not None
        and cat_car is not None
        and cat_dog > cat_car
    )
    check_true("小猫与小狗比小猫与汽车更相似", relation_is_correct)

    print(f"\n完成情况：{passed}/{total}")


if __name__ == "__main__":
    main()
