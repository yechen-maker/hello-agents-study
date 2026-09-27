"""bpe_demo.py 的学习检查器。"""

from bpe_demo import VOCAB, count_pairs, merge_pair, most_frequent_pair


def main() -> None:
    passed = 0

    def check(name: str, condition: bool) -> None:
        nonlocal passed
        print(f"[{'通过' if condition else '未通过'}] {name}")
        if condition:
            passed += 1

    counts = count_pairs(VOCAB)
    check("统计相邻对", counts.get(("u", "g")) == 2)

    weighted = count_pairs({"a b c": 3, "a b d": 2})
    check("按词频加权", weighted.get(("a", "b")) == 5)

    check("选出最高频词对", most_frequent_pair(counts) == ("u", "g"))

    try:
        merged = merge_pair(("u", "g"), VOCAB)
    except NotImplementedError:
        merged = {}
    check(
        "合并相邻词元并保留词频",
        merged.get("h ug </w>") == 1
        and merged.get("p ug </w>") == 1
        and merged.get("p u n </w>") == 1,
    )

    print(f"\n完成情况：{passed}/4")


if __name__ == "__main__":
    main()
