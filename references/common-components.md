# 通用增量组件

> 跨主题通用的组件，所有主题共享。这些组件不依赖主题色板，使用中性色。

## 章节锚点编号

自动为 H2/H3 添加中文编号：

```
H2 → 一、二、三、
H3 → （一）（二）（三）
H4 → 1、2、3、
H5 → 1.1、1.2、1.3
```

规则：
- 编号在装配阶段自动添加，不从 Markdown 原文中读取
- 如果原文已有编号，先去除再重新编号
- "互动话题"标题不编号

---

## 段落首行缩进（可选）

默认不缩进。如果用户明确要求"首行缩进"：

```html
<p style="margin:0 0 16px 0;padding:0;line-height:1.8;font-size:16px;color:#333333;letter-spacing:0.5px;text-align:justify;text-indent:2em;"><span leaf="">段落内容</span></p>
```

说明：`text-indent:2em` 实现首行缩进 2 字符。仅用于特定文章类型（如江湖夜话）。

---

## 脚注/注释

用于补充说明，不影响正文阅读流：

```html
<p style="margin:8px 0 16px 0;padding:0;line-height:1.6;font-size:13px;color:#999999;letter-spacing:0.5px;"><span leaf="">注：这是补充说明文字，字号小、颜色浅，不干扰正文。</span></p>
```

说明：13px 浅灰，用于术语解释、出处标注等。

---

## 表格

公众号对 `<table>` 支持有限，用 `<section>` + flex 布局模拟：

```html
<section style="margin:16px 0;padding:0;border:1px solid #e0e0e0;border-radius:4px;overflow:hidden;">
<section style="display:flex;background:#f5f5f5;border-bottom:1px solid #e0e0e0;">
<span style="flex:1;padding:8px 12px;font-size:14px;font-weight:bold;color:#333;border-right:1px solid #e0e0e0;"><span leaf="">列1</span></span>
<span style="flex:1;padding:8px 12px;font-size:14px;font-weight:bold;color:#333;"><span leaf="">列2</span></span>
</section>
<section style="display:flex;border-bottom:1px solid #e0e0e0;">
<span style="flex:1;padding:8px 12px;font-size:14px;color:#666;border-right:1px solid #e0e0e0;"><span leaf="">内容1</span></span>
<span style="flex:1;padding:8px 12px;font-size:14px;color:#666;"><span leaf="">内容2</span></span>
</section>
<section style="display:flex;">
<span style="flex:1;padding:8px 12px;font-size:14px;color:#666;border-right:1px solid #e0e0e0;"><span leaf="">内容3</span></span>
<span style="flex:1;padding:8px 12px;font-size:14px;color:#666;"><span leaf="">内容4</span></span>
</section>
</section>
```

说明：
- 用 `flex` 布局代替 `<table>`（兼容性更好）
- 表头灰底加粗，内容行白底
- 最多 4 列（列数过多手机端不可读）

---

## 提示框

用于强调重要信息（警告/提示/注意）：

```html
<section style="margin:16px 0;padding:12px 16px;background:#fff8e1;border-left:3px solid #ffa000;border-radius:0 4px 4px 0;">
<p style="margin:0;padding:0;line-height:1.8;font-size:15px;color:#666;"><span leaf=""><strong style="font-weight:bold;">注意：</strong>这是需要注意的内容。</span></p>
</section>
```

变体：
- 警告（红）：`background:#ffebee;border-left-color:#e53935`
- 提示（蓝）：`background:#e3f2fd;border-left-color:#1976d2`
- 成功（绿）：`background:#e8f5e9;border-left-color:#43a047`

---

## 链接

公众号正文不支持外链跳转，链接以文字形式展示：

```html
<span style="color:#4e6b99;text-decoration:underline;"><span leaf="">链接文字（https://example.com）</span></span>
```

说明：
- 链接 URL 必须在正文中以纯文本展示
- 用点缀色 + 下划线标注
- 可在文末"参考资料"区集中列出

---

## 参考资料

文末参考资料区：

```html
<h3 style="margin:20px 0 10px 0;padding:0;font-size:16px;font-weight:bold;color:#1a1a1a;line-height:1.4;"><span leaf="">参考资料</span></h3>
<section style="margin:0 0 16px 0;padding:0 0 0 20px;line-height:1.8;font-size:14px;color:#666;">
<p style="margin:0 0 4px 0;padding:0;"><span leaf="">1. 资料标题（https://example.com）</span></p>
<p style="margin:0 0 4px 0;padding:0;"><span leaf="">2. 资料标题（https://example.com）</span></p>
</section>
```

说明：
- 14px 浅灰，手动编号
- 放在互动话题之前、正文之后
- 非必需，有引用时才添加
