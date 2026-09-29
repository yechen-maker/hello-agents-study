"""4.3 离线练习：只验证“先规划，再逐步执行并传递历史”。

这里的 30、25、70 是预设的执行结果，不是在调用真实模型。
"""


class ScriptedPlanner:
    def __init__(self, steps: list[str]) -> None:
        self.steps = steps
        self.calls = 0

    def plan(self, question: str) -> list[str]:
        self.calls += 1
        return self.steps.copy()


class ScriptedExecutor:
    def __init__(self, results: list[str]) -> None:
        self.results = iter(results)
        self.received: list[dict] = []

    def execute(
        self,
        question: str,
        plan: list[str],
        history: list[tuple[str, str]],
        current_step: str,
    ) -> str:
        """记录四项输入，按顺序返回预设结果。"""
        self.received.append({
            "question": question,
            "plan": plan.copy(),
            "history": history.copy(),
            "current_step": current_step,
        })
        return next(self.results)


class PlanAndSolveAgent:
    def __init__(self, planner: ScriptedPlanner, executor: ScriptedExecutor) -> None:
        self.planner = planner
        self.executor = executor
        self.history: list[tuple[str, str]] = []

    def run(self, question: str) -> str | None:
        self.history = []
        # TODO 1：只调用一次 planner.plan(question)，保存完整计划。
        plans = self.planner.plan(question)
        # TODO 2：按计划顺序遍历，把 question、完整计划、已有 history、当前步骤传给 executor.execute。
        for current_step in plans:
            current_result = self.executor.execute(question, plans, self.history, current_step)
        # TODO 3：将 (当前步骤, 本步结果) 加入 history，供下一步读取。
            self.history.append((current_step, current_result))
        # TODO 4：返回最后一步的结果；空计划时返回 None。
        if not self.history:
            return None
        return self.history[-1][-1]
        raise NotImplementedError("请完成 TODO 1～4")


if __name__ == "__main__":
    question = "周一卖出15个苹果；周二是周一两倍；周三比周二少5个。三天共卖出多少？"
    planner = ScriptedPlanner(["计算周二销量", "计算周三销量", "计算三天总销量"])
    executor = ScriptedExecutor(["30", "25", "70"])
    agent = PlanAndSolveAgent(planner, executor)
    print("最终答案：", agent.run(question))
    print("执行历史：", agent.history)
