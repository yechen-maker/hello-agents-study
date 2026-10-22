"""第 7 章小练习：把环境变量转换成框架配置，不调用模型或网络。

教程使用 Pydantic；这里沿用普通 Python 类，集中练习 from_env 的读取与类型转换。
运行检查：uv run python chapter07/check_config.py
"""

import os
from typing import Any


class Config:
    def __init__(
        self,
        default_model: str = "gpt-3.5-turbo",
        default_provider: str = "openai",
        temperature: float = 0.7,
        max_tokens: int | None = None,
        debug: bool = False,
        log_level: str = "INFO",
        max_history_length: int = 100,
    ) -> None:
        self.default_model = default_model
        self.default_provider = default_provider
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.debug = debug
        self.log_level = log_level
        self.max_history_length = max_history_length

    @classmethod
    def from_env(cls) -> "Config":
        """读取环境变量，得到一个 Config 对象。"""
        # TODO 1：读取 DEBUG、LOG_LEVEL、TEMPERATURE、MAX_TOKENS。
        # DEBUG 只有忽略大小写后等于 "true" 才是 True；缺省为 False。
        # LOG_LEVEL 缺省为 "INFO"；TEMPERATURE 缺省为浮点数 0.7。
        # MAX_TOKENS 未设置时是 None，设置后转换为 int。
        # 最后用 cls(...) 创建并返回对象；其他字段沿用 __init__ 的默认值。
        return cls(
            debug = os.getenv("DEBUG", 'false').lower() == 'true',
            log_level = os.getenv("LOG_LEVEL", "INFO"),
            temperature = float(os.getenv("TEMPERATURE", 0.7)),
            max_tokens = int(os.getenv("MAX_TOKENS")) if os.getenv("MAX_TOKENS") else None
        )
        raise NotImplementedError("请完成 TODO 1：从环境变量创建配置")

    def to_dict(self) -> dict[str, Any]:
        """返回全部七个配置字段组成的新字典。"""
        # TODO 2：键名与实例属性名一致；不要返回 self.__dict__ 本身。
        return {"default_model": self.default_model, 
                "default_provider": self.default_provider, 
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "debug": self.debug,
                "log_level": self.log_level,
                "max_history_length": self.max_history_length}
        raise NotImplementedError("请完成 TODO 2：导出配置字典")


if __name__ == "__main__":
    config = Config.from_env()
    print(config.to_dict())
