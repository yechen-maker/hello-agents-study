# Hello-Agents 逐章环境兼容表

检查基准：Datawhale `hello-agents` 主分支，提交 `4f7682c`（2026-09-04）。

## 总体策略

- 主学习环境固定为 Python 3.11，不使用旧 `DataClean` 项目的 Python 3.14。
- 第 1～4 章使用当前练习项目的基础环境。
- 从第 6 章开始，不同框架的依赖可能互相冲突，复杂案例使用独立子项目和独立 `uv.lock`。
- 教材指定旧版 `hello-agents` 时按章节锁定，不直接用最新 1.0.0 替换。
- Java 8 与 Python 学习无冲突，暂时保留。

## 逐章说明

| 章节 | 主要运行内容 | 版本与环境判断 | 我们的处理方式 |
|---|---|---|---|
| 1 | HTTP 天气、Tavily、OpenAI 兼容 API | Python 基础依赖已安装 | 当前环境直接学习 |
| 2 | ELIZA、正则表达式 | 只需 Python 标准库 | 当前环境直接学习 |
| 3 | N-gram、词向量、BPE、Transformer、Qwen | `numpy` 较轻；`torch/transformers` 较大 | 先做手写小实验，再单独添加模型依赖 |
| 4 | ReAct、Plan-and-Solve、Reflection | 需要 OpenAI 兼容 API、dotenv、SerpAPI | 复用基础环境，搜索依赖到本章再添加 |
| 5 | Coze、Dify、FastGPT、n8n | 主要是在线平台；本地部署常需 Docker | 选一个平台体验，不在本机同时部署四套 |
| 6 | AutoGen、AgentScope、CAMEL、LangGraph | 教材固定了不同框架版本，依赖面较大 | 每个框架使用独立 `uv` 子项目；重点学 LangGraph |
| 7 | 自建 Agent 框架 | 教材要求 Python ≥3.10、`hello-agents==0.1.1` | 新建第 7 章独立环境并精确锁定 0.1.1 |
| 8 | 记忆、RAG、Qdrant、Neo4j | 教材为 `hello-agents[all]==0.2.0`；外部数据库可选 | 先做本地最小版，再决定是否使用云数据库 |
| 9 | 上下文工程、NoteTool、TerminalTool | 教材固定 `hello-agents[all]==0.2.8` | 独立环境，避免覆盖第 8 章版本 |
| 10 | MCP、A2A、ANP | 教材写 `hello-agents[protocol]==0.2.2`，但后续包使用 `protocols`，存在命名差异 | 到本章核对该版本元数据并锁定可安装组合；Node 改用 LTS |
| 11 | SFT、GRPO、分布式训练 | `hello-agents[rl]==0.2.5`；完整训练对显存要求高 | 6GB 显存只做极小实验，完整训练改用云端 GPU 或只分析代码 |
| 12 | BFCL、GAIA、数据生成评估 | 正文要求 0.2.7，配套 README 却写 0.2.3；BFCL 还有 NumPy 冲突 | 单独环境，以实际示例导入和测试结果确定版本 |
| 13 | 旅行助手、FastAPI、Vue、MCP | 后端限制 `hello-agents[protocols]>=0.2.4,<=0.2.9` | Python 3.11 合适；前端改用 Node 24 LTS |
| 14 | Deep Research、FastAPI、Vue | 后端 `pyproject.toml` 固定 `hello-agents==0.2.9`，并原生提供 `uv.lock` | 直接使用案例自己的 `uv` 环境 |
| 15 | AI 小镇、FastAPI、Godot | 后端限制 `hello-agents>=0.2.4,<=0.2.9`，另需 Godot | 作为可选综合项目，不纳入第一轮必做项 |
| 16 | 毕业设计 | 技术栈由选题决定 | 优先复用第 7～10 章能力，控制项目规模 |

## 已发现的具体风险

### 1. 教材正文与配套代码并非总是同一依赖版本

第 12 章正文与代码 README 给出了不同的 `hello-agents` 版本。遇到此类情况不能靠猜，也不能只看“安装成功”；必须实际运行对应导入和最小示例。

### 2. 不应把所有章节依赖装进一个环境

AutoGen、AgentScope、CAMEL、LangGraph、训练与评估工具更新速度不同。全部装进同一个 `.venv` 很容易出现“A 库要求新版、B 库要求旧版”的冲突。`uv` 子项目可以把每章的依赖和锁文件隔离开。

### 3. Node.js 25 已结束支持

本机 Node 25.4.0 可以暂时保留，但在需要前端或 `npx` 的章节前，应改用 Node 24 LTS。不要等项目出现难以理解的构建错误后再换。

### 4. 本机不适合完整的大模型训练

RTX 3060 Laptop 只有 6GB 显存。Agent 应用、API 调用和小模型推理没有问题，但完整 SFT/GRPO 不是这一个月的主线目标。

### 5. API 密钥必须与代码分离

所有真实密钥只放 `.env`，示例文件只保留空值。日志、截图、Git 提交和聊天中都不要出现真实密钥。

