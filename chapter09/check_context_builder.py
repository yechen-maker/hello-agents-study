"""第 9 章 9.4 上下文构建器离线检查器。

验证：
1. ContextPacket 结构体数据承载
2. 历史对话逆序滑动窗口裁剪 (prune_history)
3. 预算内全量拼装与超预算优先级保留 (build)
"""

from context_builder_demo import ContextBuilder, ContextPacket


def check(label: str, test) -> bool:
    try:
        test()
    except Exception as exc:
        print(f"[未通过] {label}：{type(exc).__name__}: {exc}")
        return False
    print(f"[通过] {label}")
    return True


def test_packet() -> None:
    p = ContextPacket(system_prompt="你是一个助理", query="你好")
    assert p.system_prompt == "你是一个助理"
    assert p.query == "你好"
    assert p.history == []
    assert p.references == []


def test_prune_history() -> None:
    builder = ContextBuilder(max_chars=200)
    history = [
        "第一轮古老消息：字数很多很多",    # 13 字符
        "第二轮问答：短",                 # 7 字符
        "第三轮最新：也很短",             # 8 字符
    ]

    # 预算 16：只能装下第三轮 (8) 和第二轮 (7)，共 15 字符；第一轮装不下
    pruned = builder.prune_history(history, budget=16)
    assert pruned == ["第二轮问答：短", "第三轮最新：也很短"]

    # 预算 5：连第三轮都装不下，返回空列表
    assert builder.prune_history(history, budget=5) == []

    # 预算充足：全部保留，且保持原本时间顺序
    assert builder.prune_history(history, budget=50) == history


def test_build_within_budget() -> None:
    # 预算充裕（500 字符），所有模块都应保留
    builder = ContextBuilder(max_chars=500)
    packet = ContextPacket(
        system_prompt="你是一个资深 Python 导师",
        query="今天学习什么",
        history=["第一轮：讨论了环境", "第二轮：讨论了变量"],
        references=["【参考】教材第 9 章上下文工程"],
    )
    prompt = builder.build(packet)

    assert "【系统角色】\n你是一个资深 Python 导师" in prompt
    assert "【参考资料】\n【参考】教材第 9 章上下文工程" in prompt
    assert "【历史对话】\n第一轮：讨论了环境\n第二轮：讨论了变量" in prompt
    assert "【当前提问】\n今天学习什么" in prompt


def test_build_exceeds_budget() -> None:
    # 预算紧张（110 字符）：系统设定 + 当前提问必须在，历史超长只能保留最新
    builder = ContextBuilder(max_chars=110)
    packet = ContextPacket(
        system_prompt="你是 Python 助手",               # 必保
        query="请总结一下",                             # 必保
        history=[
            "古老历史：非常长非常长非常长非常长非常长非常长",  # 必须被裁剪
            "最新历史：短消息",                          # 预算够就留下
        ],
        references=[],
    )
    prompt = builder.build(packet)

    # 验证核心优先级
    assert "【系统角色】\n你是 Python 助手" in prompt
    assert "【当前提问】\n请总结一下" in prompt
    assert "古老历史" not in prompt
    assert "最新历史：短消息" in prompt
    assert len(prompt) <= 110


def main() -> None:
    tests = [
        ("ContextPacket 数据包初始化", test_packet),
        ("历史对话按预算逆序滑动裁剪", test_prune_history),
        ("预算充足时的全量结构化组装", test_build_within_budget),
        ("超出预算时的核心优先与动态压缩", test_build_exceeds_budget),
    ]
    passed = sum(check(label, test) for label, test in tests)
    print(f"\n完成情况：{passed}/{len(tests)}")


if __name__ == "__main__":
    main()
