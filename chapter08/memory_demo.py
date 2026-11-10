"""第 8 章小练习：最小记忆系统，离线理解工作记忆与长期记忆。

运行检查：uv run python chapter08/check_memory.py
这里的关键词检索只是入门模拟，不代表语义检索。
"""

import json
from pathlib import Path


class MemoryStore:
    def __init__(self) -> None:
        self.working: list[dict[str, object]] = []
        self.long_term: list[dict[str, object]] = []

    def remember(self, text: str, importance: int) -> None:
        """编码并暂存一条新记忆。"""
        # TODO 1：创建一个字典，包含 "text" 和 "importance" 两个键，
        # 其中 text 要先用 .strip() 去掉两端空白，再追加到 self.working。
        temp_memory = {}
        temp_memory["text"] = text.strip()
        temp_memory["importance"] = importance
        self.working.append(temp_memory)
        return 
        raise NotImplementedError("请完成 TODO 1：remember")

    def retrieve(self, keyword: str) -> list[str]:
        """在工作记忆和长期记忆中，按关键词找回文本。"""
        # TODO 2：依次遍历 working、long_term；
        # 若 keyword（不区分大小写）出现在某条记忆的 text 中，就把 text 加入结果。
        # 返回文本列表，不修改原有记忆。
        text = []
        for working in self.working:
            if keyword.casefold() in working["text"].casefold():
                text.append(working["text"])
        for long_term in self.long_term:
            if keyword.casefold() in long_term["text"].casefold():
                text.append(long_term["text"])
        return text
        raise NotImplementedError("请完成 TODO 2：retrieve")

    def consolidate(self, min_importance: int) -> None:
        """把足够重要的工作记忆转入长期记忆。"""
        # TODO 3：importance >= min_importance 的条目从 working 移到 long_term；
        # 其余条目仍留在 working。不要在遍历 working 时直接从中删除元素。
        new_working = []
        transprot = []
        for working in self.working:
            if working["importance"] >= min_importance:
                transprot.append(working)
            else:
                new_working.append(working)
        self.long_term.extend(transprot)
        self.working = new_working
        return  
        raise NotImplementedError("请完成 TODO 3：consolidate")

    def forget_working(self) -> None:
        """模拟当前会话结束：清空工作记忆，但保留长期记忆。"""
        # TODO 4：只清空 self.working。
        self.working.clear()
        return
        raise NotImplementedError("请完成 TODO 4：forget_working")

    def save(self, path: str | Path) -> None:
        """仅将长期记忆保存为 JSON 文件。"""
        # TODO 5：使用 Path(path).write_text(...) 写入 JSON。
        # 可用 json.dumps(self.long_term, ensure_ascii=False) 生成字符串；
        # 写文件时指定 encoding="utf-8"。
        json_text = json.dumps(self.long_term, ensure_ascii=False)
        Path(path).write_text(json_text, encoding="utf-8")
        return
        raise NotImplementedError("请完成 TODO 5：save")

    @classmethod
    def load(cls, path: str | Path) -> "MemoryStore":
        """从 JSON 文件创建新的 MemoryStore 对象。"""
        # TODO 6：创建 cls() 对象，用 Path(path).read_text(encoding="utf-8")
        # 读出字符串，再用 json.loads(...) 还原到 long_term；返回该对象。
        # 新对象的 working 应保持为空。
        cls = MemoryStore()
        json_text = Path(path).read_text(encoding="utf-8")
        cls.long_term.extend(json.loads(json_text))
        return cls
        raise NotImplementedError("请完成 TODO 6：load")


if __name__ == "__main__":
    store = MemoryStore()
    store.remember("用户喜欢 Python", importance=8)
    store.remember("刚刚问过天气", importance=2)
    store.consolidate(min_importance=5)
    print("长期记忆：", store.long_term)
    print("检索 Python：", store.retrieve("Python"))
