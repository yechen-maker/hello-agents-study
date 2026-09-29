"""运行：uv run python chapter04/check_tool_executor.py"""

from tool_executor_demo import ToolExecutor, add


def main() -> None:
    checks = 0
    executor = ToolExecutor()
    executor.register_tool("Add", "计算两个整数的和", add)

    assert "Add" in executor.tools, "注册表中找不到 Add"
    print("[通过] 注册工具")
    checks += 1

    assert executor.tools["Add"]["description"] == "计算两个整数的和", "描述未保存"
    print("[通过] 保存工具描述")
    checks += 1

    tool = executor.get_tool("Add")
    assert tool is add, "get_tool 应返回函数本身"
    print("[通过] 按名称取出函数")
    checks += 1

    assert tool(a=2, b=3) == 5, "取出的函数没有正确执行"
    print("[通过] 调用取出的函数")
    checks += 1

    assert executor.get_tool("Weather") is None, "未注册工具应返回 None"
    print("[通过] 未注册工具返回 None")
    checks += 1

    print(f"\n完成情况：{checks}/5")


if __name__ == "__main__":
    main()
