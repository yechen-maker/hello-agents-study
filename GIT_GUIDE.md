# Git 学习指南

本项目同时用于练习 Git 和 GitHub。Git 操作会穿插在每章的小成果之间，而不是等所有内容完成后统一提交。

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
