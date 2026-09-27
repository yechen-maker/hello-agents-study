"""第 3 章练习 1：亲手实现一个最小 Bigram 语言模型。

当前练习只使用 Python 标准库，不需要安装新依赖。
请完成所有 TODO，然后运行本文件观察结果，再运行 check_ngram.py。
"""


CORPUS = [
    "datawhale agent learns",
    "datawhale agent works",
]


def tokenize_corpus(corpus: list[str]) -> list[str]:
    """把多句话切分并合并成一个 Token 列表。"""
    tokens = []

    for sentence in corpus:
        # TODO 1：
        # 1. 使用 sentence.split() 把当前句子切成单词。
        words = sentence.split()
        # 2. 使用 tokens.extend(...) 把这些单词加入 tokens。
        tokens.extend(words)

    return tokens


def build_bigrams(tokens: list[str]) -> list[tuple[str, str]]:
    """把 Token 列表变成相邻词对列表。"""
    # TODO 2：使用 zip(tokens, tokens[1:]) 产生相邻词对，
    result = list(zip(tokens, tokens[1:]))
    # 再使用 list(...) 将结果转换为列表并返回。
    return result


def unigram_probability(word: str, tokens: list[str]) -> float:
    """计算一个词在全部 Token 中出现的概率。"""
    if not tokens:
        return 0.0

    # TODO 3：
    # 一个词的概率 = 这个词出现的次数 / Token 总数。
    count_word = 0
    count_token = 0
    for token in tokens:
        count_token += 1
        if word == token:
            count_word += 1
    return count_word / count_token


def conditional_probability(
    next_word: str,
    previous_word: str,
    tokens: list[str],
) -> float:
    """计算 P(next_word | previous_word)。"""
    previous_count = tokens.count(previous_word)

    # 如果作为条件的词从未出现，就无法继续做除法。
    if previous_count == 0:
        return 0.0

    bigrams = build_bigrams(tokens)

    # TODO 4：
    # 1. 使用 bigrams.count((previous_word, next_word)) 统计目标词对。
    count_bigrams = bigrams.count((previous_word, next_word))
    # 2. 用词对次数除以 previous_word 的次数并返回。
    return count_bigrams / previous_count


def sentence_bigram_probability(sentence: str, tokens: list[str]) -> float:
    """按照教程的 Bigram 近似方法计算一个句子的概率。"""
    words = sentence.split()

    if not words:
        return 0.0

    # 先计算句子第一个词的概率。
    probability = unigram_probability(words[0], tokens)

    # TODO 5：
    # 遍历句子中的每一对相邻词，计算条件概率，
    for previous_word, next_word in build_bigrams(words):

    # 再使用 probability *= 条件概率，把它们依次相乘。
        probability *= conditional_probability(next_word, previous_word, tokens)

    return probability


if __name__ == "__main__":
    corpus_tokens = tokenize_corpus(CORPUS)

    print(f"语料库 Token：{corpus_tokens}")
    print(f"相邻词对：{build_bigrams(corpus_tokens)}")
    print(f"P(agent)：{unigram_probability('agent', corpus_tokens):.3f}")
    print(
        "P(works | agent)："
        f"{conditional_probability('works', 'agent', corpus_tokens):.3f}"
    )
    print(
        "P(agent works)："
        f"{sentence_bigram_probability('agent works', corpus_tokens):.3f}"
    )
    print(
        "P(agent codes)："
        f"{sentence_bigram_probability('agent codes', corpus_tokens):.3f}"
    )
