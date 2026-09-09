"""面向初学者的热身练习检查器。"""

from warmup import add, build_tool_registry, call_tool, make_greeting, temperature_label


def check(description: str, actual, expected) -> bool:
    if actual == expected:
        print(f"[通过] {description}")
        return True

    print(f"[未通过] {description}")
    print(f"   期望：{expected!r}")
    print(f"   实际：{actual!r}")
    return False


def main() -> None:
    results = [
        check("问候语", make_greeting("小明"), "你好，小明！"),
        check("9 度属于寒冷", temperature_label(9), "寒冷"),
        check("10 度属于舒适", temperature_label(10), "舒适"),
        check("27 度属于舒适", temperature_label(27), "舒适"),
        check("28 度属于炎热", temperature_label(28), "炎热"),
        check("加法函数", add(2, 3), 5),
    ]

    tools = build_tool_registry()
    results.extend(
        [
            check("注册表包含 add", isinstance(tools, dict) and tools.get("add") is add, True),
            check("通过注册表调用工具", call_tool("add", tools, a=2, b=3), 5),
            check(
                "不存在的工具会返回易懂的错误",
                call_tool("missing", tools),
                "错误：没有名为 missing 的工具",
            ),
        ]
    )

    passed = sum(results)
    total = len(results)
    print(f"\n完成情况：{passed}/{total}")
    if passed == total:
        print("热身通过，可以进入第一个 Agent。")
    else:
        print("请根据上面的‘期望’和‘实际’修改 warmup.py，然后再次运行。")


if __name__ == "__main__":
    main()
