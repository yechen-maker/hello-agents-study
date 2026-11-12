# AI 教学接力交接文档 (AI Handover Guide)

> **双 AI 协同机制说明**：
> 本项目由两位 AI 助手交替辅导学习者（如周中由国内环境 AI 辅导，周末由 Antigravity 辅导）。
> **本文件是两位 AI 之间的“工作交接黑板”与进度同步中枢**。请接班的 AI **务必仔细阅读本指南**，严格遵守既定的教学约定与节奏，实现无缝衔接！

---

## 一、核心原则与教学风格（⚠️ 极其重要）

1. **把学习者当完全的小白教学**：
   - 用大白话、生活化比喻（如“做小抄”、“快递箱”）拆解抽象概念，切忌直接抛出一堆黑话或复杂专业术语。
   - 语法细节要讲透（比如 `if not x` 与 `if x is not None` 的区别、`@dataclass` 的作用等）。
2. **坚持“学习者先写，助手再引导”的原则**：
   - **绝对不要直接贴出整段完整代码给学习者抄！**
   - 每次只给清晰的思路拆解（TODO 指引）、参数与返回值说明；
   - 学习者先动手写，遇到错误时，按照约定引导：“先看错误类型、文件名和行号”，再给出递进式提示。
3. **离线优先、杜绝多余云端/付费依赖**：
   - 优先使用 Python 原生数据结构、本地文件进行可验证的小型核心实验。
   - 不为了完成教程示例而盲目安装 Qdrant、Docker、Neo4j 或调用付费 API。

---

## 二、学习资料与参考教材

- **项目主教程**：Datawhale 开源教程《Hello-Agents：从零开始构建智能体》
  - 在线阅读地址：[https://hello-agents.datawhale.cc/](https://hello-agents.datawhale.cc/)
- **本地项目环境**：
  - 包管理工具：`uv`（Python 3.11 虚拟环境）
  - 执行所有检查统一使用：`uv run python chapterXX/check_XX.py`

---

## 三、当前学习进度与历史成果

| 章节 | 名称 | 状态 | 核心成果 / 掌握情况 |
| :--- | :--- | :---: | :--- |
| **第 1 章** | 初识智能体与最小 Agent 循环 | ✅ 已完成 | Python 热身 9/9、最小无 LLM Agent 循环、工具调用 |
| **第 2 章** | 智能体发展史与规则机器人 | ✅ 理论完成 | 符号主义、ELIZA 模式匹配 |
| **第 3 章** | 大语言模型基础 | ✅ 已完成 | 语言模型、注意力机制、BPE 分词小实验全部通过 |
| **第 4 章** | 智能体经典范式构建 | ✅ 已完成 | ReAct (6/6)、Plan-and-Solve (7/7)、Reflection (6/6) 离线全通 |
| **第 5 章** | 低代码平台体验 | ⏭️ 选择性跳过 | 体验 Coze，概念映射完成，跳过低ROI拖拽 |
| **第 6 章** | 框架开发实践 | ✅ 已完成 | LangGraph 条件回环离线练习 5/5 通过，掌握节点/状态/条件边 |
| **第 7 章** | 构建你的智能体框架 | ✅ 已完成 | 手写 Message (5/5)、Config (4/4)、BaseAgent (6/6)、ToolRegistry (6/6) |
| **第 8 章** | 记忆与检索 | ✅ 已完成 | 记忆系统 (5/5)、RAG 切分检索 (4/4)、案例整合路由 (4/4) 全部全绿通关 |
| **第 9 章** | 上下文工程 | 🚧 **进行中** | 9.1~9.3 理论已掌握（GSSC 框架、上下文腐蚀、滑动窗口） |

---

## 四、接棒当前正在进行的事项（当前暂停点）

**当前所在章节：第 9 章《上下文工程》（Context Engineering）**

1. **已完成内容**：
   - 阅读并理解了 9.1 与 9.2（提示工程 vs 上下文工程、“迷失在中间”与上下文腐蚀）；
   - 阅读并理解了 9.3（GSSC 流水线：Gather 收集 $\rightarrow$ Select 筛选 $\rightarrow$ Structure 结构化 $\rightarrow$ Compress 压缩）；
   - 理解了 `@dataclass` 的作用。
2. **待完成任务（当前代码练习）**：
   - **练习文件**：`chapter09/context_builder_demo.py`
   - **检查文件**：`chapter09/check_context_builder.py`
   - **当前通过情况**：`1/4`（`ContextPacket 数据包初始化` 已通过）
   - **下一步具体动作**：
     - 指导学习者完成 `context_builder_demo.py` 中的 **TODO 1 (`prune_history`)**；
     - 逻辑：通过逆序遍历 `reversed(history)`，根据 `budget` 预算挑选最新的对话，超标停止，最后翻转回正常顺序返回。
     - 之后推进 TODO 2 (`build`)，将测试跑到 4/4 全绿。

---

## 五、仓库与远程配置（双端已同步）

- **主分支**：`main`
- **远程仓库**：
  - **Gitee（国内首选）**：`https://gitee.com/king-li-yanchen/hello-agents-study.git`（remote 名称：`gitee`）
  - **GitHub**：`https://github.com/yechen-maker/hello-agents-study.git`（remote 名称：`origin`）
  - 国内网络环境下优先使用 `git push gitee main` 和 `git pull gitee main`。
- **学习进度记录**：每章开始和结束均维护根目录的 `PROGRESS.md` 和 `README.md`，并在对应的 `chapterXX/README.md` 记录详细暂停点与验收标准。
- **Git 提交原则**：除非学习者明确要求，平时不擅自自动 commit 或 push；当章节全部通过、学习者要求提交时，先 `git diff --cached --stat` 核对无误后再提交。

---

## 六、双 AI 轮值交接协议（交班与接班规范）

为了保证两位 AI 能够互相无缝衔接，请在交接时严格遵守以下规范：

### 1. 交班规范（当次辅导结束时）
- **更新进度**：更新本文件「四、接棒当前正在进行的事项」中的**最新通过率、当前卡点与具体下一步动作**；
- **同步文档**：更新 `PROGRESS.md` 和对应 `chapterXX/README.md` 的暂停点勾选；
- **推送远端**：将最新代码推送到 Gitee（国内环境）和 GitHub（若网络可用）：
  ```bash
  git add .
  git commit -m "docs: handover - update chapter XX progress"
  git push gitee main
  # 若网络允许可同时 push origin main
  ```

### 2. 接班规范（下次辅导开始时）
- **同步远端**：接手第一步先拉取最新代码（防止对方有最新提交未同步）：
  ```bash
  git pull gitee main
  ```
- **阅读交接板**：仔细阅读本文件「四、接棒当前正在进行的事项」，确认上一次对话停在哪一行代码或哪一个小节；
- **无缝开场**：向学习者简述上一次停滞的位置，延续小白教学风格（耐心、比喻、引导手写、不贴整段代码），继续下一阶段辅导。
