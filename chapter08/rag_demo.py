"""第 8 章 RAG 热身：在本地模拟文档准备与检索，不调用模型。

运行检查：uv run python chapter08/check_rag.py
这里使用关键词匹配；向量检索和生成回答留给后续学习。
"""


DOCUMENTS = [
    {"source": "agent_notes.md", "text": "Agent可以调用工具完成任务。Agent也能记录用户偏好。"},
    {"source": "rag_notes.md", "text": "RAG先检索资料，再把相关片段交给模型。回答时应标注资料来源。"},
]


def split_text(text: str, chunk_size: int) -> list[str]:
    """按字符数切分文本；例如 abcdef、大小为 2，得到 ['ab', 'cd', 'ef']。"""
    # TODO 1：使用 range(0, len(text), chunk_size) 产生起点，
    # 每次取 text[start:start + chunk_size]，返回所有非空片段。
    # chunk_size <= 0 时抛出 ValueError；空文本返回空列表。
    result = []
    if chunk_size <= 0:
        raise ValueError
        return result
    else:
        for start in range(0, len(text), chunk_size):
            result.append(text[start: start + chunk_size])
        return result
    raise NotImplementedError("请完成 TODO 1：split_text")


def build_index(documents: list[dict[str, str]], chunk_size: int) -> list[dict[str, object]]:
    """把文档切成片段，并记录每片来自哪里。"""
    # TODO 2：依次处理 documents 中的每篇文档，用 split_text 切分其 text。
    # 每个片段保存为：
    # {"source": 文档的 source, "chunk_id": 从 1 开始的片段序号, "text": 片段内容}
    # 返回包含所有片段的列表。这里的列表就是最小版“索引”。
    result = []
    for document in documents:
        text = split_text(document["text"], chunk_size)
        i = 1
        for text_split in text:
            result.append({"source": document["source"], "chunk_id": i, "text": text_split})
            i += 1
    return result
    raise NotImplementedError("请完成 TODO 2：build_index")


def search_chunks(query: str, index: list[dict[str, object]], limit: int = 3) -> list[dict[str, object]]:
    """按关键词查找片段，保留索引中的来源信息。"""
    # TODO 3：忽略大小写，依原顺序挑出 text 包含 query 的片段，最多 limit 条。
    # 空查询或 limit <= 0 时返回 []；不要修改 index 或其中的字典。
    result = []
    if limit <= 0 or not query:
        return result
    i = 1
    for chunk in index:
        if i <= limit:
            if query.casefold() in chunk["text"].casefold():
                result.append(chunk)
                i += 1
    return result
    raise NotImplementedError("请完成 TODO 3：search_chunks")


def format_context(matches: list[dict[str, object]]) -> str:
    """把检索结果整理成可交给模型的资料，并标注来源。"""
    # TODO 4：每条结果写成 "[来源: source#chunk_id] text"，
    # 用换行拼接后返回。没有结果时返回空字符串。
    lines = []
    for match in matches:
        lines.append(f"[来源: {match['source']}#{match['chunk_id']}] {match['text']}")
    return '\n'.join(lines)
    raise NotImplementedError("请完成 TODO 4：format_context")


if __name__ == "__main__":
    index = build_index(DOCUMENTS, chunk_size=24)
    matches = search_chunks("RAG", index)
    print(format_context(matches))
