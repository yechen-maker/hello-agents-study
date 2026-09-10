# Git 学习指南

本项目同时用于练习 Git 和 GitHub。Git 操作会穿插在每章的小成果之间，而不是等所有内容完成后统一提交。

## 教学约定

每章结束安排一次约 10～20 分钟的 Git 实操课，并使用本章真实产生的代码和文档练习。

- 不只提供可复制的命令；执行前先说明命令读取或改变了什么。
- 学习者先判断文件当前状态、选择应该使用的命令，再亲手输入。
- 执行后阅读终端输出，确认结果是否符合预期。
- 每次只引入少量重要概念，并在后续章节重复使用。
- 危险或容易丢失修改的命令不作为初学阶段的默认方案。

## 递进学习路线

### 第 2 章：一次提交是怎样产生的

- 工作区、暂存区、本地仓库、远程仓库的区别。
- `git status` 中 `untracked`、`modified`、`staged` 的含义。
- 使用 `git diff` 和 `git diff --staged` 检查改动。
- 有选择地 `git add`，再创建一个内容单一的小提交。

### 第 3 章：读懂项目历史

- 使用 `git log --oneline` 阅读提交历史。
- 使用 `git show` 查看某一次提交。
- 比较两个版本之间发生了什么变化。
- 理解提交编号以及为什么它会变化。

### 第 4 章：使用分支安全地做实验

- 理解分支不是“复制一份项目”，而是指向提交的指针。
- 使用 `git switch -c` 创建实验分支。
- 在分支上开发并提交，再合并回 `main`。
- 认识合并冲突，并亲手解决一次简单冲突。

### 第 5 章：理解本地与远程同步

- 区分 `fetch`、`pull` 和 `push`。
- 理解 `origin/main` 与本地 `main`。
- 判断领先、落后和分叉状态。
- 在同步前先检查状态，避免覆盖尚未保存的工作。

### 第 6 章：安全地撤销错误

- 撤销尚未暂存的修改。
- 把文件移出暂存区但保留代码。
- 使用 `commit --amend` 修正最近一次未共享的提交。
- 使用 `git revert` 撤销已经共享的提交。
- 理解为什么不能不加判断地使用 `reset --hard`。

### 后续章节：GitHub 协作

- 使用 Issue 记录任务和问题。
- 通过分支与 Pull Request 展示一项完整改动。
- 阅读代码差异并完成一次自我审查。
- 使用标签或 Release 标记阶段性成果。

## 一个完整的小循环

```text
完成一小段代码或笔记
        ↓
git status 查看发生了什么变化
        ↓
git diff 检查具体改动
        ↓
运行程序或检查器验证
        ↓
git add 选择要提交的文件
        ↓
git commit 保存一个有意义的版本
        ↓
git push 同步到 GitHub
```

## 常用命令

```powershell
# 查看仓库状态
git status

# 查看尚未暂存的修改
git diff

# 暂存一个明确的文件
git add 文件路径

# 查看已经暂存、即将提交的修改
git diff --staged

# 创建一次提交
git commit -m "说明这次完成了什么"

# 查看简洁的提交历史
git log --oneline

# 将本地提交同步到 GitHub
git push
```

学习初期不盲目使用 `git add .`。先用 `git status` 看清变化，再明确选择准备提交的文件，以便理解工作区和暂存区。

## 三个重要区域

- 工作区：电脑中正在编辑的文件。
- 暂存区：通过 `git add` 选中、准备放进下一次提交的内容。
- 本地仓库：通过 `git commit` 保存下来的历史版本。

`git push` 会把本地仓库中的提交同步到 GitHub 远程仓库。

## 提交信息约定

提交信息要描述一个完整的小成果，例如：

```text
docs: add chapter 2 learning plan
feat: implement rule-based ELIZA
feat: add ELIZA study rules
test: add ELIZA response checks
fix: correct pronoun replacement
```

常用前缀：

- `docs`：文档或学习笔记。
- `feat`：新增功能。
- `test`：新增或修改检查代码。
- `fix`：修复错误。
- `chore`：项目配置、依赖等杂项工作。
