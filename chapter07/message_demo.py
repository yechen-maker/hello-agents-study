"""第 7 章小练习：实现最小 Message 类，不调用模型或网络。

教程使用 Pydantic；这里先用普通 Python 类理解字段和转换，暂不增加依赖。
运行检查：uv run python chapter07/check_message.py
"""

from datetime import datetime
from typing import Any, Literal


MessageRole = Literal["user", "assistant", "system", "tool"]


class Message:
    """框架内部的一条消息。"""

    def __init__(
        self,
        content: str,
        role: MessageRole,
        timestamp: datetime | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        # TODO 1：保存 content、role、timestamp、metadata 四个实例属性。
        # timestamp 没有传入时用 datetime.now()；metadata 没有传入时用新字典。
        # 注意：Literal 是类型提示，不会自动检查运行时的字符串。
        # 如果 role 不在四种允许的角色中，主动 raise ValueError。
        if role in ("user", "assistant", "system", "tool"):
            self.content = content
            self.role = role
            self.timestamp = timestamp if timestamp is not None else datetime.now()
            self.metadata = metadata if metadata is not None else {}
        else:
            raise ValueError
        # raise NotImplementedError("请完成 TODO 1：初始化消息")

    def to_dict(self) -> dict[str, str]:
        """只返回模型 API 所需的 role 和 content。"""
        # TODO 2：返回形如 {"role": "user", "content": "你好"} 的字典。
        # 不要把 timestamp 或 metadata 放进这个字典。
        return {'role': self.role, 'content': self.content}
        raise NotImplementedError("请完成 TODO 2：转换为 API 字典")

    def __str__(self) -> str:
        """供开发者阅读的消息表示，例如 [user] 你好。"""
        # TODO 3：返回 [角色] 内容，注意方括号和空格。
        return f'[{self.role}] {self.content}'
        raise NotImplementedError("请完成 TODO 3：消息显示格式")


if __name__ == "__main__":
    message = Message(content="你好", role="user")
    print("内部消息：", message)
    print("API 字典：", message.to_dict())
