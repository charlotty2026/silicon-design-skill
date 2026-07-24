#!/usr/bin/env python3
"""
component_lint.py - 组件库源头检查

扫描组件库 Markdown 文件中的 HTML 组件，检查是否包含公众号禁用项。

用法:
    python component_lint.py references/
    python component_lint.py references/theme-silicon-minimal.md
"""

import re
import sys
from pathlib import Path


FORBIDDEN_IN_COMPONENTS = [
    (r'<style\b', '<style> 标签'),
    (r'<script\b', '<script> 标签'),
    (r'<div\b', '<div> 标签 (应使用 <section>)'),
    (r'<iframe\b', '<iframe> 标签'),
    (r'<link\b', '<link> 标签'),
    (r'<meta\b', '<meta> 标签'),
    (r'\bclass\s*=', 'class= 属性'),
    (r'\bid\s*=', 'id= 属性'),
    (r'position\s*:\s*(fixed|absolute|sticky)', 'position:fixed/absolute/sticky'),
    (r'float\s*:', 'float'),
    (r'display\s*:\s*grid', 'display:grid'),
    (r'var\s*\(--', 'CSS 变量'),
]

# 代码块中的 HTML 示例不检查（它们在 ```html ... ``` 内）
CODE_BLOCK_PATTERN = r'```(?:html)?\s*\n(.*?)```'


def extract_components_from_md(md_text: str) -> list:
    """从 Markdown 文件中提取 HTML 代码块"""
    blocks = re.findall(CODE_BLOCK_PATTERN, md_text, re.DOTALL)
    # 只保留包含 HTML 标签的块
    html_blocks = [b for b in blocks if re.search(r'<\w+', b)]
    return html_blocks


def check_component(html: str, source_label: str) -> list:
    """检查单个组件 HTML"""
    errors = []
    for pattern, desc in FORBIDDEN_IN_COMPONENTS:
        matches = list(re.finditer(pattern, html, re.IGNORECASE))
        if matches:
            for m in matches[:3]:
                line_num = html[:m.start()].count('\n') + 1
                errors.append(f'[ERROR] {source_label} 第{line_num}行: {desc}')
            if len(matches) > 3:
                errors.append(f'[ERROR] {source_label}: ...还有 {len(matches)-3} 处 {desc}')
    return errors


def check_span_leaf(html: str, source_label: str) -> list:
    """检查组件中的文本节点是否用 span leaf 包裹"""
    warnings = []
    text_nodes = re.findall(r'>([^<]+)<', html)
    unwrapped = []
    for text in text_nodes:
        text = text.strip()
        if not text:
            continue
        # 检查是否在 span leaf 内
        idx = html.find(f'>{text}<')
        if idx == -1:
            continue
        before = html[:idx]
        last_open = before.rfind('<span')
        last_close = before.rfind('</span>')
        if last_open > last_close:
            span_tag = html[last_open:idx+1]
            if 'leaf' not in span_tag:
                unwrapped.append(text[:30])
        else:
            if text and text not in ['\n', ' ']:
                unwrapped.append(text[:30])

    if unwrapped:
        warnings.append(f'[WARNING] {source_label}: {len(unwrapped)} 处文本未用 <span leaf=""> 包裹')
        for t in unwrapped[:3]:
            warnings.append(f'  -> "{t}..."')
    return warnings


def scan_file(filepath: Path) -> tuple:
    """扫描单个文件"""
    md_text = filepath.read_text(encoding='utf-8')
    components = extract_components_from_md(md_text)
    all_errors = []
    all_warnings = []

    for i, comp in enumerate(components, 1):
        label = f'{filepath.name} (组件#{i})'
        all_errors.extend(check_component(comp, label))
        all_warnings.extend(check_span_leaf(comp, label))

    return all_errors, all_warnings


def main():
    if len(sys.argv) < 2:
        print('用法: python component_lint.py <文件或目录>')
        sys.exit(1)

    target = Path(sys.argv[1])
    if not target.exists():
        print(f'[FATAL] 路径不存在: {target}')
        sys.exit(1)

    files = []
    if target.is_dir():
        files = sorted(target.glob('**/*.md'))
    else:
        files = [target]

    if not files:
        print('[FATAL] 未找到 Markdown 文件')
        sys.exit(1)

    total_errors = 0
    total_warnings = 0

    for f in files:
        errors, warnings = scan_file(f)
        if errors or warnings:
            print(f'\n📄 {f}')
            for e in errors:
                print(f'  {e}')
            for w in warnings:
                print(f'  {w}')
            total_errors += len(errors)
            total_warnings += len(warnings)
        else:
            print(f'✅ {f.name} - 通过')

    print('\n' + '=' * 60)
    if total_errors:
        print(f'结果: FAIL ({total_errors} ERROR, {total_warnings} WARNING)')
        sys.exit(1)
    else:
        print(f'结果: PASS ({total_warnings} WARNING)')
        sys.exit(0)


if __name__ == '__main__':
    main()
