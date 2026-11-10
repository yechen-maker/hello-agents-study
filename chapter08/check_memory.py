"""最小记忆系统的离线检查器；临时 JSON 文件会自动清理。"""

from pathlib import Path
from tempfile import TemporaryDirectory

from memory_demo import MemoryStore


def check(label: str, test) -> bool:
    try:
        test()
    except Exception as exc:
        print(f"[未通过] {label}：{type(exc).__name__}: {exc}")
        return False
    print(f"[通过] {label}")
    return True


def test_remember() -> None:
    store = MemoryStore()
    store.remember("  用户喜欢 Python  ", 8)
    assert store.working == [{"text": "用户喜欢 Python", "importance": 8}]
    assert store.long_term == []


def test_retrieve() -> None:
    store = MemoryStore()
    store.working = [{"text": "用户喜欢 Python", "importance": 8}]
    store.long_term = [{"text": "正在学习 Agent", "importance": 9}]
    assert store.retrieve("PYTHON") == ["用户喜欢 Python"]
    assert store.retrieve("学习") == ["正在学习 Agent"]
    assert store.retrieve("不存在") == []


def test_consolidate() -> None:
    store = MemoryStore()
    store.working = [
        {"text": "偏好 Python", "importance": 8},
        {"text": "刚问了天气", "importance": 2},
        {"text": "正在学习 Agent", "importance": 5},
    ]
    store.consolidate(5)
    assert store.long_term == [
        {"text": "偏好 Python", "importance": 8},
        {"text": "正在学习 Agent", "importance": 5},
    ]
    assert store.working == [{"text": "刚问了天气", "importance": 2}]


def test_forget() -> None:
    store = MemoryStore()
    store.working = [{"text": "临时消息", "importance": 1}]
    store.long_term = [{"text": "长期偏好", "importance": 8}]
    store.forget_working()
    assert store.working == []
    assert store.long_term == [{"text": "长期偏好", "importance": 8}]


def test_persistence() -> None:
    with TemporaryDirectory() as folder:
        path = Path(folder) / "memory.json"
        store = MemoryStore()
        store.working = [{"text": "一次性上下文", "importance": 1}]
        store.long_term = [{"text": "偏好中文回答", "importance": 9}]
        store.save(path)
        restored = MemoryStore.load(path)
        assert isinstance(restored, MemoryStore)
        assert restored is not store
        assert restored.working == []
        assert restored.long_term == store.long_term
        assert restored.retrieve("中文") == ["偏好中文回答"]


def main() -> None:
    tests = [
        ("编码并暂存新记忆", test_remember),
        ("按关键词检索两类记忆", test_retrieve),
        ("重要记忆转入长期记忆", test_consolidate),
        ("会话结束只遗忘工作记忆", test_forget),
        ("保存并恢复长期记忆", test_persistence),
    ]
    passed = sum(check(label, test) for label, test in tests)
    print(f"\n完成情况：{passed}/{len(tests)}")


if __name__ == "__main__":
    main()
