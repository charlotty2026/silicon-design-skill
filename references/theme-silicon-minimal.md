# 硅基极简主题组件库

> 主题代号：`silicon-minimal`
> 设计原则：克制用色，信息密度优先，极简技术风
> 最后更新：2026-07-24

---

## 设计变量色板

| 角色 | 作用 | 色值 | 用量约束 |
|------|------|------|----------|
| 主色 | 章节编号、锚点强调 | `#1a1a1a` | 全文≤5处 |
| 点缀色 | 标签、链接、引用竖线 | `#4e6b99` | 引用竖线+引言卡+标签 |
| 浅底色 | 引用块背景 | `#f7f7f7` | — |
| 代码底色 | 代码块背景 | `#f5f5f5` | — |
| 正文色 | 段落文字 | `#333333` | 全文主体 |
| 辅助灰 | 落款、注释、分割线 | `#999999` / `#dddddd` | 落款+分割线 |
| 下划线色 | 关键词下划线 | `#a0c4e8` | 每段≤3处 |

克制三原则：
1. 主色只在锚点出现（全文≤5处），大面积用白底+灰阶
2. 一段内高亮≤2种（加粗+下划线）
3. 不用渐变、不用阴影（图片轻阴影除外）

---

## 全局外壳

每篇公众号文章的 HTML 外壳：

```html
<section style="max-width:578px;margin:0 auto;padding:0 16px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;font-size:16px;color:#333333;line-height:1.8;letter-spacing:0.5px;text-align:justify;">

  <!-- 引言卡 -->
  <!-- 正文内容 -->
  <!-- 互动话题 -->
  <!-- 签名落款 -->

</section>
```

说明：
- `max-width:578px` 对齐微信公众号正文宽度
- `font-family` 用系统字体栈，不依赖外部字体
- `letter-spacing:0.5px` 增加字间呼吸感
- `text-align:justify` 两端对齐

---

## 组件清单

### 1. h1-title — 文章主标题

**触发**：Markdown `# text`

```html
<h1 style="margin:0 0 20px 0;padding:0;font-size:22px;font-weight:bold;color:#1a1a1a;line-height:1.4;text-align:center;"><span leaf="">文章标题</span></h1>
```

说明：
- 22px 居中加粗，全文仅 1 个
- 不用 26px（实际产出验证 22px 在手机端更合适）

---

### 2. h2-section — 章节标题

**触发**：Markdown `## text`

```html
<h2 style="margin:24px 0 12px 0;padding:0 0 0 10px;font-size:18px;font-weight:bold;color:#1a1a1a;line-height:1.4;border-left:4px solid #1a1a1a;"><span leaf="">一、章节标题</span></h2>
```

说明：
- 18px 左对齐加粗 + 左竖线 4px
- 章节编号：一、二、三、（中文数字）
- `margin-top:24px` 与上文保持呼吸

---

### 3. h3-subsection — 小节标题

**触发**：Markdown `### text`（非"互动话题"）

```html
<h3 style="margin:20px 0 10px 0;padding:0;font-size:16px;font-weight:bold;color:#1a1a1a;line-height:1.4;"><span leaf="">（一）小节标题</span></h3>
```

说明：
- 16px 加粗，不加竖线（与 H2 区分层级）
- 小节编号：（一）（二）（三）

---

### 4. paragraph — 正文段落

**触发**：Markdown 普通文本段落

```html
<p style="margin:0 0 16px 0;padding:0;line-height:1.8;font-size:16px;color:#333333;letter-spacing:0.5px;text-align:justify;"><span leaf="">这是正文内容。每个段落用这个组件包裹，确保行距和字间距统一。</span></p>
```

说明：
- 16px / 行高 1.8 / 字间距 0.5px / 两端对齐
- `margin-bottom:16px` 段间距
- 所有文字必须用 `<span leaf="">` 包裹

---

### 5. bold-inline — 行内加粗

**触发**：Markdown `**text**`

```html
<strong style="font-weight:bold;color:#1a1a1a;"><span leaf="">加粗文字</span></strong>
```

说明：
- 加粗文字用近黑色 `#1a1a1a`，比正文 `#333` 更深
- 一段内加粗不超过 3 处

---

### 6. quote-block — 引用块

**触发**：Markdown `> text`

```html
<blockquote style="margin:16px 0;padding:12px 16px;background:#f7f7f7;border-left:3px solid #4e6b99;font-size:15px;color:#666;line-height:1.8;"><span leaf="">这是引用内容。灰底+深蓝灰左竖线，用于强调、补充说明、引用他人观点。</span></blockquote>
```

说明：
- 灰底 `#f7f7f7` + 左竖线 3px `#4e6b99`（点缀色）
- 字号 15px（比正文小 1px，视觉降级）
- 颜色 `#666`（比正文浅）

---

### 7. code-block — 代码块

**触发**：Markdown ` ```language\ncode\n``` `

```html
<section style="margin:16px 0;padding:0;border-radius:4px;overflow:hidden;">
<section style="padding:8px 12px;background:#e8e8e8;display:flex;align-items:center;gap:6px;">
<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#ff5f57;margin:0;"></span>
<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#febc2e;margin:0;"></span>
<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#28c840;margin:0;"></span>
</section>
<section style="margin:0;padding:12px 16px;background:#f5f5f5;border-radius:0 0 4px 4px;overflow-x:auto;">
<pre style="margin:0;padding:0;background:none;font-family:Menlo,Monaco,Consolas,'Courier New',monospace;font-size:13px;line-height:1.6;color:#333;white-space:pre-wrap;word-wrap:break-word;"><code style="font-family:Menlo,Monaco,Consolas,'Courier New',monospace;font-size:13px;color:#333;"><span leaf="">代码内容</span></code></pre>
</section>
</section>
```

说明：
- Mac 三色按钮 + 浅灰底 `#f5f5f5`
- 13px 等宽字体 Menlo/Consolas
- `white-space:pre-wrap` + `word-wrap:break-word` 长行自动换行
- 注意：用 `<section>` 代替 `<div>`（公众号过滤 div）

---

### 8. inline-code — 行内代码

**触发**：Markdown `` `code` ``

```html
<code style="font-family:Menlo,Monaco,Consolas,'Courier New',monospace;font-size:14px;color:#4e6b99;background:#f0f0f0;padding:1px 4px;border-radius:2px;"><span leaf="">code</span></code>
```

说明：
- 14px 等宽字体 + 浅灰底 `#f0f0f0` + 圆角 2px
- 文字色用点缀色 `#4e6b99`

---

### 9. image — 图片

**触发**：Markdown `![alt](url)`

```html
<section style="margin:16px 0;text-align:center;"><img src="图片URL" alt="图片说明" style="max-width:100%;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,0.1);"></section>
```

说明：
- 居中 + `max-width:100%` + 圆角 8px + 轻阴影
- 封面图尺寸：1080×864px（4:3 比例）
- 用 `<section>` 代替 `<div>`

---

### 10. divider — 分割线

**触发**：Markdown `---`

```html
<hr style="margin:24px 0;border:none;border-top:1px solid #dddddd;">
```

说明：
- 简洁水平线，颜色 `#dddddd`
- `margin:24px 0` 上下留白

---

### 11. info-card — 引言卡

**触发**：文章头部信息块

```html
<blockquote style="margin:0 0 20px 0;padding:12px 16px;background:#f7f7f7;border-left:3px solid #4e6b99;font-size:14px;color:#666;line-height:1.8;">
<span leaf="">栏目：专项攻略</span><br>
<span leaf="">作者：佛跳墙</span><br>
<span leaf="">日期：2026-07-24</span>
</blockquote>
```

说明：
- 文章第一个元素，紧跟 `<h1>` 之后
- 栏目/作者/日期三行
- 14px 小字，灰底+点缀色竖线

---

### 12. signature-block — 签名落款

**触发**：文章末尾固定结构

```html
<hr style="margin:24px 0;border:none;border-top:1px solid #dddddd;">
<p style="margin:0;padding:0;line-height:1.8;font-size:14px;color:#999999;text-align:center;font-style:italic;">
<span leaf="">— 硅基聊斋 —</span>
</p>
<p style="margin:8px 0 0 0;padding:0;line-height:1.8;font-size:14px;color:#999999;text-align:center;">
<span leaf="">📖 栏目：专项攻略</span><br>
<span leaf="">📝 创作时间：2026-07-24</span><br>
<span leaf="">🖊️ 本期作者：佛跳墙</span><br>
<span leaf="">🏷️ 标签：硅基聊斋 | AI | 提示词</span>
</p>
<p style="margin:12px 0 0 0;padding:0;line-height:1.8;font-size:14px;color:#999999;text-align:center;font-style:italic;">
<span leaf="">—— 佛跳墙</span><br>
<span leaf="">代码不会骗人，跑通才算数。</span>
</p>
```

说明：
- 分割线 + "硅基聊斋"品牌行 + 栏目/日期/作者/标签 + Agent 签名
- 14px 灰色 `#999` 居中
- 落款区的 emoji（📖📝🖊️🏷️）是唯一允许的 emoji
- 签名从签名池随机匹配 1 条

---

### 13. interaction-topic — 互动话题

**触发**：Markdown `### 互动话题` 或文末话题段落

```html
<h3 style="margin:20px 0 10px 0;padding:0;font-size:16px;font-weight:bold;color:#1a1a1a;line-height:1.4;"><span leaf="">互动话题</span></h3>
<p style="margin:0 0 16px 0;padding:0;line-height:1.8;font-size:16px;color:#333333;letter-spacing:0.5px;text-align:justify;"><span leaf="">你在实际使用中遇到过什么问题？欢迎在评论区聊聊。</span></p>
```

说明：
- 每篇文章必须有互动话题
- 放在正文末尾、签名落款之前
- 用 H3 样式但标题固定为"互动话题"

---

### 14. tag-list — 标签列表

**触发**：落款区标签行

```html
<span leaf="">🏷️ 标签：硅基聊斋 | 标签1 | 标签2 | 标签3</span>
```

说明：
- `#硅基聊斋` 必须第一个
- 总标签 3-6 个
- 标签之间用 ` | ` 分隔
- 嵌入 signature-block 的第二段中

---

### 15. step-label — 步骤标签

**触发**：Markdown `**步骤1：**` 或 `**Step 1:**`

```html
<p style="margin:0 0 8px 0;padding:0;line-height:1.8;font-size:16px;color:#333333;letter-spacing:0.5px;"><strong style="font-weight:bold;color:#1a1a1a;"><span leaf="">步骤1：</span></strong><span leaf="">步骤内容描述。</span></p>
```

说明：
- 步骤标签加粗近黑色，紧跟步骤内容
- 用于教程类文章的步骤拆解

---

### 16. list-ordered — 有序列表

**触发**：Markdown `1. text`

```html
<section style="margin:0 0 16px 0;padding:0 0 0 20px;line-height:1.8;font-size:16px;color:#333333;">
<p style="margin:0 0 4px 0;padding:0;"><span leaf="">1. 第一项</span></p>
<p style="margin:0 0 4px 0;padding:0;"><span leaf="">2. 第二项</span></p>
<p style="margin:0 0 4px 0;padding:0;"><span leaf="">3. 第三项</span></p>
</section>
```

说明：
- 手动编号（公众号可能重置 `<ol>` 编号）
- 缩进 20px
- 每项间距 4px

---

### 17. list-unordered — 无序列表

**触发**：Markdown `- text`

```html
<section style="margin:0 0 16px 0;padding:0 0 0 20px;line-height:1.8;font-size:16px;color:#333333;">
<p style="margin:0 0 4px 0;padding:0;"><span leaf="">• 第一项</span></p>
<p style="margin:0 0 4px 0;padding:0;"><span leaf="">• 第二项</span></p>
<p style="margin:0 0 4px 0;padding:0;"><span leaf="">• 第三项</span></p>
</section>
```

说明：
- 手动 bullet 符号 `•`
- 缩进 20px
- 用 `<section>` 代替 `<ul>`

---

### 18. highlight-text — 黄底高亮文字

**触发**：Markdown `==text==`（自定义语法）

```html
<span style="background:#fff3cd;padding:1px 3px;border-radius:2px;"><span leaf="">高亮文字</span></span>
```

说明：
- 黄底 `#fff3cd` + 圆角 2px
- 用于标注关键结论、重要提醒
- 一段内最多 1 处

---

### 19. keyword-underline — 关键词下划线

**触发**：自动提取每段 1-3 个关键词

```html
<span style="border-bottom:1px solid #a0c4e8;padding-bottom:1px;"><span leaf="">关键词</span></span>
```

说明：
- 浅蓝灰下划线 `#a0c4e8`
- 用于标注技术术语、核心概念
- 每段最多 3 个关键词
- 与加粗不同时使用（一段内高亮≤2种）

---

### 20. placeholder — 待补素材占位

**触发**：Markdown `[待补: xxx]`

```html
<span style="background:#fff3cd;color:#996600;padding:2px 6px;border-radius:2px;font-size:14px;"><span leaf="">[待补: xxx]</span></span>
```

说明：
- 黄底棕字醒目标记
- 表示需要手动补充的素材
- 交付前必须全部替换，否则校验报 ERROR

---

## Agent 签名池

| Agent | 签名池 |
|-------|--------|
| 佛跳墙 | `代码不会骗人，跑通才算数。` / `本篇由佛跳墙技术出品。` / `先跑通再优化，别反着来。` |
| 西湖醋鱼 | `宗主今天也在思考。` / `以上内容已经宗主审阅。` / `宗主说：写得还行。` |
| 伏特加 | `伏特加出品，度数够高。` / `干活不拖，收工不磨。` / `先把活干了再说。` |
| 锅包又 | `保险柜护法提醒您：签字前再看一遍。` / `合规审查通过，请放心食用。` |
| 冰拿铁 | `冰镇出品，常温饮用。` / `这篇是凉的，慢慢看。` |

签名匹配规则：
- 用户指定作者 → 用该作者签名池
- 未指定 → 按文章类型推断：
  - 专项攻略/开源项目/避坑指南 → 佛跳墙
  - 宗门实录 → 伏特加
  - 他山石/江湖夜话 → 佛跳墙或西湖醋鱼

---

## 排版禁忌词清单

以下词汇在正文中出现时，应替换为更自然的表述：

| 禁用词 | 替代建议 |
|--------|---------|
| 综上所述 | 删掉或用"说到底" |
| 值得注意的是 | 删掉或用"有个细节" |
| 至关重要 | "很关键" |
| 不可或缺 | "少不了" |
| 确保安全 | "保安全" |
| 赋能 | "帮上忙" / "助力" |
| 全流程 | "整个流程" / "从头到尾" |
| 全方位 | "各方面" |
| 深度融合 | "结合" |
| 显著提升 | "明显好" / "提升不少" |
| 核心竞争力 | "看家本事" / "关键优势" |
| 战略高度 | 删掉 |
| 此外 | "另外" / 删掉 |
| 提供全方位 | "全面提供" |

---

## 完整装配示例

输入 Markdown：

```markdown
# AI 总自作主张？给它画三条红线

> 栏目：专项攻略
> 作者：佛跳墙
> 日期：2026-07-24

## 一、红线一：不碰报价

AI 在报价区绝对不能动手。报价数字是客户的底线，改一个数字可能丢一个单子。

### （一）具体怎么做

在系统提示词里写死：**报价区域的内容只字不改**。

```
示例代码
```

---

## 互动话题

你在用 AI 做标书时踩过什么坑？
```

输出 HTML：

```html
<section style="max-width:578px;margin:0 auto;padding:0 16px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;font-size:16px;color:#333333;line-height:1.8;letter-spacing:0.5px;text-align:justify;">

<h1 style="margin:0 0 20px 0;padding:0;font-size:22px;font-weight:bold;color:#1a1a1a;line-height:1.4;text-align:center;"><span leaf="">AI 总自作主张？给它画三条红线</span></h1>

<blockquote style="margin:0 0 20px 0;padding:12px 16px;background:#f7f7f7;border-left:3px solid #4e6b99;font-size:14px;color:#666;line-height:1.8;">
<span leaf="">栏目：专项攻略</span><br>
<span leaf="">作者：佛跳墙</span><br>
<span leaf="">日期：2026-07-24</span>
</blockquote>

<h2 style="margin:24px 0 12px 0;padding:0 0 0 10px;font-size:18px;font-weight:bold;color:#1a1a1a;line-height:1.4;border-left:4px solid #1a1a1a;"><span leaf="">一、红线一：不碰报价</span></h2>

<p style="margin:0 0 16px 0;padding:0;line-height:1.8;font-size:16px;color:#333333;letter-spacing:0.5px;text-align:justify;"><span leaf="">AI 在报价区绝对不能动手。报价数字是客户的底线，改一个数字可能丢一个单子。</span></p>

<h3 style="margin:20px 0 10px 0;padding:0;font-size:16px;font-weight:bold;color:#1a1a1a;line-height:1.4;"><span leaf="">（一）具体怎么做</span></h3>

<p style="margin:0 0 16px 0;padding:0;line-height:1.8;font-size:16px;color:#333333;letter-spacing:0.5px;text-align:justify;"><span leaf="">在系统提示词里写死：</span><strong style="font-weight:bold;color:#1a1a1a;"><span leaf="">报价区域的内容只字不改</span></strong><span leaf="">。</span></p>

<section style="margin:16px 0;padding:0;border-radius:4px;overflow:hidden;">
<section style="padding:8px 12px;background:#e8e8e8;display:flex;align-items:center;gap:6px;">
<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#ff5f57;margin:0;"></span>
<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#febc2e;margin:0;"></span>
<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#28c840;margin:0;"></span>
</section>
<section style="margin:0;padding:12px 16px;background:#f5f5f5;border-radius:0 0 4px 4px;overflow-x:auto;">
<pre style="margin:0;padding:0;background:none;font-family:Menlo,Monaco,Consolas,'Courier New',monospace;font-size:13px;line-height:1.6;color:#333;white-space:pre-wrap;word-wrap:break-word;"><code style="font-family:Menlo,Monaco,Consolas,'Courier New',monospace;font-size:13px;color:#333;"><span leaf="">示例代码</span></code></pre>
</section>
</section>

<hr style="margin:24px 0;border:none;border-top:1px solid #dddddd;">

<h3 style="margin:20px 0 10px 0;padding:0;font-size:16px;font-weight:bold;color:#1a1a1a;line-height:1.4;"><span leaf="">互动话题</span></h3>
<p style="margin:0 0 16px 0;padding:0;line-height:1.8;font-size:16px;color:#333333;letter-spacing:0.5px;text-align:justify;"><span leaf="">你在用 AI 做标书时踩过什么坑？</span></p>

<hr style="margin:24px 0;border:none;border-top:1px solid #dddddd;">
<p style="margin:0;padding:0;line-height:1.8;font-size:14px;color:#999999;text-align:center;font-style:italic;">
<span leaf="">— 硅基聊斋 —</span>
</p>
<p style="margin:8px 0 0 0;padding:0;line-height:1.8;font-size:14px;color:#999999;text-align:center;">
<span leaf="">📖 栏目：专项攻略</span><br>
<span leaf="">📝 创作时间：2026-07-24</span><br>
<span leaf="">🖊️ 本期作者：佛跳墙</span><br>
<span leaf="">🏷️ 标签：硅基聊斋 | AI | 提示词</span>
</p>
<p style="margin:12px 0 0 0;padding:0;line-height:1.8;font-size:14px;color:#999999;text-align:center;font-style:italic;">
<span leaf="">—— 佛跳墙</span><br>
<span leaf="">代码不会骗人，跑通才算数。</span>
</p>

</section>
```
