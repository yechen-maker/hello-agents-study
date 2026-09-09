"""第二关检查器。先完成 warmup.py，再运行本文件。"""

from manual_agent import fake_model, get_weather, run_agent


def main() -> None:
    failures: list[str] = []

    weather = get_weather("成都")
    if weather != "成都今天晴，气温 25 摄氏度":
        failures.append("get_weather 的固定返回值被意外修改")

    first_action = fake_model([{"role": "user", "content": "查询天气"}])
    if first_action.get("type") != "tool":
        failures.append("第一次决策应该要求调用工具")

    try:
        answer, history = run_agent()
    except (TypeError, ValueError) as error:
        failures.append(f"run_agent 还没有正确返回两个结果：{error}")
    else:
        if answer != "查询完成：成都今天晴，气温 25 摄氏度":
            failures.append(f"最终答案不正确，实际得到：{answer!r}")

        observations = [item for item in history if item.get("role") == "observation"]
        if len(observations) != 1:
            failures.append(f"历史中应该正好有 1 条 observation，实际有 {len(observations)} 条")

    if failures:
        print("第二关尚未通过：")
        for failure in failures:
            print(f"- {failure}")
        return

    print("第二关通过：你已经跑通了一个不依赖 LLM 的最小 Agent 循环。")


if __name__ == "__main__":
    main()

