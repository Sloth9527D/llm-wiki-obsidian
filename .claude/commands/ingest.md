---
description: 从raw材料中提起关键发现、方法论、架构设计和批判性观点，创建或更新`entity/concept`页面，更新`LOG.md/TAGS.md`
allowed-tools: Bash(obsidian*)
---

## 核心原则

1. 主动触发`obsidian-cli` skill并优先使用进行操作。仅在`obsidian-cli`无法完成时（如原始文件不在 vault 内、内容过长 CLI 参数装不下等），才回退到文件系统工具（Read、Write、Edit、Glob）。

2. 编辑文件时主动触发`obsidian-markdown`技能，确保生成的.md文件符合`Obsidian Flavored Markdown`规范（wikilink、callout、frontmatter等）

## 约束

### 1. wiki文件规则

| 类型    | 生成目录      | YAML模板            | 关联规则              | tag个数 |
| ------- | ------------- | ------------------- | --------------------- | ------- |
| source  | wiki/source   | templates/source.md | 可关联raw和wiki内链接 | 小于6   |
| entity  | wiki/entities | templates/wiki.md   | 仅可关联wiki内链接    | 小于3   |
| concept | wiki/concepts | templates/wiki.md   | 仅可关联wiki内链接    | 小于3   |

### 2. 操作日志格式

```markdown
## [YYYY-MM-DD] ingest | {操作的内容概括}

- 提炼了N个来源
  - raw名称1：路径
  - entity名称...：路径
  - raw名称N：路径
- 创建/更新了N个entities
  - entity名称1：路径
  - entity名称...：路径
  - entity名称N：路径
- 创建/更新了N个concepts
  - concept名称1：路径
  - concept名称...：路径
  - concept名称N：路径
- 新创建N个tag
```

### 3. 其他

- 生成的 wiki 页面至少包含一个内部 wikilink
- 批量操作时，每个文件处理完再处理下一个，不要跳过

## 流程

> 待提取的文件: !`obsidian search query='path:raw -path:raw/asset -path:raw/excalidraw -[state:ingested] -[state:skip]'`

1. 列出待处理文件列表  
   1.1 待提取的文件为空,提示用户"没有待摄入的文件"。流程结束  
   1.2 待提取的文件整理为表格(编号/相对路径)展示给用户
2. 使用 `AskUserQuestion` 工具让用户选择，支持以下几种选择方式
   - 输入单个序号
   - 输入多个序号,序号用 `/` 分隔
   - 文件名称模糊匹配
   - 正则过滤
3. 选择后，逐个读取目标文件`obsidian read file="file-name"`，分析提炼一下内容
   - 核心要点：3-8条
   - 实体(entities): 人物、地点、组织、工具
   - 概念(concepts): 理论、框架、方法论
   - 核心tags
4. 创建`wiki/source/页面`obsidian create name="filename" content="Frontmatter\n正文"`(内容含标准 frontmatter + 简短摘要 + wikilink 关联)
5. 更新raw文件frontmatter
   - 更新提取时间`obsidian property:set name="ingest_time" value="YYYY-MM-DD" file="raw/filename.md"`
   - 状态标记为已提取`obsidian property:set name="status" value="ingested"`
6. 更新entity/concept页面  
   6.1 查询页面是否存在`obsidian search query="entity/concept name"`  
   6.2 存在则使用 `obsidian property:set` 在现有页面追加 `related`对于的链接,并看是否需要调整已有内容  
   6.3不存在使用 `obsidian create`创建页面（含标准 frontmatter + 简短摘要 + wikilink 关联）
7. 更新操作日志到moc/LOG.md
8. 更新moc/TAGS
   - tag已存在，则跳过
   - tag分析有相似询问用户处理策略，然后按用户反馈进行合并或其他处理
   - 不存在则新增
