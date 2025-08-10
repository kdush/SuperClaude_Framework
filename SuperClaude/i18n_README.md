# SuperClaude V4 国际化系统开发者文档

## 📚 概述

SuperClaude V4 国际化系统提供完整的多语言支持，包括 SuperClaude 框架本身和 Claude Code 命令描述的统一语言切换。

### 🎯 核心特性

- **10 种语言支持**：en_US, zh_CN, zh_TW, ja_JP, ko_KR, ru_RU, es_ES, de_DE, fr_FR, ar_SA
- **统一语言切换**：通过 `/sc:i18n` 命令同时切换 SuperClaude 和 Claude Code 语言
- **高质量翻译**：专业的技术术语翻译和文化适应
- **开发者工具**：增量翻译检测、批量翻译、质量验证
- **智能缓存**：性能优化和响应时间监控

## 🏗️ 系统架构

```
SuperClaude/
├── i18n.py                    # 核心国际化管理器
├── claude_code_localizer.py   # Claude Code 集成
├── i18n_command_handler.py    # /sc:i18n 命令处理
├── i18n_dev_tools.py         # 开发者工具
├── claude_translator.py      # 专业翻译工具
└── i18n_README.md            # 本文档

Framework-Hooks/locales/
├── en_US.json                 # 英语翻译
├── zh_CN.json                 # 简体中文翻译
├── zh_TW.json                 # 繁体中文翻译
├── ja_JP.json                 # 日语翻译
├── ko_KR.json                 # 韩语翻译
├── ru_RU.json                 # 俄语翻译
├── es_ES.json                 # 西班牙语翻译
├── de_DE.json                 # 德语翻译
├── fr_FR.json                 # 法语翻译
└── ar_SA.json                 # 阿拉伯语翻译

~/.claude/commands/sc/         # Claude Code 命令文件
├── analyze.md
├── build.md
├── implement.md
└── ...                        # 18个命令文件
```

## 🛠️ 开发者工作流程

### 1. 添加新的翻译键

当添加新功能时，需要在 `zh_CN.json` 中添加新的翻译键：

```json
{
  "commands": {
    "new_command": "新命令的中文描述"
  },
  "ui": {
    "new_message": "新界面消息"
  }
}
```

### 2. 检测缺失翻译

使用开发者工具检测哪些语言缺少新的翻译：

```bash
cd /Users/ray/workspace/sc/SuperClaude_Framework/SuperClaude
python i18n_dev_tools.py detect --reference zh_CN
```

### 3. 批量翻译

使用 Claude 的专业翻译能力更新所有语言：

```bash
python claude_translator.py
```

或使用开发者工具进行特定语言翻译：

```bash
python i18n_dev_tools.py translate zh_CN ko_KR ja_JP
```

### 4. 验证翻译质量

```bash
python i18n_dev_tools.py validate
```

### 5. 测试语言切换

```bash
python -c "
from SuperClaude.i18n_command_handler import I18nCommandHandler
handler = I18nCommandHandler()
handler.switch_language('ja')  # 测试日语切换
"
```

## 📋 locale 文件结构

每个 locale 文件遵循统一的 JSON 结构：

```json
{
  "metadata": {
    "language": "zh_CN",
    "name": "简体中文", 
    "version": "1.0.0",
    "build_time": "2025-08-11T01:30:00.000000",
    "total_items": 42,
    "build_cost": 0.000001,
    "quality_score": 1.0
  },
  "commands": {
    "analyze": "在质量、安全、性能和架构领域执行全面的代码分析。",
    "build": "构建、编译和打包项目，并提供全面的错误处理和优化。",
    // ... 18个命令的翻译
  },
  "ui": {
    "welcome": "欢迎使用 SuperClaude V4",
    "language_switched": "语言已切换到 {language}",
    "current_language": "当前语言：{language}"
  },
  "errors": {
    "file_not_found": "文件未找到：{filename}",
    "invalid_language": "不支持的语言代码：{code}"
  },
  "personas": {
    "architect": {
      "name": "系统架构师",
      "description": "专注于系统设计和长远架构决策的专家"
    }
    // ... 其他角色翻译
  },
  "system": {
    "initializing": "初始化中...",
    "ready": "系统就绪"
  }
}
```

## 🔧 工具参考

### i18n_dev_tools.py

开发者主要工具，提供以下命令：

#### 检测缺失翻译
```bash
python i18n_dev_tools.py detect [--reference zh_CN]
```

#### 批量翻译
```bash
python i18n_dev_tools.py translate <source> <target1> [target2...]
```

#### 生成所有缺失文件
```bash
python i18n_dev_tools.py generate-all
```

#### 验证翻译质量
```bash
python i18n_dev_tools.py validate [locale1] [locale2...]
```

### claude_translator.py

专业翻译工具，使用 Claude 的高质量翻译能力：

```bash
python claude_translator.py
```

这会：
- 自动翻译所有 18 个命令到 7 种语言（zh_TW, ko_KR, ru_RU, es_ES, de_DE, fr_FR, ar_SA）
- 使用专业的软件开发术语
- 保持文化适应性和技术准确性
- 更新 locale 文件和元数据

## 🌍 语言管理

### 支持的语言代码

| 代码 | 语言名称 | 本地名称 | 别名 |
|------|----------|----------|------|
| en_US | English (US) | English | en, english, us |
| zh_CN | Simplified Chinese | 简体中文 | zh, chinese, cn |
| zh_TW | Traditional Chinese | 繁體中文 | tw |
| ja_JP | Japanese | 日本語 | ja, jp, japanese |
| ko_KR | Korean | 한국어 | ko, kr, korean |
| ru_RU | Russian | Русский | ru, russian |
| es_ES | Spanish | Español | es, spanish |
| de_DE | German | Deutsch | de, german |
| fr_FR | French | Français | fr, french |
| ar_SA | Arabic | العربية | ar, arabic |

### 添加新语言

1. 在 `i18n_dev_tools.py` 的 `supported_languages` 中添加语言配置
2. 在 `i18n_command_handler.py` 的 `language_aliases` 中添加别名
3. 使用翻译工具生成 locale 文件：
   ```bash
   python i18n_dev_tools.py translate zh_CN new_language_code
   ```

## 🔗 Claude Code 集成

### 自动同步机制

当通过 `/sc:i18n` 切换语言时，系统会：

1. **更新 SuperClaude 框架**：切换内部本地化管理器
2. **更新 Claude Code 命令描述**：修改 `~/.claude/commands/sc/*.md` 文件的 YAML frontmatter
3. **提供用户反馈**：显示切换状态和重启提示

### 命令文件更新

对于每个命令文件，系统会更新 YAML frontmatter：

```yaml
---
name: analyze
description: "在质量、安全、性能和架构领域执行全面的代码分析。"
user: "ray"
---
```

## 📏 最佳实践

### 翻译质量标准

1. **技术准确性**：使用正确的软件开发术语
2. **文化适应性**：符合目标语言的表达习惯
3. **一致性**：在整个系统中保持术语一致
4. **简洁性**：保持描述简洁而准确
5. **专业性**：使用专业的技术写作风格

### 开发工作流

1. **中文优先**：以 `zh_CN` 作为主要参考语言
2. **增量更新**：每次添加功能后及时更新翻译
3. **质量验证**：使用验证工具检查翻译质量
4. **测试验证**：测试语言切换功能
5. **版本控制**：跟踪翻译变更和版本信息

### 性能优化

1. **缓存策略**：LocalizationManager 使用智能缓存
2. **延迟加载**：只加载当前语言的翻译
3. **批量操作**：使用批量翻译减少 API 调用
4. **监控指标**：跟踪翻译性能和命中率

## 🐛 故障排除

### 常见问题

#### 1. 语言切换失败

**症状**：`/sc:i18n switch <lang>` 报错不支持的语言代码

**解决方案**：
- 检查语言代码是否正确：`python -c "from SuperClaude.i18n import get_localizer; print(get_localizer().supported_locales)"`
- 检查别名映射：查看 `i18n_command_handler.py` 中的 `language_aliases`

#### 2. Claude Code 描述未更新

**症状**：Claude Code 仍显示之前语言的命令描述

**解决方案**：
- 重启 Claude Code
- 检查文件权限：确保 `~/.claude/commands/sc/` 目录可写
- 手动验证文件内容：`cat ~/.claude/commands/sc/analyze.md`

#### 3. 翻译质量问题

**症状**：翻译包含占位符或不准确

**解决方案**：
```bash
# 验证翻译质量
python i18n_dev_tools.py validate

# 重新生成专业翻译
python claude_translator.py

# 手动修复特定语言
python i18n_dev_tools.py translate zh_CN target_language
```

#### 4. locale 文件损坏

**症状**：JSON 解析错误或文件格式问题

**解决方案**：
```bash
# 检查 JSON 格式
python -m json.tool Framework-Hooks/locales/zh_CN.json

# 重新生成文件
python i18n_dev_tools.py generate-all
```

### 调试技巧

#### 1. 启用详细日志

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from SuperClaude.i18n import get_localizer
localizer = get_localizer()
localizer.set_locale('ja_JP')  # 查看详细切换过程
```

#### 2. 检查缓存状态

```python
from SuperClaude.i18n import get_localizer
localizer = get_localizer()
print(f"Cache size: {len(localizer._cache)}")
print(f"Cache hit rate: {localizer.cache_hit_rate:.2%}")
```

#### 3. 验证文件完整性

```bash
# 检查所有 locale 文件
find Framework-Hooks/locales -name "*.json" -exec python -m json.tool {} \; > /dev/null
echo "JSON validation complete"
```

## 📈 性能监控

### 关键指标

- **翻译缓存命中率**：应 > 80%
- **语言切换时间**：应 < 1 秒
- **内存使用量**：单个 locale < 50KB
- **并发性能**：支持多用户同时切换

### 监控代码示例

```python
from SuperClaude.i18n import get_localizer

localizer = get_localizer()
stats = localizer.get_performance_stats()

print(f"""
缓存命中率: {stats['cache_hit_rate']:.2%}
平均响应时间: {stats['avg_response_time']:.2f}ms
内存使用量: {stats['memory_usage']:.1f}KB
支持语言数: {len(stats['supported_locales'])}
""")
```

## 🚀 未来规划

### 计划功能

1. **动态翻译**：集成在线翻译 API 实现实时翻译
2. **翻译记忆**：维护翻译术语库提高一致性
3. **A/B 测试**：支持多版本翻译的用户体验测试
4. **社区贡献**：允许社区成员提交翻译改进
5. **自动化 CI/CD**：集成翻译验证到持续集成流程

### 扩展点

- **新语言支持**：添加更多地区语言
- **方言支持**：同种语言的地区差异
- **专业术语库**：特定领域的术语管理
- **翻译质量评分**：自动化翻译质量评估

## 📞 支持和贡献

### 获取帮助

- **文档问题**：查看本 README 文档
- **代码问题**：检查源代码注释和类型提示
- **功能请求**：在项目 issue 中提交

### 贡献指南

1. **翻译改进**：提交高质量翻译修正
2. **新语言支持**：按照标准流程添加新语言
3. **工具增强**：改进开发者工具功能
4. **文档更新**：保持文档与代码同步

---

**版本**: 1.0.0  
**更新时间**: 2025-08-11  
**维护者**: SuperClaude 开发团队  