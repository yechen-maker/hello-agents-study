"""第 6 章小练习：用 LangGraph 实现一个完全离线的「草稿 → 审查 → 返工」循环。

请亲手完成四个 TODO。这里用固定文本代替 LLM，因此运行不会调用模型或搜索 API。
运行检查：uv run python chapter06/check_graph_loop.py
"""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class DraftState(TypedDict):
    required_phrase: str  # 审查时要求草稿包含的词
    draft: str
    attempts: int
    max_attempts: int
    approved: bool
    trace: list[str]  # 记录实际经过的节点，如 ["draft", "review"]


def draft_node(state: DraftState) -> dict:
    """生成或修订草稿，只返回要更新的状态字段。"""
    # TODO 1：
    # 1. attempts 加 1，得到这次是第几稿。
    next_attempt = state["attempts"] + 1
    # 2. 第 1 稿固定为「先实现功能」；第 2 稿及以后固定为「先实现功能，再编写测试」。
    if next_attempt == 1:
        next_draft = '先实现功能'
    else:
        next_draft = '先实现功能，再编写测试'
    # 3. 返回 attempts、draft，以及在原 trace 后追加 "draft" 的新 trace。
    # 注意：不要直接修改传入的 state 或 state["trace"]。
    return {"attempts": next_attempt, "draft": next_draft, "trace": state["trace"] + ["draft"]}
    raise NotImplementedError("请完成 TODO 1：draft_node")


def review_node(state: DraftState) -> dict:
    """检查草稿是否包含要求的词。"""
    # TODO 2：
    # 返回 approved（required_phrase 是否出现在 draft 中），
    # 以及在原 trace 后追加 "review" 的新 trace。
    # if state["required_phrase"] in state["draft"]:
    #     next_approve = True
    # else:
    #     next_approve = False
    # return {"approved": next_approve, "trace": state["trace"] + ["review"]}
    return {"approved": True if state["required_phrase"] in state["draft"] else False, "trace": state["trace"] + ["review"]}
    raise NotImplementedError("请完成 TODO 2：review_node")


def route_after_review(state: DraftState) -> str:
    """决定结束，还是再写一稿；本函数只做判断，不修改状态。"""
    # TODO 3：已通过，或 attempts 达到 max_attempts 时，返回 "end"；
    # 否则返回 "revise"。
    if state["approved"] or state["attempts"] >= state["max_attempts"] :
        return "end"
    else:
        return "revise"
    raise NotImplementedError("请完成 TODO 3：route_after_review")


def build_graph():
    """组装并编译图。"""
    # TODO 4：
    # 1. 用 DraftState 创建 StateGraph。
    workflow = StateGraph(DraftState)
    # 2. 注册 "draft" 和 "review" 两个节点。
    workflow.add_node("draft", draft_node)
    workflow.add_node("review", review_node)
    # 3. 加普通边 START → draft → review。
    workflow.add_edge(START, "draft")
    workflow.add_edge("draft", "review")
    # 4. 从 review 加条件边：route_after_review 返回 "revise" 时去 draft；
    #    返回 "end" 时去 END。
    workflow.add_conditional_edges(
        "review",
        route_after_review,
        {"revise": "draft", "end": END}
    )
    # 5. 编译并返回图。
    return workflow.compile()
    raise NotImplementedError("请完成 TODO 4：build_graph")


def initial_state(required_phrase: str, max_attempts: int = 2) -> DraftState:
    """为每次独立运行准备初始状态；max_attempts 至少为 1。"""
    if max_attempts < 1:
        raise ValueError("max_attempts 至少为 1")
    return {
        "required_phrase": required_phrase,
        "draft": "",
        "attempts": 0,
        "max_attempts": max_attempts,
        "approved": False,
        "trace": [],
    }


if __name__ == "__main__":
    graph = build_graph()
    result = graph.invoke(initial_state("测试"))
    print("经过的节点：", " → ".join(result["trace"]))
    print("最终草稿：", result["draft"])
    print("尝试次数：", result["attempts"])
    print("是否通过：", result["approved"])
