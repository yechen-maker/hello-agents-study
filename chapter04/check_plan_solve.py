"""运行：uv run python chapter04/check_plan_solve.py（不调用模型 API）。"""

from plan_solve_demo import PlanAndSolveAgent, ScriptedExecutor, ScriptedPlanner


def main() -> None:
    question = "周一卖出15个苹果；周二是周一两倍；周三比周二少5个。三天共卖出多少？"
    steps = ["计算周二销量", "计算周三销量", "计算三天总销量"]
    planner = ScriptedPlanner(steps)
    executor = ScriptedExecutor(["30", "25", "70"])
    agent = PlanAndSolveAgent(planner, executor)
    answer = agent.run(question)

    assert planner.calls == 1, "规划阶段应只调用一次"
    print("[通过] 先生成一次完整计划")

    assert [item["current_step"] for item in executor.received] == steps
    print("[通过] 按计划顺序执行")

    assert all(item["question"] == question and item["plan"] == steps for item in executor.received)
    print("[通过] 每步都收到原题和完整计划")

    assert executor.received[0]["history"] == []
    assert executor.received[1]["history"] == [(steps[0], "30")]
    assert executor.received[2]["history"] == [(steps[0], "30"), (steps[1], "25")]
    print("[通过] 历史结果逐步累积")

    assert agent.history == [(steps[0], "30"), (steps[1], "25"), (steps[2], "70")]
    print("[通过] Agent 保存完整执行历史")

    assert answer == "70"
    print("[通过] 返回最后一步结果")

    empty_agent = PlanAndSolveAgent(ScriptedPlanner([]), ScriptedExecutor([]))
    assert empty_agent.run(question) is None
    print("[通过] 空计划不会报错")

    print("\n完成情况：7/7")


if __name__ == "__main__":
    main()
