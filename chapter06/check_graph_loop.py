"""第 6 章离线检查器；不会调用模型或搜索 API。"""

from graph_loop import (
    build_graph,
    draft_node,
    initial_state,
    review_node,
    route_after_review,
)


def check(label: str, test) -> bool:
    try:
        test()
    except Exception as exc:
        print(f"[未通过] {label}：{type(exc).__name__}: {exc}")
        return False
    print(f"[通过] {label}")
    return True


def test_first_draft() -> None:
    state = initial_state("功能")
    update = draft_node(state)
    assert update["attempts"] == 1
    assert update["draft"] == "先实现功能"
    assert update["trace"] == ["draft"]
    assert state["attempts"] == 0 and state["trace"] == [], "不要直接修改输入状态"


def test_revised_draft() -> None:
    state = initial_state("测试")
    state.update({"attempts": 1, "draft": "先实现功能", "trace": ["draft", "review"]})
    update = draft_node(state)
    assert update["attempts"] == 2
    assert update["draft"] == "先实现功能，再编写测试"
    assert update["trace"] == ["draft", "review", "draft"]


def test_review() -> None:
    state = initial_state("测试")
    state.update({"draft": "先实现功能，再编写测试", "trace": ["draft"]})
    update = review_node(state)
    assert update["approved"] is True
    assert update["trace"] == ["draft", "review"]
    assert state["trace"] == ["draft"], "不要直接修改输入状态"
    state["draft"] = "先实现功能"
    assert review_node(state)["approved"] is False


def test_route() -> None:
    state = initial_state("测试")
    state["attempts"] = 1
    assert route_after_review(state) == "revise"
    state["approved"] = True
    assert route_after_review(state) == "end"
    state["approved"] = False
    state["attempts"] = 2
    assert route_after_review(state) == "end"


def test_graph() -> None:
    graph = build_graph()
    cases = [
        ("功能", 1, True, ["draft", "review"]),
        ("测试", 2, True, ["draft", "review", "draft", "review"]),
        ("部署", 2, False, ["draft", "review", "draft", "review"]),
    ]
    for phrase, attempts, approved, trace in cases:
        result = graph.invoke(initial_state(phrase))
        assert result["attempts"] == attempts, (phrase, result)
        assert result["approved"] is approved, (phrase, result)
        assert result["trace"] == trace, (phrase, result)


def main() -> None:
    tests = [
        ("第一稿与状态更新", test_first_draft),
        ("返工后的第二稿", test_revised_draft),
        ("审查草稿", test_review),
        ("决定返工或结束", test_route),
        ("条件边与完整循环", test_graph),
    ]
    passed = sum(check(label, test) for label, test in tests)
    print(f"\n完成情况：{passed}/{len(tests)}")


if __name__ == "__main__":
    main()
