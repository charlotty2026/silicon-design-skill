# Known Issues

## v1.0

### #1 validate_gzh_html.py span leaf 定位使用 html.find，重复文本只定位第一个

**状态**：已确认，v1.0 够用，后续优化
**影响**：当同一段文本在 HTML 中出现多次时，`check_span_wrap` 中的 `html.find(f'>{text}<')` 只会定位到第一个匹配位置，可能导致后续相同文本的包裹状态误判。
**当前缓解**：实际使用中重复文本较少，误判率低，不影响核心校验功能。
**后续方案**：改用正则 `re.finditer` 逐位置扫描，或用 HTML 解析器（如 html.parser）做精确的 DOM 遍历。
