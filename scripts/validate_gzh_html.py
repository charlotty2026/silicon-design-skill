#!/usr/bin/env python3
"""
validate_gzh_html.py - 微信公众号 HTML 产物合规校验

检查最终生成的 HTML 是否符合公众号平台限制和硅基聊斋排版规范。

用法:
    python validate_gzh_html.py <html_file>
    python validate_gzh_html.py <html_file> --check-span
    python validate_gzh_html.py <html_file> --check-punctuation
    python validate_gzh_html.py <html_file> --check-signature
    python validate_gzh_html.py <html_file> --check-interaction
    python validate_gzh_html.py <html_file> --check-placeholder
"""

import re
import sys
import argparse
from pathlib import Path


# === 检查规则 ===

FORBIDDEN_TAGS = [
    (r'<style\b', '<style> 标签 - 公众号会过滤'),
    (r'<script\b', '<script> 标签 - 公众号会过滤'),
    (r'<div\b', '<div> 标签 - 公众号会过滤，改用 <section>'),
    (r'<iframe\b', '<iframe> 标签 - 公众号会过滤'),
    (r'<link\b', '<link> 标签 - 公众号会过滤'),
    (r'<meta\b', '<meta> 标签 - 公众号会过滤'),
    (r'<base\b', '<base> 标签 - 公众号会过滤'),
]

FORBIDDEN_ATTRS = [
    (r'\bclass\s*=', 'class= 属性 - 公众号会过滤'),
    (r'\bid\s*=', 'id= 属性 - 公众号会过滤'),
]

FORBIDDEN_CSS = [
    (r'position\s*:\s*(fixed|absolute|sticky)', 'position:fixed/absolute/sticky - 公众号不支持'),
    (r'float\s*:', 'float - 公众号不支持'),
    (r'display\s*:\s*grid', 'display:grid - 公众号不支持'),
    (r'var\s*\(--', 'CSS 变量 - 公众号不支持'),
    (r'white-space\s*:\s*pre(?![\w-])', 'white-space:pre - 导致大空白（pre-wrap 可以）'),
]

# 禁用 AI 味词汇
AI_FLAVOR_WORDS = [
    '综上所述', '值得注意的是', '至关重要', '不可或缺', '确保安全',
    '赋能', '全流程', '全方位', '深度融合', '显著提升',
    '核心竞争力', '战略高度', '此外', '提供全方位',
]

# 半角标点（正文中应为全角）
HALFWIDTH_PUNCT = [
    (r'(?<![\w:/@.-]),(?![\w:/@.-])', '半角逗号 , → 全角 ，'),
    (r'(?<![\w:/@.-])\.(?![\w:/@.-])(?=\s|$)', '半角句号 . → 全角 。'),
    (r'(?<![\w:/@.-]):(?![\w:/@.-])', '半角冒号 : → 全角 ：'),
    (r'(?<![\w:/@.-]);(?![\w:/@.-])', '半角分号 ; → 全角 ；'),
    (r'(?<![\w:/@.-])\?(?![\w:/@.-])', '半角问号 ? → 全角 ？'),
    (r'(?<![\w:/@.-])!(?![\w:/@.-])', '半角感叹号 ! → 全角 ！'),
]

# 必须的签名落款要素
SIGNATURE_REQUIRED = [
    (r'硅基聊斋', '品牌名"硅基聊斋"'),
    (r'栏目[：:]', '栏目信息'),
    (r'创作时间[：:]|日期[：:]', '日期信息'),
    (r'作者[：:]|本期作者[：:]', '作者信息'),
    (r'标签[：:]', '标签信息'),
]


def extract_text(html: str) -> str:
    """提取 HTML 中的纯文本内容（去除标签）"""
    # 先去除 <pre>/<code> 块内容（代码块内不检查标点）
    text_parts = re.split(r'<(?:pre|code)[^>]*>.*?</(?:pre|code)>', html, flags=re.DOTALL)
    no_tags = re.sub(r'<[^>]+>', '', '\n'.join(text_parts))
    return no_tags


def strip_code_blocks(html: str) -> str:
    """移除代码块内容，用于标点检查"""
    result = re.sub(r'<pre[^>]*>.*?</pre>', '', html, flags=re.DOTALL)
    result = re.sub(r'<code[^>]*>.*?</code>', '', result, flags=re.DOTALL)
    return result


def check_forbidden_tags(html: str) -> list:
    """检查禁用标签"""
    errors = []
    for pattern, desc in FORBIDDEN_TAGS:
        matches = list(re.finditer(pattern, html, re.IGNORECASE))
        if matches:
            for m in matches:
                pos = html[:m.start()].count('\n') + 1
                errors.append(f'[ERROR] 第{pos}行附近: {desc}')
    return errors


def check_forbidden_attrs(html: str) -> list:
    """检查禁用属性"""
    errors = []
    for pattern, desc in FORBIDDEN_ATTRS:
        matches = list(re.finditer(pattern, html, re.IGNORECASE))
        if matches:
            for m in matches[:3]:  # 只报前3个
                pos = html[:m.start()].count('\n') + 1
                errors.append(f'[ERROR] 第{pos}行附近: {desc}')
            if len(matches) > 3:
                errors.append(f'[ERROR] ...还有 {len(matches)-3} 处 {desc}')
    return errors


def check_forbidden_css(html: str) -> list:
    """检查禁用 CSS"""
    errors = []
    for pattern, desc in FORBIDDEN_CSS:
        matches = list(re.finditer(pattern, html, re.IGNORECASE))
        if matches:
            for m in matches[:3]:
                pos = html[:m.start()].count('\n') + 1
                errors.append(f'[ERROR] 第{pos}行附近: {desc}')
            if len(matches) > 3:
                errors.append(f'[ERROR] ...还有 {len(matches)-3} 处 {desc}')
    return errors


def check_span_wrap(html: str) -> list:
    """检查 span leaf 包裹率"""
    warnings = []
    # 找所有文本节点（标签之间的纯文本）
    # 简单方法：找 > 和 < 之间的非空白文本
    text_nodes = re.findall(r'>([^<]+)<', html)
    unwrapped = []
    for text in text_nodes:
        text = text.strip()
        if not text:
            continue
        # 检查是否已被 span leaf 包裹
        # 向前查找最近的开始标签
        idx = html.find(f'>{text}<')
        if idx == -1:
            continue
        before = html[:idx]
        # 检查最近的开标签是否是 span leaf
        last_open = before.rfind('<span')
        last_close = before.rfind('</span>')
        if last_open > last_close:
            # 在 span 内，检查是否有 leaf
            span_tag = html[last_open:idx+1]
            if 'leaf' not in span_tag:
                unwrapped.append(text[:30])
        else:
            # 不在 span 内
            # 检查是否是特殊标签（br, hr, img 等自闭合标签的属性值）
            if text not in ['', ' ']:
                unwrapped.append(text[:30])

    if unwrapped:
        warnings.append(f'[WARNING] {len(unwrapped)} 处文本未被 <span leaf=""> 包裹:')
        for t in unwrapped[:5]:
            warnings.append(f'  -> "{t}..."')
        if len(unwrapped) > 5:
            warnings.append(f'  -> ...还有 {len(unwrapped)-5} 处')
    return warnings


def check_punctuation(html: str) -> list:
    """检查半角标点"""
    warnings = []
    no_code = strip_code_blocks(html)
    text = re.sub(r'<[^>]+>', '', no_code)
    # 移除 URL 中的标点
    text = re.sub(r'https?://\S+', '', text)

    for pattern, desc in HALFWIDTH_PUNCT:
        matches = list(re.finditer(pattern, text))
        if matches:
            for m in matches[:5]:
                context_start = max(0, m.start() - 10)
                context_end = min(len(text), m.end() + 10)
                context = text[context_start:context_end].replace('\n', ' ')
                warnings.append(f'[WARNING] {desc} (上下文: "...{context}...")')
            if len(matches) > 5:
                warnings.append(f'[WARNING] ...还有 {len(matches)-5} 处 {desc}')
    return warnings


def check_signature(html: str) -> list:
    """检查签名落款完整性"""
    errors = []
    for pattern, desc in SIGNATURE_REQUIRED:
        if not re.search(pattern, html):
            errors.append(f'[ERROR] 签名落款缺少: {desc}')
    return errors


def check_interaction(html: str) -> list:
    """检查互动话题存在性"""
    errors = []
    if not re.search(r'互动话题', html):
        errors.append('[ERROR] 未找到"互动话题"段落 - 每篇公众号文章必须有互动话题')
    return errors


def check_placeholder(html: str) -> list:
    """检查占位符"""
    errors = []
    matches = list(re.finditer(r'\[待补[：:]?\s*[^\]]*\]', html))
    if matches:
        for m in matches:
            errors.append(f'[ERROR] 发现未替换的占位符: {m.group()}')
    return errors


def check_ai_flavor(html: str) -> list:
    """检查 AI 味词汇"""
    warnings = []
    text = re.sub(r'<[^>]+>', '', html)
    for word in AI_FLAVOR_WORDS:
        if word in text:
            count = text.count(word)
            warnings.append(f'[WARNING] AI味词汇 "{word}" 出现 {count} 次 - 建议替换为更自然的表述')
    return warnings


def main():
    parser = argparse.ArgumentParser(description='微信公众号 HTML 产物校验')
    parser.add_argument('html_file', help='待校验的 HTML 文件路径')
    parser.add_argument('--check-span', action='store_true', help='仅检查 span leaf 包裹率')
    parser.add_argument('--check-punctuation', action='store_true', help='仅检查半角标点')
    parser.add_argument('--check-signature', action='store_true', help='仅检查签名落款')
    parser.add_argument('--check-interaction', action='store_true', help='仅检查互动话题')
    parser.add_argument('--check-placeholder', action='store_true', help='仅检查占位符')
    args = parser.parse_args()

    filepath = Path(args.html_file)
    if not filepath.exists():
        print(f'[FATAL] 文件不存在: {filepath}')
        sys.exit(1)

    html = filepath.read_text(encoding='utf-8')

    all_errors = []
    all_warnings = []

    if args.check_span:
        all_warnings.extend(check_span_wrap(html))
    elif args.check_punctuation:
        all_warnings.extend(check_punctuation(html))
    elif args.check_signature:
        all_errors.extend(check_signature(html))
    elif args.check_interaction:
        all_errors.extend(check_interaction(html))
    elif args.check_placeholder:
        all_errors.extend(check_placeholder(html))
    else:
        # 全量检查
        all_errors.extend(check_forbidden_tags(html))
        all_errors.extend(check_forbidden_attrs(html))
        all_errors.extend(check_forbidden_css(html))
        all_errors.extend(check_signature(html))
        all_errors.extend(check_interaction(html))
        all_errors.extend(check_placeholder(html))
        all_warnings.extend(check_span_wrap(html))
        all_warnings.extend(check_punctuation(html))
        all_warnings.extend(check_ai_flavor(html))

    # 输出结果
    print('=' * 60)
    print(f'校验文件: {filepath.name}')
    print('=' * 60)

    if all_errors:
        print(f'\n❌ ERROR ({len(all_errors)}):')
        for e in all_errors:
            print(f'  {e}')

    if all_warnings:
        print(f'\n⚠️  WARNING ({len(all_warnings)}):')
        for w in all_warnings:
            print(f'  {w}')

    if not all_errors and not all_warnings:
        print('\n✅ 全部通过，无 ERROR，无 WARNING')

    print('\n' + '=' * 60)
    if all_errors:
        print(f'结果: FAIL ({len(all_errors)} ERROR, {len(all_warnings)} WARNING)')
        sys.exit(1)
    else:
        print(f'结果: PASS ({len(all_warnings)} WARNING)')
        sys.exit(0)


if __name__ == '__main__':
    main()
