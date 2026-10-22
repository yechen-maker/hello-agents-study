"""Config 小练习的离线检查器；临时设置环境变量，不改系统配置。"""

import os
from unittest.mock import patch

from config_demo import Config


def check(label: str, test) -> bool:
    try:
        test()
    except Exception as exc:
        print(f"[未通过] {label}：{type(exc).__name__}: {exc}")
        return False
    print(f"[通过] {label}")
    return True


def test_defaults() -> None:
    with patch.dict(os.environ, {}, clear=True):
        config = Config.from_env()
    assert isinstance(config, Config)
    assert config.debug is False
    assert config.log_level == "INFO"
    assert config.temperature == 0.7
    assert config.max_tokens is None
    assert config.default_model == "gpt-3.5-turbo"
    assert config.default_provider == "openai"
    assert config.max_history_length == 100


def test_debug() -> None:
    with patch.dict(os.environ, {"DEBUG": "TRUE"}, clear=True):
        assert Config.from_env().debug is True
    with patch.dict(os.environ, {"DEBUG": "False"}, clear=True):
        assert Config.from_env().debug is False


def test_values() -> None:
    variables = {
        "DEBUG": "true",
        "LOG_LEVEL": "WARNING",
        "TEMPERATURE": "0.25",
        "MAX_TOKENS": "256",
    }
    with patch.dict(os.environ, variables, clear=True):
        config = Config.from_env()
    assert config.log_level == "WARNING"
    assert config.temperature == 0.25
    assert isinstance(config.temperature, float)
    assert config.max_tokens == 256
    assert isinstance(config.max_tokens, int)


def test_dict() -> None:
    config = Config(debug=True, max_tokens=128)
    expected = {
        "default_model": "gpt-3.5-turbo",
        "default_provider": "openai",
        "temperature": 0.7,
        "max_tokens": 128,
        "debug": True,
        "log_level": "INFO",
        "max_history_length": 100,
    }
    result = config.to_dict()
    assert result == expected
    result["debug"] = False
    assert config.debug is True, "导出的字典不能改变原 Config 对象"


def main() -> None:
    tests = [
        ("未设置环境变量时使用默认值", test_defaults),
        ("DEBUG 字符串转布尔值", test_debug),
        ("温度和 Token 数转为数字", test_values),
        ("导出独立的完整配置字典", test_dict),
    ]
    passed = sum(check(label, test) for label, test in tests)
    print(f"\n完成情况：{passed}/{len(tests)}")


if __name__ == "__main__":
    main()
