#!/usr/bin/env python3
import os
import re
import argparse
from pathlib import Path
from datetime import datetime

# ==========================================
# 配置区
# ==========================================
WIKI_ROOT = Path(__file__).parent.parent
MOC_DIR = WIKI_ROOT / "moc"
WIKI_DIR = WIKI_ROOT / "wiki"
TAGS_FILE = MOC_DIR / "tags.md"

# 正则表达式
WIKILINK_PATTERN = re.compile(r"\[\[(.*?)\]\]")
FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
TAG_PATTERN = re.compile(r"tags:\s*\[(.*?)\]")


class WikiLinter:
    def __init__(self):
        self.all_files = set()
        self.valid_tags = set()
        self.issues = {
            "dead_links": [],
            "missing_yaml": [],
            "invalid_tags": [],
            "orphans": [],
        }
        self.link_graph = {}  # {source_file: [target_files]}

    def load_context(self):
        """加载全局状态：所有有效文件和允许的标签"""
        # 1. 扫描所有 md 文件作为有效链接目标
        for root, _, files in os.walk(WIKI_ROOT):
            if ".obsidian" in root or "cache" in root or "assets" in root:
                continue
            for file in files:
                if file.endswith(".md"):
                    self.all_files.add(Path(root) / file)
                    self.all_files.add(file)  # 允许不带路径的短链接匹配
                    self.all_files.add(file[:-3])  # 允许去掉 .md 的链接名匹配

        # 2. 从 moc/tags.md 加载标准标签字典
        if TAGS_FILE.exists():
            with open(TAGS_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                # 假设 tags.md 包含类似 - #llm 或 #c++ 的列表
                self.valid_tags = set(re.findall(r"#([a-zA-Z0-9_\-]+)", content))

    def lint_file(self, filepath: Path, auto_fix=False):
        """对单个文件进行体检"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return

        filename = filepath.name
        self.link_graph[filename] = []

        # 1. 检查 Frontmatter
        fm_match = FRONTMATTER_PATTERN.search(content)
        if not fm_match:
            self.issues["missing_yaml"].append(filepath)
            if auto_fix:
                self._fix_missing_yaml(filepath, content)
        else:
            # 检查非法标签
            tag_match = TAG_PATTERN.search(fm_match.group(1))
            if tag_match and self.valid_tags:
                tags = [t.strip().strip("\"'") for t in tag_match.group(1).split(",")]
                for tag in tags:
                    if tag and tag not in self.valid_tags:
                        self.issues["invalid_tags"].append((filepath, tag))

        # 2. 检查死链 (Dead Links)
        links = WIKILINK_PATTERN.findall(content)
        for link in links:
            # 处理带别名的链接，如 [[Page Name|Alias]]
            target = link.split("|")[0].strip()
            self.link_graph[filename].append(target)

            if target not in self.all_files:
                self.issues["dead_links"].append((filepath, target))

    def find_orphans(self):
        """查找孤立页面 (Orphans)"""
        all_targets = set()
        for targets in self.link_graph.values():
            all_targets.update(targets)

        for file in self.all_files:
            if isinstance(file, str):  # 跳过短名称，只检查完整 Path 对象
                continue
            # 排查：不在 MOC，不在 Raw，且没有任何文件指向它的 .md
            if (
                "wiki" in str(file)
                and file.name[:-3] not in all_targets
                and file.name != "index.md"
            ):
                self.issues["orphans"].append(file)

    def _fix_missing_yaml(self, filepath: Path, original_content: str):
        """自动修复：注入默认 YAML 头"""
        today = datetime.now().strftime("%Y-%m-%d")
        yaml_template = f"---\naliases: []\ntags: []\ndate_created: {today}\n---\n\n"
        new_content = yaml_template + original_content
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"🔧 Fixed: Added empty YAML frontmatter to {filepath.name}")

    def run(self, check_only=True):
        """执行全库体检"""
        print("🔍 Starting LLM-Wiki Lint Pass...\n")
        self.load_context()

        # 遍历 wiki 目录
        for root, _, files in os.walk(WIKI_DIR):
            for file in files:
                if file.endswith(".md"):
                    self.lint_file(Path(root) / file, auto_fix=not check_only)

        self.find_orphans()
        self.print_report()

    def print_report(self):
        """打印诊断报告"""
        print("-" * 40)
        print("📊 Triage Report")
        print("-" * 40)

        if self.issues["dead_links"]:
            print(f"\n❌ Dead Links Found ({len(self.issues['dead_links'])}):")
            for filepath, target in self.issues["dead_links"][:10]:
                print(f"  - [{filepath.name}] points to non-existent: [[{target}]]")
            if len(self.issues["dead_links"]) > 10:
                print("  ... and more")

        if self.issues["missing_yaml"]:
            print(f"\n⚠️ Missing Frontmatter ({len(self.issues['missing_yaml'])}):")
            for filepath in self.issues["missing_yaml"][:5]:
                print(f"  - {filepath.name}")

        if self.issues["invalid_tags"]:
            print(f"\n🏷️ Invalid Tags Found ({len(self.issues['invalid_tags'])}):")
            for filepath, tag in self.issues["invalid_tags"][:5]:
                print(f"  - [{filepath.name}] uses unregistered tag: #{tag}")

        if self.issues["orphans"]:
            print(
                f"\n🏝️ Orphan Pages (No inbound links) ({len(self.issues['orphans'])}):"
            )
            for filepath in self.issues["orphans"][:5]:
                print(f"  - {filepath.name}")

        total_issues = sum(len(v) for v in self.issues.values())
        if total_issues == 0:
            print("\n✅ All clean! The wiki topology is healthy.")
        else:
            print(f"\nTotal issues found: {total_issues}")
            print(
                "Tip: Run `python scripts/lint.py --fix` to auto-repair formatting issues."
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM-Wiki Consistency Linter")
    parser.add_argument(
        "--check",
        action="store_true",
        default=True,
        help="Run in read-only mode (default)",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix formatting issues (like missing YAML)",
    )
    args = parser.parse_args()

    linter = WikiLinter()
    # 如果指定了 --fix，则关闭 check_only 模式
    linter.run(check_only=not args.fix)
