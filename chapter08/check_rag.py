"""离线检查 RAG 两条流程：切分建索引，以及按关键词检索并保留来源。"""

from rag_demo import build_index, format_context, search_chunks, split_text


def check(label: str, test) -> bool:
    try:
        test()
    except Exception as exc:
        print(f"[未通过] {label}：{type(exc).__name__}: {exc}")
        return False
    print(f"[通过] {label}")
    return True


def test_split() -> None:
    assert split_text("abcdefghij", 4) == ["abcd", "efgh", "ij"]
    assert split_text("", 4) == []
    try:
        split_text("abc", 0)
    except ValueError:
        pass
    else:
        raise AssertionError("chunk_size 为 0 时应抛出 ValueError")


def test_build_index() -> None:
    documents = [
        {"source": "a.md", "text": "abcdef"},
        {"source": "b.md", "text": "xyz"},
    ]
    assert build_index(documents, 4) == [
        {"source": "a.md", "chunk_id": 1, "text": "abcd"},
        {"source": "a.md", "chunk_id": 2, "text": "ef"},
        {"source": "b.md", "chunk_id": 1, "text": "xyz"},
    ]


def test_search() -> None:
    index = [
        {"source": "one.md", "chunk_id": 1, "text": "RAG 检索资料"},
        {"source": "two.md", "chunk_id": 1, "text": "Agent 调用工具"},
        {"source": "three.md", "chunk_id": 2, "text": "rag 标注来源"},
    ]
    original = [item.copy() for item in index]
    assert search_chunks("rag", index, 1) == [index[0]]
    assert search_chunks("RAG", index) == [index[0], index[2]]
    assert search_chunks("", index) == []
    assert search_chunks("rag", index, 0) == []
    assert index == original


def test_context() -> None:
    matches = [
        {"source": "one.md", "chunk_id": 2, "text": "RAG 检索资料"},
        {"source": "two.md", "chunk_id": 1, "text": "Agent 调用工具"},
    ]
    assert format_context(matches) == (
        "[来源: one.md#2] RAG 检索资料\n"
        "[来源: two.md#1] Agent 调用工具"
    )
    assert format_context([]) == ""


def main() -> None:
    tests = [
        ("按固定长度切分文本", test_split),
        ("建立索引并保留文档来源", test_build_index),
        ("检索时保留来源且不修改索引", test_search),
        ("整理带来源的资料", test_context),
    ]
    passed = sum(check(label, test) for label, test in tests)
    print(f"\n完成情况：{passed}/{len(tests)}")


if __name__ == "__main__":
    main()
