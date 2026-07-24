# silicon-design-skill - 公众号排版 Skill

## 什么时候触发

当用户请求涉及以下场景时触发本 Skill：

- "排版成公众号文章"、"排成公众号格式"
- "帮我排版这篇 Markdown"
- "转换成微信文章 HTML"
- "格式化公众号文章"
- "WeChat article formatting"
- 任何将 Markdown/纯文本转换为微信公众号编辑器可直接粘贴的 HTML 的请求

不触发：用户只是写文章内容不涉及排版格式化、用户要求导出 PDF/Word 等非 HTML 格式。

## 核心理念

**约束而非自由**：预设「硅基极简」色板和 20 个固定组件，Agent 的任务是"装配"而非"创作"。组件库里的样式是经过公众号实战验证的，直接用，不现场发挥。

**样式粘贴不掉**：公众号编辑器会过滤 `<style>`、`<script>`、`<div>`、`class=`、`id=` 等。所有样式必须用 inline style，所有文字节点用 `<span leaf="">` 包裹。

**质量靠脚本不靠自觉**：装配完必须跑 `scripts/validate_gzh_html.py`，ERROR 清零才交付。组件库自身也要定期跑 `scripts/component_lint.py` 检查反模式。

## 工作流

```
输入：Markdown 文章 + 可选参数（主题/栏目/作者/标签）
  │
  ├─ Step 0: 确认参数
  │   • 主题：默认「硅基极简」，可选其他已安装主题
  │   • 栏目：专项攻略/避坑指南/开源项目/他山石/江湖夜话/宗门实录
  │   • 作者：硅基聊斋主笔/硅基聊斋编辑部/硅基聊斋技术组/硅基聊斋观察员/硅基聊斋读者之友
  │   • 标签：#硅基聊斋 必须第一个，总标签 3-6 个
  │
  ├─ Step 1: 读取主题
  │   • 读 references/theme-index.md 确认可用主题
  │   • 读 references/theme-silicon-minimal.md 获取组件定义
  │   • 读 references/common-components.md 获取通用增量组件
  │
  ├─ Step 2: 格式归一化（如需要）
  │   • 如果输入不是标准 Markdown，先按 references/format-normalize.md 归一化
  │   • docx → Markdown：用 python-docx 提取文本和结构
  │   • 纯文本 → Markdown：按段落和缩进推断标题层级
  │
  ├─ Step 3: 解析 Markdown 结构
  │   • 识别：H1/H2/H3 标题、正文段落、加粗、引用块、代码块、图片、列表、分割线
  │   • 识别特殊结构：文章头部引言卡、文末互动话题、文末落款区
  │   • 推断文章类型（如用户未指定）：代码块多→专项攻略/开源项目，引用多→避坑指南/他山石
  │
  ├─ Step 4: 装配 HTML
  │   • 用组件库中的真实 HTML 组件替换 Markdown 元素
  │   • 落实章节编号：一、→（一）→ 1、→ 1.1
  │   • 落实全角标点：正文中的 ,.:;?! → ，。：；？！
  │   • 落实关键词下划线：每段提取 1-3 个关键词加下划线
  │   • 装配引言卡（栏目+作者+日期）
  │   • 装配签名落款（从签名池随机匹配 1 条）
  │   • 装配互动话题（如 Markdown 中已有则保留，否则提示用户补充）
  │   • 装配标签列表
  │
  ├─ Step 5: 校验
  │   • 运行 python scripts/validate_gzh_html.py <html_file>
  │   • ERROR 必须清零；WARNING 逐条确认
  │   • 如果有 ERROR：修复后重新校验，最多 3 轮
  │
  └─ 输出
      • 干净的正文 HTML（可直接粘贴到公众号编辑器）
      • 在对话中展示预览
```

## 组件装配规则

### 必须包含的结构（每篇文章）

1. **引言卡**（info-card）：文章头部，包含栏目、作者、日期
2. **正文**：由组件库中的组件装配
3. **互动话题**（interaction-topic）：正文末尾，每篇必有
4. **签名落款**（signature-block）：文末固定结构

### 章节编号规则

```
H2 → 一、二、三、
H3 → （一）（二）（三）
H4 → 1、2、3、
H5 → 1.1、1.2、1.3
```

### 全角标点规则

正文中的标点必须使用全角：
- `,` → `，`
- `.` → `。`（句末）
- `:` → `：`
- `;` → `；`
- `?` → `？`
- `!` → `！`
- `()` → `（）`

例外：代码块内、URL 中、英文专有名词中保持半角。

### 关键词下划线规则

- 每段正文提取 1-3 个关键词
- 关键词用 `<span style="border-bottom:1px solid #a0c4e8;">` 加下划线
- 关键词选择标准：核心概念、技术术语、关键数字
- 一段内不超过 2 种高亮方式（加粗 + 下划线）

### 签名匹配规则

从签名池中按署名角色匹配，每篇随机选 1 条：
- 如果用户指定了署名角色，用该角色的签名池
- 如果未指定，根据文章类型推断：
  - 专项攻略/开源项目 → 硅基聊斋主笔
  - 宗门实录 → 硅基聊斋编辑部
  - 他山石/江湖夜话 → 硅基聊斋观察员或硅基聊斋主笔
  - 避坑指南 → 硅基聊斋主笔

### 标签规则

- `#硅基聊斋` 必须是第一个标签
- 总标签 3-6 个
- 标签之间用 ` | ` 分隔
- 标签来源：栏目名 + 文章核心关键词

## 文章类型配方

| 文章类型 | 必用组件 | 可选组件 | 排版气质 |
|----------|---------|---------|---------|
| 专项攻略 | h1+h2+h3+paragraph+code-block+signature+interaction | step-label+image+highlight | 干货密集，代码块多 |
| 避坑指南 | h1+h2+paragraph+quote-block+signature+interaction | code-block+image | 案例驱动，引用多 |
| 开源项目 | h1+h2+paragraph+code-block+image+signature+interaction | step-label+list-ordered | 教程风，步骤清晰 |
| 他山石 | h1+h2+paragraph+quote-block+signature+interaction | image+highlight | 观点输出，引用多 |
| 江湖夜话 | h1+h2+paragraph+signature+interaction | quote-block+divider | 走心随笔，留白多 |
| 宗门实录 | h1+h2+paragraph+signature+interaction | image+quote-block | 故事叙述，节奏感 |

## 主题系统

### 默认主题：硅基极简

- 主色：`#1a1a1a`（近黑）
- 点缀色：`#4e6b99`（深蓝灰）
- 浅底色：`#f5f5f5` / `#f7f7f7`
- 正文色：`#333333`
- 辅助灰：`#999999` / `#dddddd`
- 下划线色：`#a0c4e8`（浅蓝灰）

### 自定义主题

参考 `references/theme-generator.md`，按描述或参考图生成新主题。生成的新主题写入 `references/theme-<name>.md`，并在 `references/theme-index.md` 中注册。

## 校验

### 产物校验（必须执行）

```bash
python scripts/validate_gzh_html.py <html_file>
```

检查项：
- 禁用标签清零：`<style>`/`<script>`/`<div>`/`<iframe>`
- 禁用属性清零：`class=`/`id=`/`position:`/`float`
- `<span leaf="">` 包裹率：100%
- 半角标点检测
- 签名落款完整性
- 互动话题存在性

### 组件库源头检查（定期执行）

```bash
python scripts/component_lint.py references/
```

检查项：
- 组件 HTML 是否包含禁用项
- 是否有 `position:fixed/absolute/sticky`/`float`/`display:grid`
- 所有文字节点是否用 `<span leaf="">` 包裹

## 排版禁忌

1. 禁止使用 `<style>`/`<script>`/`<div>`/`class=`/`id=`
2. 禁止使用 `position:fixed/absolute/sticky`/`float`/`display:grid`
3. 禁止使用 CSS 变量 `var(--xxx)`
4. 禁止正文 emoji（落款区的 📖📝🖊️🏷️ 除外）
5. 禁止虚假权威语气（"至关重要"/"不可或缺"/"赋能"/"全流程"等 AI 味词汇）
6. 禁止知识截止声明
7. 禁止广告语气
