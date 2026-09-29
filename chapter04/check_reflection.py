"""运行：uv run python chapter04/check_reflection.py（不调用模型 API）。"""

from reflection_demo import Memory, ReflectionAgent, ScriptedLLM


def main() -> None:
    memory = Memory()
    assert memory.get_last_execution() is None
    memory.add_record("execution", "版本一")
    memory.add_record("reflection", "需要改进效率")
    memory.add_record("execution", "版本二")
    assert memory.records == [
        {"type": "execution", "content": "版本一"},
        {"type": "reflection", "content": "需要改进效率"},
        {"type": "execution", "content": "版本二"},
    ]
    print("[通过] 按顺序保存执行与反思")

    assert memory.get_last_execution() == "版本二"
    print("[通过] 取到最近一次执行结果")

    llm = ScriptedLLM(["版本一", "需要改进效率", "版本二", "无需改进"])
    agent = ReflectionAgent(llm, max_iterations=3)
    assert agent.run("编写找出素数的函数") == "版本二"
    assert [r["type"] for r in agent.memory.records] == [
        "execution", "reflection", "execution", "reflection"
    ]
    print("[通过] 初稿、反馈、修订稿、停止反馈的顺序正确")

    assert len(llm.prompts) == 4
    assert "版本一" in llm.prompts[1]
    assert "版本一" in llm.prompts[2] and "需要改进效率" in llm.prompts[2]
    assert "版本二" in llm.prompts[3]
    print("[通过] 每轮提示词使用正确的旧版本与反馈")

    no_change = ReflectionAgent(ScriptedLLM(["初稿", "无需改进"]), max_iterations=3)
    assert no_change.run("任务") == "初稿"
    assert len(no_change.memory.records) == 2
    print("[通过] 无需改进时不再生成修订稿")

    limited = ReflectionAgent(ScriptedLLM(["初稿", "还需改进", "修订稿"]), max_iterations=1)
    assert limited.run("任务") == "修订稿"
    assert len(limited.memory.records) == 3
    print("[通过] 达到最大迭代次数后停止")

    print("\n完成情况：6/6")


if __name__ == "__main__":
    main()
