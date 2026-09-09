"""第 1 章 Python 热身。

请亲手完成所有 TODO。第一次运行出现结果不正确或检查失败很正常，
学习编程的重要部分就是根据反馈一点点修正代码。
"""


def make_greeting(name: str) -> str:
    """返回一句问候语，例如传入“小明”时返回“你好，小明！”。"""
    # TODO 1：使用 f-string 拼出问候语并返回。
    return f'你好，{name}！'


def temperature_label(temp_c: int) -> str:
    """根据温度返回“寒冷”“舒适”或“炎热”。

    规则：
    - 小于 10 度：寒冷
    - 10～27 度（包含边界）：舒适
    - 大于 27 度：炎热
    """
    # TODO 2：使用 if / elif / else 完成判断。
    if temp_c < 10:
        return "寒冷"
    elif temp_c >= 10 and temp_c <= 27 :
        return "舒适"
    elif temp_c > 27:
        return "炎热"

def add(a: float, b: float) -> float:
    """返回两个数字之和。"""
    # TODO 3：返回 a 与 b 相加的结果。
    return a + b


def build_tool_registry() -> dict:
    """建立工具注册表。

    注册表就是一个字典：键是工具名，值是可以执行的函数。
    """
    # TODO 4：返回一个字典，把字符串 "add" 映射到上面的 add 函数。
    return {"add": add}


def call_tool(tool_name: str, tools: dict, **kwargs):
    """根据工具名寻找并执行工具。

    如果工具不存在，返回：错误：没有名为 xxx 的工具
    """
    # TODO 5：
    # 1. 判断 tool_name 是否存在于 tools。
    # 2. 不存在时返回题目要求的错误文字。
    # 3. 存在时取出函数，并使用 **kwargs 调用它。
    if tool_name in tools:
        return tools[tool_name](**kwargs)
    else:
        return f'错误：没有名为 {tool_name} 的工具'


if __name__ == "__main__":
    print(make_greeting("小明"))
    print(temperature_label(22))

    tool_registry = build_tool_registry()
    print(call_tool("add", tool_registry, a=2, b=3))
    print(call_tool("missing", tool_registry))

