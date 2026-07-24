# 格式归一化

> 将非标准 Markdown 输入归一化为标准 Markdown，再进入排版流程。

## 什么时候使用

当输入不是标准 Markdown 时：
- Word 文档（.docx）
- 纯文本（.txt）
- PDF 提取的文本
- 网页复制的文本（带大量空行和缩进）

## Word 文档 → Markdown

### 方法

使用 python-docx 读取 .docx 文件：

```python
from docx import Document

def docx_to_markdown(filepath):
    doc = Document(filepath)
    lines = []
    for para in doc.paragraphs:
        style = para.style.name
        text = para.text.strip()
        if not text:
            lines.append("")
            continue
        if style.startswith("Heading 1"):
            lines.append(f"# {text}")
        elif style.startswith("Heading 2"):
            lines.append(f"## {text}")
        elif style.startswith("Heading 3"):
            lines.append(f"### {text}")
        elif style.startswith("Heading 4"):
            lines.append(f"#### {text}")
        elif style.startswith("List"):
            lines.append(f"- {text}")
        else:
            lines.append(text)
    return "\n".join(lines)
```

### 注意事项

- Word 中的加粗/斜体在转换后会丢失，需要手动检查
- 表格需要单独处理（python-docx 的 table API）
- 图片需要提取并保存为文件
- 如果 Word 中使用了多级编号，需要在 Markdown 中手动重建

## 纯文本 → Markdown

### 规则

1. **标题推断**：
   - 独占一行、全句无标点、字数≤20 → 推断为标题
   - 前面有空行且后面跟正文 → 推断为 H2
   - 文件第一个推断的标题 → H1

2. **段落分割**：
   - 连续的非空行合并为一段
   - 空行作为段落分隔

3. **列表推断**：
   - 以 `1.`/`2.`/`- `/`* ` 开头 → 列表项
   - 以 `第一步`/`第二步` 开头 → 有序列表

4. **代码块推断**：
   - 连续行以 4 空格或 Tab 开头 → 代码块
   - 包含 ` ``` ` 标记 → 直接识别

5. **清理**：
   - 去除多余空行（连续 2+ 空行合并为 1）
   - 去除行首行尾空白
   - 统一换行符为 `\n`

## PDF 提取文本 → Markdown

### 方法

使用 `baidu-document-parser` 技能或 `markdown-converter` 技能将 PDF 转为 Markdown。

### 注意事项

- PDF 提取的文本常有断行错误（句中被换行），需要修复
- PDF 中的表格可能丢失结构
- PDF 中的图片需要单独提取

## 网页复制文本 → Markdown

### 清理规则

1. 去除 HTML 标签残留
2. 修复编码问题（乱码/全角半角混乱）
3. 去除网页特有元素（导航/广告/页脚）
4. 重建段落结构

## 归一化后的检查清单

归一化完成后，检查以下内容：

- [ ] 文章有且仅有 1 个 H1 标题
- [ ] H2/H3 层级正确（不跳级）
- [ ] 没有多余空行（连续 2+ 空行）
- [ ] 代码块有正确的 ` ``` ` 标记
- [ ] 列表格式正确
- [ ] 没有残留的 HTML 标签
- [ ] 全角/半角标点使用正确
