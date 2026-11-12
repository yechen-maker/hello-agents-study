"""第 9 章 9.4 核心实践：轻量级上下文构建器（GSSC 流水线与预算裁剪）。

运行检查：uv run python chapter09/check_context_builder.py
核心目标：
1. 掌握 @dataclass 结构化管理上下文候选项 (Gather)
2. 掌握滑动窗口逆序裁剪历史对话 (Compress)
3. 掌握有限预算下保住系统人设与当前提问的分区组装 (Structure)
"""

from dataclasses import dataclass, field


@dataclass
class ContextPacket:
    """承载原始上下文的候选包（对应 Gather 阶段）。

    使用 @dataclass 自动生成 __init__、__repr__ 等样板代码。
    """
    system_prompt: str
    query: str
    history: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)


class ContextBuilder:
    """上下文构建器（执行 Select、Compress、Structure）。"""

    def __init__(self, max_chars: int = 200) -> None:
        self.max_chars = max_chars

    def prune_history(self, history: list[str], budget: int) -> list[str]:
        """按预算从最新向最旧保留历史记录（滑动窗口逆序挑选）。"""
        # TODO 1：
        # history 是按时间正序排列的字符串列表，越靠后越新：["第1轮旧消息", "第2轮", "第3轮最新"]。
        # 挑选逻辑：
        # 1. 准备一个空列表 selected，以及已用字符计数 used_len = 0；
        # 2. 从最后一条（最新）开始倒序向前遍历（提示：可用 reversed(history)）；
        # 3. 如果 used_len + len(msg) <= budget：
        #    把 msg 加入 selected，并将 used_len 加上 len(msg)；
        #    否则直接 break（停止挑选）；
        # 4. 把 selected 逆序翻转回正常的时间顺序（提示：reversed(selected) 或 selected[::-1]）并返回。
        raise NotImplementedError("请完成 TODO 1：ContextBuilder.prune_history")

    def build(self, packet: ContextPacket) -> str:
        """执行 GSSC：保住高优先级内容，裁剪历史，结构化拼装。"""
        # TODO 2：
        # 1. 准备核心固定段落（必须保留）：
        #    sys_sec = f"【系统角色】\n{packet.system_prompt}"
        #    query_sec = f"【当前提问】\n{packet.query}"
        #
        # 2. 计算当前已占用字符数与剩余预算：
        #    base_len = len(sys_sec) + len(query_sec)
        #    remaining_budget = self.max_chars - base_len
        #
        # 3. 准备可选段落列表 optional_sections = []：
        #    - 如果 packet.references 非空：
        #      ref_text = "【参考资料】\n" + "\n".join(packet.references)
        #      若 len(ref_text) <= remaining_budget：
        #          optional_sections.append(ref_text)
        #          remaining_budget -= len(ref_text)
        #
        #    - 如果 packet.history 非空 且 remaining_budget > 0：
        #      调用 self.prune_history(packet.history, remaining_budget) 得到保留的历史列表；
        #      若保留列表非空：
        #          hist_text = "【历史对话】\n" + "\n".join(保留的历史列表)
        #          optional_sections.append(hist_text)
        #
        # 4. 拼装所有段落并返回：
        #    按顺序组合：[sys_sec] + optional_sections + [query_sec]
        #    用 "\n\n".join(...) 拼接返回。
        raise NotImplementedError("请完成 TODO 2：ContextBuilder.build")
