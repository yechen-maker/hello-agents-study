"""第 1 章第二关：不用大语言模型，先理解 Agent 循环。

请先完成 warmup.py 并通过检查器，再做本文件中的 TODO。
"""


def get_weather(city: str) -> str:
    """返回用于练习的固定天气，暂时不访问网络。"""
    return f"{city}今天晴，气温 25 摄氏度"


TOOLS = {
    "get_weather": get_weather,
}


def fake_model(history: list[dict]) -> dict:
    """用普通规则假装自己是模型。

    没有观察结果时，它要求调用天气工具；
    已经得到观察结果时，它要求结束任务。
    """
    observations = [item for item in history if item["role"] == "observation"]

    if not observations:
        return {
            "type": "tool",
            "tool_name": "get_weather",
            "arguments": {"city": "成都"},
        }

    return {
        "type": "finish",
        "answer": f"查询完成：{observations[-1]['content']}",
    }


def run_agent(max_steps: int = 3) -> tuple[str, list[dict]]:
    """运行最小 Agent，并同时返回最终答案和完整历史。"""
    history: list[dict] = [
        {"role": "user", "content": "请查询成都今天的天气"},
    ]

    # TODO 1：最多循环 max_steps 次。
    for i in range(max_steps):
    # TODO 2：每轮调用 fake_model(history)，得到 action 字典。
        action = fake_model(history)
    # TODO 3：如果 action["type"] 是 "finish"，返回答案和历史。
        if action["type"] == 'finish':
            return  [action['answer'], history]

    # TODO 4：如果它要求调用工具：
    #   a. 从 TOOLS 中找到函数；
    #   b. 使用 action["arguments"] 调用函数；
    #   c. 把结果以下面的格式追加到 history：
    #      {"role": "observation", "content": 工具结果}
        elif action["type"] == 'tool':
            tool = TOOLS[action["tool_name"]]
            content = tool(action["arguments"]['city'])
            history.append({"role": "observation", "content": content})
    # TODO 5：如果循环次数用完仍未结束，返回“错误：超过最大行动次数”和历史。
        if i == max_steps - 1:
            return ["错误：超过最大行动次数", history]

if __name__ == "__main__":
    final_answer, agent_history = run_agent()
    print(final_answer)
    print("\n完整历史：")
    for message in agent_history:
        print(message)

