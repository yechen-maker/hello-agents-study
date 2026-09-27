"""第 3 章练习 5：不使用正则，亲手实现简化版 BPE。

这里的字典键是用空格隔开的词元序列，值是该词出现的次数。
例如 "h u g </w>": 2 表示 hug 出现了两次。
"""


VOCAB = {
    "h u g </w>": 1,
    "p u g </w>": 1,
    "p u n </w>": 1,
    "b u n </w>": 1,
}


def count_pairs(vocab: dict[str, int]) -> dict[tuple[str, str], int]:
    """统计所有词中相邻词元对的出现次数。"""
    counts = {}

    for word, frequency in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pair = (symbols[i], symbols[i + 1])
            # TODO 1：给 counts[pair] 加上 frequency。
            # 提示：尚未出现的 pair，可以用 counts.get(pair, 0) 取得 0。
            counts[pair] = counts.get(pair, 0) + frequency
            pass

    return counts


def most_frequent_pair(
    counts: dict[tuple[str, str], int],
) -> tuple[str, str] | None:
    """选出次数最高的词对；没有词对时返回 None。"""
    if not counts:
        return None

    # TODO 2：参考教程中的 max(pairs, key=pairs.get)。
    return max(counts, key= counts.get)
    pass


def merge_pair(
    pair: tuple[str, str], vocab: dict[str, int]
) -> dict[str, int]:
    """把每个词中指定的相邻词元合并，并保留原来的词频。"""
    merged_vocab = {}

    for word, frequency in vocab.items():
        symbols = word.split()
        merged_symbols = []
        i = 0

        while i < len(symbols):
            # TODO 3：如果当前位置和下一位置正好组成 pair，
            # 就把它们拼成一个字符串，放进 merged_symbols，i 前进 2 位。
            if i + 1 < len(symbols) and pair == (symbols[i], symbols[i + 1]):
                merged_symbols.append(''.join(pair))
                i += 2
            # 否则只放入当前位置的词元，i 前进 1 位。
            # 注意先确认 i + 1 没有超过列表范围。
            else:
                merged_symbols.append(symbols[i])
                i += 1
            # raise NotImplementedError("请先完成 TODO 3：合并词元并更新 i")

        merged_word = " ".join(merged_symbols)
        merged_vocab[merged_word] = merged_vocab.get(merged_word, 0) + frequency

    return merged_vocab


if __name__ == "__main__":
    vocab = VOCAB.copy()

    for round_number in range(1, 5):
        counts = count_pairs(vocab)
        pair = most_frequent_pair(counts)
        if pair is None:
            print("没有可合并的相邻词元对，停止。")
            break

        vocab = merge_pair(pair, vocab)
        print(f"第 {round_number} 轮：{pair} → {''.join(pair)}")
        print(f"当前词元序列：{list(vocab)}")
