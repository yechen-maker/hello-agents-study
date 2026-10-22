"""Message 小练习的离线检查器。"""

from datetime import datetime

from message_demo import Message


def check(label: str, test) -> bool:
    try:
        test()
    except Exception as exc:
        print(f"[未通过] {label}：{type(exc).__name__}: {exc}")
        return False
    print(f"[通过] {label}")
    return True


def test_fields() -> None:
    message = Message(content="你好", role="user")
    assert message.content == "你好"
    assert message.role == "user"
    assert isinstance(message.timestamp, datetime)
    assert message.metadata == {}


def test_optional_fields() -> None:
    when = datetime(2026, 1, 2, 3, 4)
    extras = {"source": "exercise"}
    message = Message("工具结果", "tool", timestamp=when, metadata=extras)
    assert message.timestamp == when
    assert message.metadata == extras
    first = Message("第一条", "user")
    second = Message("第二条", "user")
    first.metadata["note"] = "只属于第一条"
    assert second.metadata == {}, "两条消息不能共用一个默认字典"


def test_role() -> None:
    try:
        Message("测试", "unknown")
    except ValueError:
        return
    raise AssertionError("无效角色应触发 ValueError")


def test_api_dict() -> None:
    message = Message("你好", "user", metadata={"source": "exercise"})
    assert message.to_dict() == {"role": "user", "content": "你好"}


def test_display() -> None:
    assert str(Message("你好", "user")) == "[user] 你好"


def main() -> None:
    tests = [
        ("保存消息字段与默认值", test_fields),
        ("传入可选字段且默认字典互不影响", test_optional_fields),
        ("拒绝无效角色", test_role),
        ("转换为模型 API 字典", test_api_dict),
        ("显示消息", test_display),
    ]
    passed = sum(check(label, test) for label, test in tests)
    print(f"\n完成情况：{passed}/{len(tests)}")


if __name__ == "__main__":
    main()
