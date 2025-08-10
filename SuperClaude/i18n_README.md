# SuperClaude V4 Internationalization System Developer Documentation

## 📚 Overview

The SuperClaude V4 internationalization system provides complete multi-language support, including unified language switching for both the SuperClaude framework itself and Claude Code command descriptions.

### 🎯 Core Features

- **10 Language Support**: en_US, zh_CN, zh_TW, ja_JP, ko_KR, ru_RU, es_ES, de_DE, fr_FR, ar_SA
- **Unified Language Switching**: Switch both SuperClaude and Claude Code languages simultaneously via `/sc:i18n` command
- **High-Quality Translation**: Professional technical terminology translation and cultural adaptation
- **Developer Tools**: Incremental translation detection, batch translation, quality validation
- **Smart Caching**: Performance optimization and response time monitoring

## 🏗️ System Architecture

### 📋 File Structure
```
SuperClaude/
├── i18n.py                         # Core internationalization manager
├── claude_code_localizer.py        # Claude Code integration
├── i18n_command_handler.py         # /sc:i18n command handler
├── i18n_dev_tools.py              # Developer tools
├── claude_translator.py           # Professional translation tool (deprecated)
├── english_first_translator.py    # English-first translation tool
├── english_reference_translations.py # English reference translations
└── i18n_README.md                 # This documentation

Framework-Hooks/locales/
├── en_US.json                      # English reference source ⭐
├── zh_CN.json                      # Simplified Chinese translation
├── zh_TW.json                      # Traditional Chinese translation
├── ja_JP.json                      # Japanese translation
├── ko_KR.json                      # Korean translation
├── ru_RU.json                      # Russian translation
├── es_ES.json                      # Spanish translation
├── de_DE.json                      # German translation
├── fr_FR.json                      # French translation
└── ar_SA.json                      # Arabic translation

~/.claude/commands/sc/              # Claude Code command files
├── analyze.md
├── build.md
├── implement.md
└── ...                             # 18 command files
```

### 🌐 English-First Translation Architecture

#### Translation Source Design
- **English as Authoritative Source**: All translations derive from high-quality English reference
- **Professional Translation Quality**: Technical terminology and cultural adaptation
- **Consistency Guarantee**: Unified translation standards across all languages
- **Version Control**: Translation versioning and update tracking

#### Translation Workflow
```
English Reference (en_US.json) 
    ↓
Professional Translation Tools
    ↓
Target Language Files (zh_CN.json, ja_JP.json, etc.)
    ↓
Quality Validation & Cultural Adaptation
    ↓
Production Deployment
```

## 🚀 Quick Start

### Basic Usage
```python
from SuperClaude.i18n import get_localizer, t, set_language

# Get localization manager
localizer = get_localizer()

# Switch language
set_language('zh_CN')

# Get localized text
message = t('commands.analyze')
print(message)  # Output: "执行质量、安全、性能和架构领域的全面代码分析。"
```

### Command Line Usage
```bash
# Switch to Chinese
/sc:i18n switch zh_CN

# Check current language
/sc:i18n current

# List available languages
/sc:i18n list

# Update only Claude Code descriptions
/sc:i18n claude-code
```

## 🔧 Developer Tools

### Translation Development Tools
```python
from SuperClaude.i18n_dev_tools import I18nDevTools

dev_tools = I18nDevTools()

# Detect missing translations
missing = dev_tools.detect_missing_translations()

# Batch translate from English
dev_tools.batch_translate_from_english()

# Validate translation quality
dev_tools.validate_translations()
```

### English-First Translation Tools
```python
from SuperClaude.english_first_translator import translate_from_english_to_all_languages

# Generate all language translations from English reference
translate_from_english_to_all_languages()
```

## 📝 Locale File Format

### Standard Locale Structure
```json
{
  "metadata": {
    "language": "zh_CN",
    "name": "简体中文", 
    "version": "1.0.0",
    "last_updated": "2024-01-15T10:30:00Z",
    "translator": "SuperClaude AI",
    "source": "en_US",
    "completeness": 100
  },
  "commands": {
    "analyze": "执行质量、安全、性能和架构领域的全面代码分析。",
    "build": "构建、编译和打包项目，提供全面的错误处理和优化。"
  },
  "ui": {
    "welcome": "欢迎使用 SuperClaude V4",
    "language_switched": "语言已切换到 {language}"
  }
}
```

### Key-Value Translation Rules
- **Hierarchical Keys**: Use dot notation for nested structures (`commands.analyze`)
- **Parameter Interpolation**: Support for `{parameter}` placeholders
- **Cultural Adaptation**: Adjust content for cultural context
- **Technical Accuracy**: Maintain technical terminology precision

## 🌍 Supported Languages

| Code | Language | Native Name | Status | Completeness |
|------|----------|-------------|--------|--------------|
| `en_US` | English (US) | English | ✅ Reference | 100% |
| `zh_CN` | Simplified Chinese | 简体中文 | ✅ Complete | 100% |
| `zh_TW` | Traditional Chinese | 繁體中文 | ✅ Complete | 100% |
| `ja_JP` | Japanese | 日本語 | ✅ Complete | 100% |
| `ko_KR` | Korean | 한국어 | ✅ Complete | 100% |
| `ru_RU` | Russian | Русский | ✅ Complete | 100% |
| `es_ES` | Spanish | Español | ✅ Complete | 100% |
| `de_DE` | German | Deutsch | ✅ Complete | 100% |
| `fr_FR` | French | Français | ✅ Complete | 100% |
| `ar_SA` | Arabic | العربية | ✅ Complete | 100% |

## 🔄 Integration with Claude Code

### Automatic Command Description Updates
The system automatically updates Claude Code command descriptions when switching languages:

```bash
# Before language switch
/sc:analyze → "Perform comprehensive code analysis across quality, security, performance, and architecture domains."

# After switching to Chinese
/sc:analyze → "执行质量、安全、性能和架构领域的全面代码分析。"
```

### Command File Structure
Each command file (`~/.claude/commands/sc/*.md`) contains:
- **YAML Frontmatter**: Metadata including localized description
- **Markdown Content**: Command documentation and examples

## 🎯 Best Practices

### Translation Quality
- **Consistency**: Use consistent terminology across all translations
- **Context Awareness**: Consider technical context and user experience
- **Cultural Adaptation**: Adapt content for target culture and region
- **Regular Updates**: Keep translations synchronized with source changes

### Performance Optimization
- **Lazy Loading**: Load translations only when needed
- **Caching Strategy**: Cache frequently used translations
- **Memory Management**: Optimize memory usage for large translation sets
- **Response Time**: Monitor and optimize translation lookup performance

## 🛠️ Troubleshooting

### Common Issues

#### Missing Translation Keys
**Symptom**: English text appears instead of localized text

**Solution**:
```bash
# Check for missing keys
python -m SuperClaude.i18n_dev_tools --check-missing

# Add missing translations
python -m SuperClaude.i18n_dev_tools --add-missing
```

#### Language Switch Not Working
**Symptom**: Language doesn't change after `/sc:i18n switch`

**Solution**:
```bash
# Verify language code
/sc:i18n list

# Force refresh Claude Code
/sc:i18n claude-code

# Check system status
python -m SuperClaude.i18n_dev_tools --status
```

#### Translation Quality Issues
**Symptom**: Translation contains placeholders or inaccuracies

**Solution**:
```bash
# Validate translation quality
python -m SuperClaude.i18n_dev_tools --validate

# Regenerate from English source
python -m SuperClaude.english_first_translator
```

## 🔮 Future Enhancements

### Planned Features
- **Dynamic Translation**: Real-time translation updates
- **User Customization**: User-defined translation overrides
- **Translation Memory**: Translation reuse and consistency
- **Quality Metrics**: Translation quality scoring and monitoring
- **Community Contributions**: Community-driven translation improvements

### Extensibility
- **Plugin Architecture**: Support for translation plugins
- **Custom Locales**: Support for custom locale definitions
- **Translation APIs**: Integration with external translation services
- **Workflow Integration**: CI/CD pipeline integration for translations

---

## 📞 Support

For issues, questions, or contributions related to the internationalization system:

1. **Documentation**: Refer to this comprehensive guide
2. **Development Tools**: Use built-in diagnostic and development tools
3. **Quality Assurance**: Run validation tools before deployment
4. **Community**: Contribute to translation improvements and feedback

---

*This documentation is maintained as part of the SuperClaude V4 internationalization system. For updates and latest information, refer to the project repository.*
