# 主题索引

> 本文件是主题列表的唯一来源。新增主题必须在此注册。

## 已安装主题

| 主题代号 | 主题名称 | 主色 | 点缀色 | 适用场景 | 文件 |
|----------|---------|------|--------|---------|------|
| `silicon-minimal` | 硅基极简 | `#1a1a1a` | `#4e6b99` | 技术干货、教程、观点输出（默认主题） | `theme-silicon-minimal.md` |

## 主题选择规则

1. 如果用户明确指定主题，使用指定主题
2. 如果未指定，默认使用 `silicon-minimal`
3. 如果文章类型为"江湖夜话"或"团队故事"，可考虑使用更柔和的主题（待生成器产出后注册）

## 新增主题流程

1. 按 `theme-generator.md` 中的工作流生成新主题
2. 将生成结果保存为 `references/theme-<name>.md`
3. 在本文件的"已安装主题"表格中添加一行
4. 运行 `python scripts/component_lint.py references/theme-<name>.md` 确保组件合规
5. 在 `assets/theme-previews/` 中生成预览 HTML
