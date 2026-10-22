"""第 7 章小练习：Agent 抽象基类与消息历史，完全离线。

FakeLLM 只是占位对象，不会向任何模型发请求。
运行检查：uv run python chapter07/check_agent_base.py
"""

from abc import ABC, abstractmethod

from config_demo import Config
from message_demo import Message


class FakeLLM:
    """只提供 provider 名称，帮助观察 Agent 如何持有 LLM 依赖。"""

    provider = "offline"


class Agent(ABC):
    def __init__(
        self,
        name: str,
        llm: FakeLLM,
        system_prompt: str | None = None,
        config: Config | None = None,
    ) -> None:
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt
        self.config = config if config is not None else Config()
        self._history: list[Message] = []

    @abstractmethod
    def run(self, input_text: str) -> str:
        """子类必须实现统一的运行入口。"""

    def add_message(self, message: Message) -> None:
        """把一条消息加入内部历史。"""
        # TODO 1：把 message 追加到 self._history。
        self._history.append(message)
        return
        raise NotImplementedError("请完成 TODO 1：add_message")

    def clear_history(self) -> None:
        """清空内部历史。"""
        # TODO 2：清空 self._history。
        self._history.clear()
        return
        raise NotImplementedError("请完成 TODO 2：clear_history")

    def get_history(self) -> list[Message]:
        """返回历史列表的浅拷贝，避免调用方直接修改内部列表。"""
        # TODO 3：返回新的列表；列表中的 Message 对象无需复制。
        return self._history.copy()
        raise NotImplementedError("请完成 TODO 3：get_history")

    def __str__(self) -> str:
        return f"Agent(name={self.name}, provider={self.llm.provider})"


class EchoAgent(Agent):
    """不用真实模型的具体 Agent：收到什么，就确认收到什么。"""

    def run(self, input_text: str) -> str:
        # TODO 4：先记录一条 role="user"、content=input_text 的消息；
        # 再生成回答 f"收到：{input_text}"，记录一条 role="assistant" 的消息；
        # 最后返回回答字符串。请复用 self.add_message(...)。
        role = "user"
        content = input_text
        self.add_message(Message(role= role, content= content))
        reply = f"收到：{input_text}"
        self.add_message(Message(role = "assistant", content = reply))
        return reply
        raise NotImplementedError("请完成 TODO 4：EchoAgent.run")


if __name__ == "__main__":
    agent = EchoAgent(name="回声助手", llm=FakeLLM())
    print(agent)
    print(agent.run("你好"))
    for message in agent.get_history():
        print(message)
