"""4.2.2 小练习：不用网络，验证工具的注册、查找和调用。"""

from collections.abc import Callable


def add(a: int, b: int) -> int:
    """本地工具：返回两个整数的和。"""
    return a + b


class ToolExecutor:
    def __init__(self) -> None:
        self.tools: dict[str, dict] = {}

    def register_tool(self, name: str, description: str, func: Callable) -> None:
        """把工具的名称、描述和函数放入注册表。"""
        # TODO 1：以 name 为键，把 description 和 func 保存到 self.tools。
        self.tools[name] = {"description": description, "func": func}
        pass

    def get_tool(self, name: str) -> Callable | None:
        """按名称取出函数；不存在时返回 None。"""
        # TODO 2：参考教程 getTool；注意返回的是函数，不是函数调用结果。
        return self.tools.get(name, {}).get("func")
        pass


if __name__ == "__main__":
    executor = ToolExecutor()
    executor.register_tool("Add", "计算两个整数的和", add)

    # TODO 3：取出名为 "Add" 的函数，传入 a=2、b=3，打印结果。
    func = executor.get_tool("Add")
    print(func(2, 3))
    # 再取出不存在的 "Weather"，打印它的值。
    func = executor.get_tool("Weather")
