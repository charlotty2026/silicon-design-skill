# 贡献指南

## 如何贡献

### 报告问题

发现 bug 或有功能建议，请通过 GitHub Issues 提交：

1. 描述问题（或建议）
2. 提供复现步骤（如适用）
3. 附上输入 Markdown 和输出 HTML（如有）

### 提交代码

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 提交改动：`git commit -m "feat: 描述你的改动"`
4. 推送分支：`git push origin feature/your-feature`
5. 提交 Pull Request

### 代码规范

- Python 代码遵循 PEP 8
- Markdown 文件使用 UTF-8 编码，LF 换行
- HTML 组件必须通过 `component_lint.py` 检查
- 校验脚本新增的检查规则必须附带测试用例

### 新增主题

1. 按 `references/theme-generator.md` 的工作流生成主题
2. 保存为 `references/theme-<name>.md`
3. 在 `references/theme-index.md` 中注册
4. 生成预览 HTML 到 `assets/theme-previews/<name>.html`
5. 运行 `python scripts/component_lint.py references/theme-<name>.md` 确保通过

### 新增组件

1. 在对应主题的组件库文件中添加组件定义
2. 组件编号延续当前最大编号
3. 必须包含：组件名、触发条件、HTML 代码、说明
4. 运行 `python scripts/component_lint.py` 确保通过
5. 更新 `SKILL.md` 中的组件清单（如需要）

## License

提交的代码默认遵循 AGPL-3.0 协议。
