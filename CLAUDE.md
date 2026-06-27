## CLAUDE.md

### 核心目标

你正在维护一个基于`Obsidian`长期演化的Markdown Wiki。目标是将碎片化的输入转化为高度互联、结构严谨且易于导航的知识图谱。

### 目录结构

| 目录         | 说明                                                                                                                          | 权限                    |
| ---------- | --------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| raw/       | 保存所有来源文件。<br>`raw/assets/` 存放图片和附件。<br> `raw/clippings/` 插件捕获的文件。                                                           | 内容只读<br>YAML元信息可按规则修改 |
| wiki/      | 读取来源文件后，保存提炼的知识。<br>`wiki/source/`来源摘要<br>`wiki/entities/`人物、地点、组织、工具<br>`wiki/concepts/`理论、框架、方法论<br>`wiki/summaries/`提炼总结 | 完全控制                  |
| templates/ | 标准模板                                                                                                                        | 只读                    |
| moc/       | 全局管理和地图层。<br>`INDEX.base`动态目录索引（按类型/标签查询所有wiki页面）<br>`LOG.md`操作日志<br>`TAGS.md`标签字典                                              | 完全控制                  |
| CLAUDE.md  | 定义规范、工作流程和标准                                                                                                                | 只读                    |

### 规范

- **obsidian-cli优先**：所有文件操作（创建、移动、重命名、删除、读取）优先使用`obsidian-cli` skill，确保Obsidian链接自动更新、vault状态一致
- **source**提炼来源文件的关键信息。关联相关页面
- **concept**页面包含定义、背景、核心思想等内容。关联wiki中相关页面
- **entity**简短摘要，关联wiki中相关页面
- **wiki**页面除专业英文或工具缩写，尽可能使用中文命名

### 模板与 Frontmatter

| 模板文件             | 适用类型    | 关键字段                                               |
| ---------------- | ------- | -------------------------------------------------- |
| templates/raw.md | raw 来源  | `create_time`, `ingest_time`, `status`             |
| templates/wiki.md | entity/concept | `create_time`, `update_time`, `source`, `tags`, `related` |
| templates/source.md | wiki/source | `ingested_time`, `source`, `tags`, `related`  |

`raw/` 文件 `status` 字段生命周期：`pend` → `ingested` / `skip`

### 自定义命令

| 命令                      | 对应SOP | 说明                                        |
| ----------------------- | ----- | ----------------------------------------- |
| `/ingest`               | SOP1  | 从raw提炼知识，创建/更新entity、concept               |
| `/query`                | SOP2  | 检索wiki回答问题，高价值结果可归档                        |
| `/lint`                 | SOP3  | 结构体检，修复孤儿、死链、tag异常                         |
| `/init-obsidian-skills` | —     | 为当前工作区安装所需的skills |

详细流程见各命令定义（`.claude/commands/`）。

### 工作流

1. SOP1：知识摄入(Ingest)，从raw材料中提炼关键发现、方法论、架构设计和批判性观点，创建或更新`entity/concept`页面，更新`LOG.md/TAGS.md`
2. SOP2：查询(Query)，以`moc/INDEX.base`为起点搜索wiki，回答问题，如有长期价值归档
3. SOP3：体检(Lint)，修复未引用的孤立页面 (Orphans)、陈旧的结论、缺少双向链接的术语、TAGS冗余

## fsadfasdfasfsa

### fsdafasdfasd

#### fdsafsafasd

##### fdsfasfasdfas

###### asdfs


## w1de1shijie1

### ##
###

### 我的