"""第 8 章 8.4 案例整合离线检查器：验证记忆与 RAG 的工具封装、意图路由与 Prompt 组装。"""

from memory_demo import MemoryStore
from rag_demo import build_index
from integrated_demo import AssistantRouter, MemoryTool, RAGTool


def check(label: str, test) -> bool:
    try:
        test()
    except Exception as exc:
        print(f"[未通过] {label}：{type(exc).__name__}: {exc}")
        return False
    print(f"[通过] {label}")
    return True


def test_memory_tool() -> None:
    store = MemoryStore()
    store.working = [{"text": "用户偏好 Python 语言", "importance": 8}]
    store.long_term = [{"text": "用户偏好简洁的代码风格", "importance": 9}]

    tool = MemoryTool(store)
    result = tool.run("Python")
    assert result == "用户偏好 Python 语言"

    result_all = tool.run("偏好")
    assert "用户偏好 Python 语言" in result_all
    assert "用户偏好简洁的代码风格" in result_all

    result_none = tool.run("Java")
    assert result_none == ""


def test_rag_tool() -> None:
    docs = [
        {"source": "guide.md", "text": "RAG 可以结合外部资料增强模型的回答准确性。"},
        {"source": "rules.md", "text": "代码规范要求函数必须有清晰的注释。"},
    ]
    index = build_index(docs, chunk_size=30)
    tool = RAGTool(index)

    result = tool.run("RAG")
    assert "[来源: guide.md#1]" in result
    assert "RAG 可以结合外部资料" in result

    result_none = tool.run("不存在的内容")
    assert result_none == ""


def test_route() -> None:
    store = MemoryStore()
    index = build_index([], chunk_size=30)
    router = AssistantRouter(MemoryTool(store), RAGTool(index))

    # 包含个人偏好 -> memory
    assert router.route("请根据我的偏好推荐内容") == ["memory"]
    assert router.route("记录我的习惯") == ["memory"]

    # 包含外部资料 -> rag
    assert router.route("请查询教材中的定义") == ["rag"]
    assert router.route("文档里的规范是什么") == ["rag"]

    # 两者都有 -> both
    both_res = router.route("按照我的偏好，从教材中找一段解释")
    assert "memory" in both_res and "rag" in both_res

    # 都不包含 -> 默认 fallback 返回两者
    default_res = router.route("今天星期几")
    assert default_res == ["memory", "rag"]


def test_build_prompt() -> None:
    store = MemoryStore()
    store.working = [{"text": "偏好 Python 编程", "importance": 8}]

    docs = [
        {"source": "lesson.md", "text": "Agent 核心概念包含感知、规划与行动。"}
    ]
    index = build_index(docs, chunk_size=40)

    router = AssistantRouter(MemoryTool(store), RAGTool(index))

    # 1. 仅命中记忆
    prompt_mem = router.build_prompt("根据我的习惯回答", "Python")
    assert "【用户问题】根据我的习惯回答" in prompt_mem
    assert "【用户记忆】" in prompt_mem
    assert "偏好 Python 编程" in prompt_mem
    assert "【参考资料】" not in prompt_mem

    # 2. 仅命中资料
    prompt_rag = router.build_prompt("请阅读教材相关内容", "Agent")
    assert "【用户问题】请阅读教材相关内容" in prompt_rag
    assert "【参考资料】" in prompt_rag
    assert "[来源: lesson.md#1]" in prompt_rag
    assert "【用户记忆】" not in prompt_rag

    # 3. 两者结合
    prompt_both = router.build_prompt("结合我的偏好查阅教材", "Python")
    assert "【用户问题】结合我的偏好查阅教材" in prompt_both
    assert "【用户记忆】" in prompt_both
    assert "【参考资料】" not in prompt_both  # 因为文档中没有 Python，rag_tool 返回空字符串，不应拼出空的参考资料段落


def main() -> None:
    tests = [
        ("MemoryTool 包装与检索", test_memory_tool),
        ("RAGTool 包装与带来源检索", test_rag_tool),
        ("意图路由分类", test_route),
        ("Prompt 组装与上下文整合", test_build_prompt),
    ]
    passed = sum(check(label, test) for label, test in tests)
    print(f"\n完成情况：{passed}/{len(tests)}")


if __name__ == "__main__":
    main()
