# 拾光 · Obsidian 知识库

基于 Obsidian 构建的个人 Wiki，配套自定义主题、CSS 片段与插件，打造沉浸式中文阅读写作体验。

---

## 前置依赖

### 字体

安装以下字体后，Obsidian 界面与编辑区才能正确显示。

| 字体 | 用途 | 下载 |
|---|---|---|
| **霞鹜文楷** | 界面字体 + 正文字体 | [GitHub · lxgw/LxgwWenKai](https://github.com/lxgw/LxgwWenKai/releases) |
| **CaskaydiaMono Nerd Font** | 等宽字体（代码块） | [Nerd Fonts · CascadiaMono](https://github.com/ryanoasis/nerd-fonts/releases) |

安装方式（Windows）：下载 `.ttf` / `.otf` 文件后右键 → **为所有用户安装**。

---

### Obsidian 主题

1. 打开 Obsidian → **设置 → 外观 → 主题**
2. 搜索并安装 **Minimal**
3. 基础配色选 **Moonstone**

---

## 社区插件安装

打开 **设置 → 社区插件 → 浏览**，搜索并安装以下插件：

| 插件 | 用途 |
|---|---|
| **Minimal Theme Settings** (`obsidian-style-settings`) | 主题细节调整 |
| **Linter** (`obsidian-linter`) | 自动格式化 Markdown |
| **Templater** (`templater-obsidian`) | 模板引擎，支持脚本 |
| **Advanced Tables** (`table-editor-obsidian`) | 表格快捷编辑 |
| **Terminal** (`terminal`) | 内嵌终端 |

---

## 自定义插件安装

### Image Click Zoom

双击图片进入全屏放大，`Ctrl + 滚轮` 继续缩放，拖拽平移，单击或 `Esc` 关闭。此插件未上架社区市场，需手动安装。

**步骤：**

1. 确认 Obsidian 已开启「社区插件」（关闭安全模式）
2. 将本库 `.obsidian/plugins/image-click-zoom/` 目录整体复制到你的 vault 的 `.obsidian/plugins/` 下
3. 重启 Obsidian，进入 **设置 → 社区插件**，找到 **Image Click Zoom** 并启用

---

## CSS 片段启用

进入 **设置 → 外观 → CSS 代码片段**，开启以下片段（已含于本库 `.obsidian/snippets/`）：

| 片段文件 | 效果 |
|---|---|
| `headline_beatify` | 标题分级配色（蓝灰渐变）+ 左侧色条指示器 |
| `tbl_beatify` | 表格美化：中性灰表头、斑马行、细边框 |
| `code_highlight` | 行内代码 chip 蓝灰配色 |
| `editor_beatify` | 编辑器排版优化 |
| `folder_beatify` | 文件树文件夹样式 |
| `floating_sidebar` | 悬浮侧边栏 |

---

## 目录结构

```
拾光/
├── raw/          # 原始来源文件（只读内容）
│   ├── assets/   # 图片与附件
│   └── clippings/# 插件捕获的网页剪藏
├── wiki/         # 提炼后的知识页面
│   ├── source/   # 来源摘要
│   ├── entities/ # 人物 / 地点 / 组织 / 工具
│   ├── concepts/ # 理论 / 框架 / 方法论
│   └── summaries/# 综合总结
├── moc/          # 导航与管理
│   ├── INDEX.base# 动态目录索引
│   ├── LOG.md    # 操作日志
│   └── TAGS.md   # 标签字典
└── templates/    # 标准模板
```
