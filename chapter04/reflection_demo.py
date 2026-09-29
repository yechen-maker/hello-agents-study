"""4.4 离线练习：用预设回复验证执行、反思、优化的顺序。

这里不调用模型，也不运行模型生成的代码；只检查流程和记忆。
"""


class Memory:
    def __init__(self) -> None:
        self.records: list[dict[str, str]] = []

    def add_record(self, record_type: str, content: str) -> None:
        # TODO 1：追加一条形如 {"type": ..., "content": ...} 的记录。
        self.records.append({"type" : record_type, "content": content})
        pass

    def get_last_execution(self) -> str | None:
        # TODO 2：从后往前找最近一条 type 为 "execution" 的记录。
        # 如果没有，返回 None。
        for last in reversed(self.records):
            if last["type"] == "execution":
                return last["content"]
        return None
        pass


class ScriptedLLM:
    """依次返回预设回复，并记录每次收到的提示词。"""

    def __init__(self, outputs: list[str]) -> None:
        self.outputs = iter(outputs)
        self.prompts: list[str] = []

    def ask(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return next(self.outputs)


class ReflectionAgent:
    def __init__(self, llm: ScriptedLLM, max_iterations: int = 3) -> None:
        self.llm = llm
        self.max_iterations = max_iterations
        self.memory = Memory()

    def run(self, task: str) -> str | None:
        self.memory = Memory()  # 每次新任务从空记忆开始
        # TODO 3：让 llm.ask 生成一次初稿，记为 execution。
        # 提示词可写成 f"初稿任务：{task}"。
        initial_execution = self.llm.ask(f"初稿任务：{task}")
        self.memory.add_record("execution", initial_execution)

        for _ in range(self.max_iterations):
            # TODO 4：取最近一次 execution，让 llm.ask 对它给出反馈，记为 reflection。
            # 提示词应包含 task 与最近一次代码，便于检查历史是否传对。
            last_execution = self.memory.get_last_execution()
            reflection = self.llm.ask(f"初稿任务：{task}\n最近一次代码:{last_execution}")
            self.memory.add_record("reflection", reflection)
            # TODO 5：若反馈包含“无需改进”，立即结束循环。
            # 否则把 task、最近一次代码和反馈交给 llm.ask 生成修订稿，
            # 并把修订稿记为新的一条 execution。
            if "无需改进" in reflection:
                break
            new_execution = self.llm.ask(f"初稿任务：{task}\n最近一次代码:{last_execution}\n反馈:{reflection}")
            self.memory.add_record("execution", new_execution)
            # raise NotImplementedError("请完成 TODO 4～5")

        return self.memory.get_last_execution()


if __name__ == "__main__":
    llm = ScriptedLLM(["版本一", "需要改进效率", "版本二", "无需改进"])
    agent = ReflectionAgent(llm)
    print("最终版本：", agent.run("编写找出素数的函数"))
    print("记忆记录：", agent.memory.records)
