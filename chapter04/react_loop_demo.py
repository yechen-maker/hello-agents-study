"""4.2.3 小练习：不联网，模拟两轮 ReAct 循环。"""

import re

from tool_executor_demo import ToolExecutor


class ScriptedLLM:
    """按顺序返回预设文字，代替暂时无法连通的模型服务。"""

    def __init__(self, outputs: list[str]) -> None:
        self.outputs = iter(outputs)
        self.prompts: list[str] = []

    def think(self, messages: list[dict[str, str]]) -> str:
        self.prompts.append(messages[0]["content"])
        return next(self.outputs)


class ReActAgent:
    def __init__(self, llm_client: ScriptedLLM, tool_executor: ToolExecutor, max_steps: int = 3) -> None:
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.history: list[str] = []

    def _parse_output(self, text: str) -> tuple[str | None, str | None]:
        """从模型输出中提取 Thought 和 Action。"""
        # TODO 1：参考教材 4.2.3（3），分别提取 Thought 和 Action。
        # 找不到时对应返回 None；找到后去掉两端空白。
        # Thought: 匹配到 Action: 或文本末尾
        thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", text, re.DOTALL)
        # Action: 匹配到文本末尾
        action_match = re.search(r"Action:\s*(.*?)$", text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action
        # raise NotImplementedError("请完成 TODO 1")

    def _parse_action(self, action_text: str) -> tuple[str | None, str | None]:
        """例如从 Weather[北京] 得到 ("Weather", "北京")。"""
        # TODO 2：参考教材，用 re.match 提取方括号前的工具名和括号内的输入。
        match = re.match(r"(\w+)\[(.*)\]", action_text, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return None, None
        # raise NotImplementedError("请完成 TODO 2")

    def run(self, question: str) -> str | None:
        self.history = []
        for _ in range(self.max_steps):
            tools_desc = "\n".join(
                f"- {name}: {info['description']}"
                for name, info in self.tool_executor.tools.items()
            )
            prompt = f"可用工具:\n{tools_desc}\n问题: {question}\n历史:\n" + "\n".join(self.history)
            response_text = self.llm_client.think([{"role": "user", "content": prompt}])
            thought, action = self._parse_output(response_text)
            if not action:
                return None

            # TODO 3：如果 action 是 Finish[答案]，提取答案并直接返回。
            # 注意：Finish 不应当当成普通工具，也不需要再追加 Observation。
            if action.startswith("Finish"):
                final_answer = re.match(r"Finish\[(.*)\]", action).group(1)
                print(f'最终答案:{final_answer}')
                return final_answer

            # TODO 4：解析普通 Action，查找并调用工具。
            # 工具不存在时，observation 设为易懂的错误文字。
            # 把本轮的 Action 和 Observation 追加到 self.history。
            tool_name, tool_input = self._parse_action(action)
            if not tool_name or not tool_input:
                # ... 处理无效Action格式 ...
                continue

            print(f"🎬 行动: {tool_name}[{tool_input}]")

            tool_function = self.tool_executor.get_tool(tool_name)
            if not tool_function:
                observation = f'错误，未找到工具{tool_name}'
            else:
                observation = tool_function(tool_input)
            self.history.append("Action: " + action)
            self.history.append("Observation: " + observation)
            # raise NotImplementedError("请完成 TODO 3 和 TODO 4")
        return None  # 达到最大步数仍未 Finish


if __name__ == "__main__":
    tools = ToolExecutor()
    tools.register_tool("Weather", "查询城市天气", lambda city: f"{city}晴天")
    llm = ScriptedLLM([
        "Thought: 先查天气\nAction: Weather[北京]",
        "Thought: 已知北京晴天\nAction: Finish[适合户外游览]",
    ])
    agent = ReActAgent(llm, tools)
    print("最终答案：", agent.run("北京今天适合户外游览吗？"))
    print("历史：", agent.history)
