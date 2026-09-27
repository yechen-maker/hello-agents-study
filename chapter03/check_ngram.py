"""自动检查 ngram_demo.py；先独立完成练习，再运行本文件。"""

import math

from ngram_demo import (
    CORPUS,
    build_bigrams,
    conditional_probability,
    sentence_bigram_probability,
    tokenize_corpus,
    unigram_probability,
)


def check(label: str, actual, expected) -> bool:
    """比较结果并打印容易理解的检查信息。"""
    if isinstance(expected, float):
        passed = isinstance(actual, (int, float)) and math.isclose(
            actual,
            expected,
            rel_tol=1e-9,
            abs_tol=1e-9,
        )
    else:
        passed = actual == expected

    if passed:
        print(f"[通过] {label}")
        return True

    print(f"[未通过] {label}")
    print(f"  你的结果：{actual!r}")
    print(f"  期望结果：{expected!r}")
    return False


def main() -> None:
    tokens = tokenize_corpus(CORPUS)
    results = [
        check(
            "语料库切分",
            tokens,
            ["datawhale", "agent", "learns", "datawhale", "agent", "works"],
        ),
        check(
            "构造相邻词对",
            build_bigrams(["agent", "learns", "fast"]),
            [("agent", "learns"), ("learns", "fast")],
        ),
        check("P(agent)", unigram_probability("agent", tokens), 2 / 6),
        check(
            "P(works | agent)",
            conditional_probability("works", "agent", tokens),
            1 / 2,
        ),
        check(
            "P(agent works)",
            sentence_bigram_probability("agent works", tokens),
            1 / 6,
        ),
        check(
            "未出现的词使句子概率为 0",
            sentence_bigram_probability("agent codes", tokens),
            0.0,
        ),
        check(
            "空句子的概率为 0",
            sentence_bigram_probability("", tokens),
            0.0,
        ),
    ]

    passed_count = sum(results)
    print(f"\n完成情况：{passed_count}/{len(results)}")

    if passed_count != len(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
