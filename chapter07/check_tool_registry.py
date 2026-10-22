"""工具对象与注册表练习的离线检查器。"""

from tool_registry_demo import AddTool, Tool, ToolRegistry


def check(label: str, test) -> bool:
    try:
        test()
    except Exception as exc:
        print(f"[未通过] {label}：{type(exc).__name__}: {exc}")
        return False
    print(f"[通过] {label}")
    return True


def test_tool() -> None:
    tool = AddTool()
    assert isinstance(tool, Tool)
    assert tool.name == "add"
    assert tool.description == "计算两个整数的和"
    assert tool.run({"a": 2, "b": 3}) == "5"


def test_parameters() -> None:
    assert AddTool().get_parameters() == ["a", "b"]


def test_register_tool() -> None:
    registry = ToolRegistry()
    tool = AddTool()
    registry.register_tool(tool)
    assert registry._tools["add"] is tool


def test_register_function() -> None:
    registry = ToolRegistry()
    echo = lambda text: text
    registry.register_function("echo", "原样返回", echo)
    assert registry._functions["echo"]["description"] == "原样返回"
    assert registry._functions["echo"]["func"] is echo


def test_description() -> None:
    registry = ToolRegistry()
    assert registry.get_tools_description() == "暂无可用工具"
    registry.register_tool(AddTool())
    registry.register_function("echo", "原样返回", lambda text: text)
    assert registry.get_tools_description() == (
        "- add: 计算两个整数的和\n- echo: 原样返回"
    )


def test_execute() -> None:
    registry = ToolRegistry()
    registry.register_tool(AddTool())
    registry.register_function("echo", "原样返回", lambda text: text)
    assert registry.execute_tool("add", {"a": 2, "b": 3}) == "5"
    assert registry.execute_tool("echo", "你好") == "你好"
    assert registry.execute_tool("missing", "anything") == "错误：未找到工具 missing"


def main() -> None:
    tests = [
        ("工具对象执行", test_tool),
        ("工具参数说明", test_parameters),
        ("注册工具对象", test_register_tool),
        ("注册普通函数", test_register_function),
        ("生成工具描述", test_description),
        ("按名称查找并执行", test_execute),
    ]
    passed = sum(check(label, test) for label, test in tests)
    print(f"\n完成情况：{passed}/{len(tests)}")


if __name__ == "__main__":
    main()
