"""运行：uv run python chapter04/check_react_loop.py（不调用模型 API）。"""

from react_loop_demo import ReActAgent, ScriptedLLM
from tool_executor_demo import ToolExecutor


def main() -> None:
    count = 0
    tools = ToolExecutor()
    tools.register_tool("Weather", "查询城市天气", lambda city: f"{city}晴天")
    llm = ScriptedLLM([
        "Thought: 先查天气\nAction: Weather[北京]",
        "Thought: 已知北京晴天\nAction: Finish[适合户外游览]",
    ])
    agent = ReActAgent(llm, tools)

    assert agent._parse_output("Thought: 先查天气\nAction: Weather[北京]") == ("先查天气", "Weather[北京]")
    print("[通过] 提取 Thought 和 Action")
    count += 1

    assert agent._parse_action("Weather[北京]") == ("Weather", "北京")
    print("[通过] 解析工具名称和输入")
    count += 1

    assert agent.run("北京今天适合户外游览吗？") == "适合户外游览"
    print("[通过] 两轮后返回 Finish 答案")
    count += 1

    assert agent.history == ["Action: Weather[北京]", "Observation: 北京晴天"]
    print("[通过] 记录行动与观察")
    count += 1

    assert "Observation: 北京晴天" in llm.prompts[1]
    print("[通过] 下一轮提示词包含上一轮观察")
    count += 1

    missing_llm = ScriptedLLM([
        "Thought: 尝试查询\nAction: Search[北京]",
        "Thought: 工具不存在\nAction: Finish[暂时无法搜索]",
    ])
    missing_agent = ReActAgent(missing_llm, tools)
    assert missing_agent.run("搜索北京") == "暂时无法搜索"
    assert "未找到" in missing_agent.history[1]
    print("[通过] 未注册工具变成可供下一轮读取的错误观察")
    count += 1

    print(f"\n完成情况：{count}/6")


if __name__ == "__main__":
    main()
