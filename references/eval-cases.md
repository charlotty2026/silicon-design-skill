# 触发用例与可验证循环

> 用于验证 Skill 是否正确触发的测试用例。

## 触发用例

### 用例 1：基本排版请求

**用户输入**：
```
帮我把这篇 Markdown 排版成公众号文章：
# 标题
## 章节
正文内容
```

**预期行为**：触发 Skill，读取硅基极简组件库，输出排版好的 HTML。

### 用例 2：指定栏目和作者

**用户输入**：
```
帮我把这篇文章排版成公众号文章，栏目是避坑指南，作者是佛跳墙：
# 标题
正文内容
```

**预期行为**：触发 Skill，使用指定栏目和作者装配引言卡和签名落款。

### 用例 3：英文请求

**用户输入**：
```
Format this Markdown for WeChat article:
# Title
## Section
Content
```

**预期行为**：触发 Skill，输出中文排版的 HTML（因为公众号是中文场景）。

### 用例 4：指定主题

**用户输入**：
```
用硅基极简主题排版这篇文章：
# 标题
正文
```

**预期行为**：触发 Skill，使用 silicon-minimal 主题。

### 用例 5：不触发 — 纯写作请求

**用户输入**：
```
帮我写一篇关于 AI 的公众号文章
```

**预期行为**：不触发排版 Skill（因为用户是要求写作，不是排版）。

### 用例 6：不触发 — 非 HTML 格式

**用户输入**：
```
把这篇文章导出为 PDF
```

**预期行为**：不触发排版 Skill（因为用户要求 PDF，不是公众号 HTML）。

## 可验证循环

### 循环 1：禁用标签清零

1. 装配 HTML
2. 运行 `validate_gzh_html.py`
3. 如果发现 `<style>`/`<script>`/`<div>`/`<iframe>` → ERROR
4. 修复（替换为 `<section>`/`<span>` 或移除）→ 重新校验
5. 清零后通过

### 循环 2：span leaf 包裹率

1. 装配 HTML
2. 运行 `validate_gzh_html.py --check-span`
3. 如果包裹率 < 100% → WARNING（列出未包裹的文本节点）
4. 逐个添加 `<span leaf="">` 包裹 → 重新校验
5. 100% 后通过

### 循环 3：半角标点检测

1. 装配 HTML
2. 运行 `validate_gzh_html.py --check-punctuation`
3. 如果正文中发现半角标点 → WARNING（列出位置和建议替换）
4. 替换为全角 → 重新校验
5. 清零后通过

### 循环 4：签名落款完整性

1. 装配 HTML
2. 运行 `validate_gzh_html.py --check-signature`
3. 检查是否包含：栏目/日期/作者/标签/签名
4. 缺失 → ERROR
5. 补全 → 重新校验
6. 全部存在后通过

### 循环 5：互动话题存在性

1. 装配 HTML
2. 运行 `validate_gzh_html.py --check-interaction`
3. 如果未找到"互动话题"段落 → ERROR
4. 提示用户补充互动话题 → 添加到正文末尾
5. 重新校验
6. 存在后通过

### 循环 6：占位符清零

1. 装配 HTML
2. 运行 `validate_gzh_html.py --check-placeholder`
3. 如果发现 `[待补: xxx]` → ERROR
4. 提示用户补充内容 → 替换占位符
5. 重新校验
6. 清零后通过
