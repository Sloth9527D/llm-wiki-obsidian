---
description: 为当前工作区安装 Obsidian 相关 skills
allowed-tools: PowerShell(npx skills*)
---

为当前工作区安装以下 skills（workspace 级别，不加 `-g`）：

## 核心 Obsidian Skills

| Skill | 来源 | 用途 |
|-------|------|------|
| obsidian-markdown | kepano/obsidian-skills | Obsidian Flavored Markdown 语法规范 |
| obsidian-cli | kepano/obsidian-skills | 通过 CLI 操作 vault（读写、搜索、属性等） |
| obsidian-bases | kepano/obsidian-skills | 创建和编辑 .base 数据库视图文件 |

## 安装步骤

1. 运行以下命令安装所有核心 skills：

```powershell
npx skills add kepano/obsidian-skills@obsidian-markdown kepano/obsidian-skills@obsidian-cli kepano/obsidian-skills@obsidian-bases -y
```

2. 安装完成后运行 `/reload-skills` 使新 skill 生效。

3. 输出已安装的 skill 列表确认结果。

## 扩展安装（可选）

如果用户传入了额外的 skill 名称（通过参数），在核心 skills 安装完成后继续安装：

```powershell
npx skills add <额外的skill包名> -y
```

## 安装位置

Skills 安装到当前工作区的 `.agents/skills/`，并自动 symlink 到 `.claude/skills/`（Claude Code 读取路径）。
