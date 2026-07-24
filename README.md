# silicon-design-skill

> 把 Markdown 一键排成可直接粘进公众号编辑器的精致 HTML —— 硅基极简主题 + 主题生成器 + 双关卡校验。
>
> An AI-agent skill that turns Markdown into paste-ready WeChat article HTML, with component-library approach.

## 核心特性

- **组件库思维**：20 个预制组件覆盖公众号全部排版场景，Agent 按文章类型组合装配，不现场发挥
- **硅基极简主题**：内置「硅基聊斋」经实战验证的极简技术风格，克制用色，信息密度优先
- **主题生成器**：按描述或参考图生成新主题，色板自动派生全套组件
- **双关卡校验**：component_lint（源头）+ validate_gzh_html（产物），ERROR 清零才交付
- **全内联样式**：`<span leaf="">` 包裹 + 纯 inline style，规避公众号平台样式过滤
- **Agent 签名池**：内置多 Agent 签名模板，每篇自动匹配落款

## 安装

### Claude Code / Codex / Cursor / WorkBuddy / OpenCode

```bash
# 从 GitHub 安装
npx skills install charlotty2026/silicon-design-skill -g

# 或从 Gitee 安装（国内推荐）
npx skills install https://gitee.com/fenglinhuoshanmen/silicon-design-skill -g
```

安装后，Agent 在处理公众号排版任务时会自动触发本 Skill。

## 快速开始

对 Agent 说：

```
帮我把这篇 Markdown 排版成公众号文章
```

Agent 会自动：

1. 读取硅基极简主题组件库
2. 解析 Markdown 结构
3. 用组件库中的真实组件拼装 HTML
4. 跑校验脚本确保格式合规
5. 输出可直接粘贴的 HTML

## 文章类型自动适配

| 文章类型 | 必用组件 | 排版气质 |
|----------|---------|---------|
| 专项攻略 | h1+h2+h3+paragraph+code-block+signature+interaction | 干货密集，代码块多 |
| 避坑指南 | h1+h2+paragraph+quote-block+signature+interaction | 案例驱动，引用多 |
| 开源项目 | h1+h2+paragraph+code-block+image+signature+interaction | 教程风，步骤清晰 |
| 他山石 | h1+h2+paragraph+quote-block+signature+interaction | 观点输出，引用多 |
| 江湖夜话 | h1+h2+paragraph+signature+interaction | 走心随笔，留白多 |
| 团队故事 | h1+h2+paragraph+signature+interaction | 故事叙述，节奏感 |

## 目录结构

```
silicon-design-skill/
├── SKILL.md                         # 排版工作流主文档（Agent 入口）
├── references/
│   ├── theme-index.md               # 主题索引（单一来源）
│   ├── theme-silicon-minimal.md     # 硅基极简主题组件库（默认主题）
│   ├── theme-generator.md           # 主题生成器
│   ├── common-components.md         # 跨主题通用增量组件
│   ├── format-normalize.md          # 格式归一化
│   └── eval-cases.md                # 触发用例 + 可验证循环
├── scripts/
│   ├── validate_gzh_html.py         # 产物合规校验
│   └── component_lint.py            # 组件库源头检查
├── assets/
│   └── sample-article.md            # 演示输入
├── README.md
├── CONTRIBUTING.md
└── LICENSE                          # AGPL-3.0
```

## 设计哲学

1. **约束而非自由** — 预设色板和固定组件保证输出下限，不让模型现场发挥
2. **样式粘贴不掉** — 全内联样式 + `<span leaf="">` 包裹，规避公众号会过滤的写法
3. **质量靠脚本不靠自觉** — 双关卡确定性检查平台红线和标点
4. **换模型不走样** — 排版逻辑全沉淀在组件库和脚本里，不依赖某家模型

## 致谢

- [gzh-design-skill](https://github.com/isjiamu/gzh-design-skill) by 摸鱼小李 — 组件库思维和双关卡校验的灵感来源

## License

AGPL-3.0
