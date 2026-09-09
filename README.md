# Hello-Agents Study 🚀

一个面向开发初学者的 AI Agent 动手学习仓库。

本仓库以 Datawhale 的 [Hello-Agents](https://github.com/datawhalechina/hello-agents) 教程为主线，把每章内容拆成“阅读 → 小练习 → 编码 → 调试 → 提交”的学习闭环。代码会保留从不完整、报错到逐步跑通的真实学习过程。

## 学习路线

| 章节 | 主题 | 状态 | 学习入口 |
| --- | --- | --- | --- |
| 第 1 章 | 初识智能体与最小 Agent 循环 | ✅ 已完成 | [进入](chapter01/README.md) |
| 第 2 章 | 智能体发展史与规则聊天机器人 | 🚧 学习中 | [进入](chapter02/README.md) |

后续章节将随着学习进度持续更新。

## 这个仓库有什么

```text
hello-agents-study/
├── chapter01/                   # Python 热身、工具调用、首个 Agent
├── chapter02/                   # 符号主义、ELIZA 与配套练习
├── LEARNING_PLAN.md             # 一个月学习计划
├── PROGRESS.md                  # 当前学习进度
├── ENVIRONMENT_COMPATIBILITY.md # 本地环境与版本说明
├── GIT_GUIDE.md                 # Git 学习与提交约定
├── pyproject.toml               # Python 项目配置
└── uv.lock                      # 可复现的依赖版本
```

## 快速开始

项目使用 Python 3.11 和 [uv](https://docs.astral.sh/uv/) 管理环境与依赖。

```powershell
git clone https://github.com/yechen-maker/hello-agents-study.git
cd hello-agents-study
uv sync
```

运行某一章的程序或检查器，例如：

```powershell
uv run python chapter01/check_warmup.py
uv run python chapter01/check_manual_agent.py
```

## 学习方法

- 先理解目标，再亲手写出最小版本。
- 报错时先看错误类型、文件和行号。
- 教程与短练习穿插进行，每章 README 都标明暂停点。
- 每完成一个小成果就验证、提交，让 Git 历史成为学习轨迹。

## 学习资料

- [Hello-Agents 在线教程](https://hello-agents.datawhale.cc/)
- [Hello-Agents GitHub 仓库](https://github.com/datawhalechina/hello-agents)

> 这是一个持续更新的学习仓库，欢迎一起从代码基础走向能够独立构建 Agent。
