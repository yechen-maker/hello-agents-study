"""第 7 章小练习：工具对象与注册表，完全离线。

运行检查：uv run python chapter07/check_tool_registry.py
"""

from abc import ABC, abstractmethod
from collections.abc import Callable


class Tool(ABC):
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, parameters: dict[str, int]) -> str:
        """执行工具，返回字符串结果。"""

    @abstractmethod
    def get_parameters(self) -> list[str]:
        """列出所需参数名。"""


class AddTool(Tool):
    def __init__(self) -> None:
        super().__init__("add", "计算两个整数的和")

    def run(self, parameters: dict[str, int]) -> str:
        # TODO 1：取出 parameters["a"] 和 parameters["b"]，
        # 相加后把结果转为字符串，例如 "5"。
        a = parameters["a"]
        b = parameters["b"]
        return str(a + b)
        raise NotImplementedError("请完成 TODO 1：AddTool.run")

    def get_parameters(self) -> list[str]:
        # TODO 2：返回所需参数名列表，顺序为 a、b。
        return ["a", "b"]
        raise NotImplementedError("请完成 TODO 2：AddTool.get_parameters")


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}
        self._functions: dict[str, dict[str, object]] = {}

    def register_tool(self, tool: Tool) -> None:
        # TODO 3：以 tool.name 为键，将工具对象放入 self._tools。
        self._tools[tool.name] = tool
        return 
        raise NotImplementedError("请完成 TODO 3：register_tool")

    def register_function(
        self, name: str, description: str, func: Callable[[str], str]
    ) -> None:
        # TODO 4：以 name 为键，把 description 和 func 存到 self._functions。
        # 结构示例：{"echo": {"description": "原样返回", "func": 某函数}}
        # 注意这里存的是函数本身，不要立刻调用它。
        self._functions[name] = {"description": description, "func": func}
        return
        raise NotImplementedError("请完成 TODO 4：register_function")

    def get_tools_description(self) -> str:
        """生成给 Agent 阅读的工具说明。"""
        # TODO 5：按注册顺序遍历对象工具、函数工具；每个工具占一行：
        # - add: 计算两个整数的和
        # - echo: 原样返回
        # 无工具时返回 "暂无可用工具"。
        descriptions = []
        for tool in self._tools.values():
            descriptions.append(f"- {tool.name}: {tool.description}")
        "\n".join(descriptions)
        for name, info in self._functions.items():
            descriptions.append(f"- {name}: {info['description']}")

        if not descriptions:
            return "暂无可用工具"
        return "\n".join(descriptions)
            
        raise NotImplementedError("请完成 TODO 5：get_tools_description")

    def execute_tool(self, name: str, parameters: dict[str, int] | str) -> str:
        """查找并执行工具；对象工具接收字典，函数工具接收字符串。"""
        # TODO 6：先查 self._tools，再查 self._functions。
        # 对象工具调用它的 run(parameters)；函数工具调用保存的 func(parameters)。
        # 找不到时返回 f"错误：未找到工具 {name}"。
        # 本题已约定传入的参数类型正确，无需写复杂的参数解析。
        if name in self._tools:
            tool = self._tools[name]
            result = tool.run(parameters)
        elif name in self._functions:
            func = self._functions[name]["func"]
            result = func(parameters)
        else:
            return f"错误：未找到工具 {name}"
        return result
        raise NotImplementedError("请完成 TODO 6：execute_tool")


if __name__ == "__main__":
    registry = ToolRegistry()
    registry.register_tool(AddTool())
    registry.register_function("echo", "原样返回", lambda text: text)
    print(registry.get_tools_description())
    print(registry.execute_tool("add", {"a": 2, "b": 3}))
