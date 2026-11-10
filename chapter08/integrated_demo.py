"""第 8 章 8.4 案例整合：记忆与 RAG 的最小离线联动。

运行检查：uv run python chapter08/check_integrated.py
将 Memory 作为查个人的工具，将 RAG 作为查资料的工具，
由 Assistant 根据意图路由并拼接带来源的 Prompt。
"""

from memory_demo import MemoryStore
from rag_demo import build_index, format_context, search_chunks


class MemoryTool:
    """包装记忆系统为工具接口。"""

    def __init__(self, store: MemoryStore) -> None:
        self.store = store

    def run(self, keyword: str) -> str:
        """检索记忆。若找到内容，用换行拼接后返回；若无结果，返回空字符串。"""
        # TODO 1：调用 self.store.retrieve(keyword) 检索记忆列表。
        # 如果列表非空，用 "\n".join(...) 拼接返回；
        # 如果为空，返回 ""。
        res = self.store.retrieve(keyword)
        if res:
            return "\n".join(res)
        else:
            return ''
        raise NotImplementedError("请完成 TODO 1：MemoryTool.run")


class RAGTool:
    """包装 RAG 检索系统为工具接口。"""

    def __init__(self, index: list[dict[str, object]]) -> None:
        self.index = index

    def run(self, keyword: str, limit: int = 3) -> str:
        """检索资料。返回带来源格式化后的字符串。"""
        # TODO 2：调用 search_chunks(keyword, self.index, limit=limit) 检索片段。
        # 再调用 format_context(matches) 返回整理好的字符串（无结果时 format_context 本身会返回 ""）。
        matches = search_chunks(keyword, self.index, limit)
        return format_context(matches)
        raise NotImplementedError("请完成 TODO 2：RAGTool.run")


class AssistantRouter:
    """分流助手：决定调用什么工具，并组装带上下文的 Prompt。"""

    def __init__(self, memory_tool: MemoryTool, rag_tool: RAGTool) -> None:
        self.memory_tool = memory_tool
        self.rag_tool = rag_tool

    def route(self, query: str) -> list[str]:
        """根据 query 关键词决定启用哪些工具：['memory']、['rag'] 或 ['memory', 'rag']。"""
        # TODO 3：意图路由：
        # - 如果 query 中包含 "我"、"偏好"、"习惯" 中的任意一个词，把 "memory" 加入工具列表；
        # - 如果 query 中包含 "教材"、"文档"、"规范" 中的任意一个词，把 "rag" 加入工具列表；
        # - 如果两个都没命中（即列表为空），默认返回 ["memory", "rag"] 作为保底；
        # 返回工具列表。
        tools = []
        if any(word in query for word in ["我", "偏好", "习惯"]):
            tools.append("memory")
        if any(word in query for word in ["教材", "文档", "规范"]):
            tools.append("rag")
        if not tools:
            return ["memory", "rag"]
        return tools
        raise NotImplementedError("请完成 TODO 3：AssistantRouter.route")

    def build_prompt(self, query: str, keyword: str) -> str:
        """根据路由结果检索上下文，组装出最终交付给模型的完整 Prompt。"""
        # TODO 4：组装 Prompt：
        # 1. 调用 self.route(query) 获取要启用的工具列表；
        tools = self.route(query)
        # 2. 准备一个段落列表 sections，第一个段落放入 f"【用户问题】{query}"；
        sections = []
        sections.append(f"【用户问题】{query}")
        # 3. 如果工具列表中包含 "memory"：
        #    调用 self.memory_tool.run(keyword) 获取结果；
        #    若结果非空（bool(res) 为 True），向 sections 追加 f"【用户记忆】\n{res}"；
        if "memory" in tools:
            res = self.memory_tool.run(keyword)
            if bool(res) == True:
                sections.append(f"【用户记忆】\n{res}")
        # 4. 如果工具列表中包含 "rag"：
        #    调用 self.rag_tool.run(keyword) 获取结果；
        #    若结果非空（bool(res) 为 True），向 sections 追加 f"【参考资料】\n{res}"；
        if "rag" in tools:
            res = self.rag_tool.run(keyword)
            if bool(res) == True:
                sections.append(f"【参考资料】\n{res}")
        # 5. 用 "\n\n".join(sections) 拼接并返回。
        return "\n\n".join(sections)
        raise NotImplementedError("请完成 TODO 4：AssistantRouter.build_prompt")
