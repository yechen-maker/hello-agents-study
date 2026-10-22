# 第 7 章：构建你的智能体框架

教程：[第七章 构建你的智能体框架](https://hello-agents.datawhale.cc/#/./chapter7/%E7%AC%AC%E4%B8%83%E7%AB%A0%20%E6%9E%84%E5%BB%BA%E4%BD%A0%E7%9A%84Agent%E6%A1%86%E6%9E%B6)

## 本章目标

把第四章手写的 Agent 与第六章的框架经验，整理成**自己理解、自己实现、能检查的小型框架**。本章代码量大，按教材顺序分段学习，但不一次复制整套 HelloAgents，也不为完成章节而部署本地模型或运行所有在线示例。每一段先理解接口和数据流，再安排一项可离线验证的小练习；需要模型调用时才使用现有配置，并留意费用。

## 穿插安排

1. **7.1 架构设计：**读 7.1.1～7.1.3 后暂停。对照第四章的代码，用自己的话解释 `core`、`agents`、`tools` 三层分别负责什么；想一想“万物皆为工具”的便利和可能的局限。先不安装教程的完整框架包。
2. **7.2 LLM 接口：**先看多提供商与自动检测的边界，再决定是否扩展第四章已有的客户端。7.2.2 本地模型部署属于可选项，已有相关经验时不重复部署。任何新增依赖或在线调用先核对实际需要。
3. **7.3 核心接口：**重点亲手实现或改编消息、配置、Agent 抽象接口中的最小集合，并配离线检查；不要同时铺开所有异常类和可选能力。
4. **7.4 Agent 实现：**先做最简单的 Agent，再比较 ReAct、Reflection、Plan-and-Solve 与第四章已有实现的共性；只重构能带来代码复用的部分，不为重复而重写全部范式。
5. **7.5 工具系统：**实现最小工具接口、注册和参数调用，再用一个纯本地工具检查。多源搜索、异步执行和工具链按实际开发需求选做。
6. **7.6 收尾：**运行本章已做练习的检查器，记录保留/跳过的理由；复盘自己的框架与第四章脚本相比减少了哪些重复代码，再学习 Git 提交和推送。

## 当前暂停点

- [x] 读完 7.1.1～7.1.3，理解 `core`、`agents`、`tools` 三层以及“记忆也当工具”的取舍。
- [x] 读完 7.2.1「支持多提供商」和 7.2.2「本地模型调用」，理解特定供应商的扩展方式及本地 OpenAI 兼容接口；不重复部署模型。
- [x] 读完 7.2.3「自动检测机制」；`_auto_detect_provider` 判断供应商，`_resolve_credentials` 解析该供应商的密钥和地址。本阶段不新增平台账号或部署本地模型。
- [x] 读完 7.3.1「Message 类」，理解 `role`、`content`、`timestamp`、`metadata` 与 `to_dict()` 的用途。
- [x] 完成 [message_demo.py](message_demo.py) 中的三个 TODO；`uv run python chapter07/check_message.py` 通过 5/5。先用普通类实现相同的核心行为，暂不安装 Pydantic。
- [x] 读完 7.3.2「Config 类」，理解默认值、`from_env()` 和环境变量的字符串转换。
- [x] 完成 [config_demo.py](config_demo.py) 中的两个 TODO；`uv run python chapter07/check_config.py` 通过 4/4。
- [x] 读完 7.3.3「Agent 抽象基类」，理解 `ABC`、`@abstractmethod`、`run()` 的约束，以及 `_history` 与 `Message` 的关系。
- [x] 完成 [agent_base_demo.py](agent_base_demo.py) 的四个 TODO；`uv run python chapter07/check_agent_base.py` 通过 6/6。练习用 `FakeLLM` 占位，不会调用模型。
- [x] 7.4.1 第一段：读完 `__init__` 和 `run()` 的无工具分支，能区分临时 `messages`（系统消息 → 旧历史 → 本轮输入）与持久 `_history`（模型回复后追加本轮输入和回复）。
- [x] 7.4.1 第二段：读懂 `_run_with_tools()` 中工具调用、继续循环、最终回答和最大迭代次数；`clean_response` 是移除工具标记后保留的模型文字。参数解析、流式输出和在线示例不逐行学习。
- [x] 7.4.2～7.4.4：抓住 ReAct 的单步格式与统一工具注册表、Reflection 的通用可定制提示词、Plan-and-Solve 的列表格式计划；重复实现与在线测试不抄写。
- [x] 7.4.5：了解原生 Function Calling 用结构化工具定义与参数调用，相比纯提示词约束通常更易可靠解析；暂不调用在线模型。
- [x] 读完 7.5.1「工具基类与注册机制设计」；工具自身执行任务，注册表负责注册、发现和按名称执行。
- [x] 完成 [tool_registry_demo.py](tool_registry_demo.py) 的六个 TODO；`uv run python chapter07/check_tool_registry.py` 通过 6/6。理解对象工具与普通函数两种注册方式。
- [x] 读完 7.5.2「自定义工具开发」：理解计算函数 → 注册 → 按名称执行；`_eval_node` 的 AST 递归只需掌握“判断节点类型 → 计算子节点 → 合成结果”，不要求独立实现。在线测试跳过。
- [x] 读完 7.5.3「多源搜索工具」：理解先确认后端可用，再用 `try/except` 在主源失败时降级到备用源；统一结果格式便于上层 Agent 不区分来源。SDK 细节和联网测试跳过。
- [x] 读完 7.5.4「工具系统的高级特性」：`add_step` 登记步骤，执行时通过 `context[output_key]` 传递结果；依赖前一步结果的任务顺序执行，互不依赖的耗时任务才考虑并发。不复制生产级实现。
- [x] 读完 7.6「本章小结」；本章主线阅读完成。

## 本章验收与取舍

- 离线检查：`check_message.py` 5/5、`check_config.py` 4/4、`check_agent_base.py` 6/6、`check_tool_registry.py` 6/6。
- 保留并亲手实现：消息、配置、抽象 Agent 与历史、对象工具和函数工具的注册与执行。
- 理解流程但不重复实现：ReAct、Reflection、Plan-and-Solve 的框架化；SimpleAgent 工具循环；多源搜索降级与工具链。
- 跳过：本地模型重复部署、新平台密钥申请、整套 HelloAgents 在线示例、搜索 SDK 联网测试和异步工具的完整实现。理由是已有相关练习，或当前阶段的开发收益不足以抵消环境与调用成本。
- 练习代码保留了部分 `return` 后不可达的 TODO 占位语句；它们不影响运行，本章不把清理它们作为验收或提交条件。

## Git 学习

本章用 `git status --short` 分辨已修改与未跟踪文件；`git diff --stat` 默认只统计已跟踪文件，因此看不到新建练习文件。把第七章文件加入暂存区后，用 `git diff --cached --stat` 核对提交范围；本章成果已提交并推送到 `origin/main`。后续章节仍只在你明确要求时由助手提交或推送。
