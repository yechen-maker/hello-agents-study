"""Agent 抽象基类小练习的离线检查器。"""

from agent_base_demo import Agent, EchoAgent, FakeLLM
from config_demo import Config
from message_demo import Message


def check(label: str, test) -> bool:
    try:
        test()
    except Exception as exc:
        print(f"[未通过] {label}：{type(exc).__name__}: {exc}")
        return False
    print(f"[通过] {label}")
    return True


def test_abstract() -> None:
    try:
        Agent("基础类", FakeLLM())
    except TypeError:
        pass
    else:
        raise AssertionError("抽象 Agent 不应能直接创建")

    class IncompleteAgent(Agent):
        pass

    try:
        IncompleteAgent("缺少 run", FakeLLM())
    except TypeError:
        return
    raise AssertionError("未实现 run 的子类不应能创建")


def test_initialization() -> None:
    llm = FakeLLM()
    custom = Config(debug=True)
    agent = EchoAgent("测试助手", llm, system_prompt="请简短回答", config=custom)
    assert agent.name == "测试助手"
    assert agent.llm is llm
    assert agent.system_prompt == "请简短回答"
    assert agent.config is custom
    assert str(agent) == "Agent(name=测试助手, provider=offline)"
    other = EchoAgent("另一位", llm)
    assert isinstance(other.config, Config)
    assert other.config is not custom


def test_add() -> None:
    agent = EchoAgent("测试助手", FakeLLM())
    message = Message("你好", "user")
    agent.add_message(message)
    assert agent._history == [message]


def test_get_copy() -> None:
    agent = EchoAgent("测试助手", FakeLLM())
    agent._history.append(Message("你好", "user"))
    outside = agent.get_history()
    assert outside == agent._history
    assert outside is not agent._history, "不能直接暴露内部列表"
    outside.clear()
    assert len(agent._history) == 1, "修改返回的列表不应清空内部历史"


def test_clear() -> None:
    agent = EchoAgent("测试助手", FakeLLM())
    agent._history.append(Message("你好", "user"))
    agent.clear_history()
    assert agent._history == []


def test_run() -> None:
    agent = EchoAgent("测试助手", FakeLLM())
    assert agent.run("你好") == "收到：你好"
    assert [(m.role, m.content) for m in agent.get_history()] == [
        ("user", "你好"),
        ("assistant", "收到：你好"),
    ]
    assert agent.run("再见") == "收到：再见"
    assert len(agent.get_history()) == 4, "第二轮不应覆盖第一轮历史"


def main() -> None:
    tests = [
        ("抽象类不能直接创建", test_abstract),
        ("保存核心依赖与默认配置", test_initialization),
        ("添加消息", test_add),
        ("取得历史列表的浅拷贝", test_get_copy),
        ("清空历史", test_clear),
        ("具体子类实现 run 并记录对话", test_run),
    ]
    passed = sum(check(label, test) for label, test in tests)
    print(f"\n完成情况：{passed}/{len(tests)}")


if __name__ == "__main__":
    main()
