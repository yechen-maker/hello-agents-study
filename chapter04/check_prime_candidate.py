"""对已审阅的初稿运行边界和正确性检查，不执行原始模型回复。"""

from prime_candidate_initial import find_primes


def main() -> None:
    cases = {
        -1: [],
        0: [],
        1: [],
        2: [2],
        3: [2, 3],
        10: [2, 3, 5, 7],
        30: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29],
    }
    for n, expected in cases.items():
        actual = find_primes(n)
        assert actual == expected, f"n={n}: {actual} != {expected}"
    print(f"初稿正确性检查：{len(cases)}/{len(cases)} 通过")


if __name__ == "__main__":
    main()
