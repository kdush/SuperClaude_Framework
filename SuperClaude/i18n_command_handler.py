#!/usr/bin/env python3
"""
SuperClaude V4 /sc:i18n Command Handler
SuperClaude V4 /sc:i18n 命令处理器

Integrated unified language switching for Claude Code and SuperClaude i18n system
集成 Claude Code 和 SuperClaude i18n 系统的统一语言切换
"""

import sys
import re
from pathlib import Path
from typing import Optional, List, Dict

# 添加路径以导入模块
sys.path.insert(0, str(Path(__file__).parent.parent))

from SuperClaude.i18n import get_localizer
from SuperClaude.claude_code_localizer import ClaudeCodeLocalizer


class I18nCommandHandler:
    """Handle unified language switching for /sc:i18n commands / 处理 /sc:i18n 命令的统一语言切换"""
    
    def __init__(self):
        self.localizer = get_localizer()
        self.claude_localizer = ClaudeCodeLocalizer()
        
        # Language code mapping / 语言代码映射
        self.language_aliases = {
            'zh': 'zh_CN',
            'chinese': 'zh_CN',
            'cn': 'zh_CN',
            'en': 'en_US', 
            'english': 'en_US',
            'us': 'en_US',
            'ja': 'ja_JP',  # Add direct Japanese mapping / 添加直接的日语映射
            'jp': 'ja_JP',
            'japanese': 'ja_JP',
            'ko': 'ko_KR',  # Add direct Korean mapping / 添加直接的韩语映射
            'kr': 'ko_KR',
            'korean': 'ko_KR',
            'es': 'es_ES',
            'spanish': 'es_ES',
            'fr': 'fr_FR',
            'french': 'fr_FR',
            'de': 'de_DE',
            'german': 'de_DE',
            'ru': 'ru_RU',
            'russian': 'ru_RU',
            'ar': 'ar_SA',
            'arabic': 'ar_SA',
            'tw': 'zh_TW'
        }
    
    def handle_command(self, command_args: str) -> bool:
        """
        处理 /sc:i18n 命令
        
        Args:
            command_args: 命令参数字符串，如 "switch zh_CN" 或 "current"
            
        Returns:
            操作是否成功
        """
        if not command_args:
            self.show_help()
            return True
        
        # 解析命令参数
        parts = command_args.strip().split()
        if not parts:
            self.show_help()
            return True
        
        subcommand = parts[0].lower()
        
        if subcommand == 'switch':
            if len(parts) < 2:
                print("❌ 错误：缺少语言代码")
                print("💡 用法：/sc:i18n switch <language_code>")
                print("💡 示例：/sc:i18n switch zh_CN")
                return False
            
            language_code = parts[1].lower()
            return self.switch_language(language_code)
            
        elif subcommand == 'current':
            return self.show_current_language()
            
        elif subcommand == 'list':
            return self.list_languages()
            
        elif subcommand == 'claude-code':
            return self.update_claude_code_only()
            
        else:
            print(f"❌ 未知子命令：{subcommand}")
            self.show_help()
            return False
    
    def switch_language(self, language_input: str) -> bool:
        """
        切换语言（SuperClaude + Claude Code）
        
        Args:
            language_input: 语言代码或别名
            
        Returns:
            切换是否成功
        """
        # 解析语言代码
        target_locale = self._resolve_language_code(language_input)
        if not target_locale:
            print(f"❌ 不支持的语言代码：{language_input}")
            self.list_languages()
            return False
        
        language_name = self._get_locale_name(target_locale)
        print(f"🌐 切换到 {language_name} ({target_locale})...")
        
        # 1. 切换 SuperClaude i18n 系统
        print("📱 更新 SuperClaude 框架语言...")
        success1 = self.localizer.set_locale(target_locale)
        if success1:
            print(f"  ✅ SuperClaude 框架已切换到 {language_name}")
        else:
            print(f"  ❌ SuperClaude 框架切换失败")
        
        # 2. 更新 Claude Code 命令描述
        print("🔧 更新 Claude Code 命令描述...")
        success2 = self.claude_localizer.update_command_descriptions(target_locale)
        if success2:
            print(f"  ✅ Claude Code 命令描述已切换到 {language_name}")
        else:
            print(f"  ❌ Claude Code 命令描述切换失败")
        
        # 总结
        if success1 and success2:
            print(f"\n🎉 语言切换完成！")
            print(f"📍 当前语言：{language_name} ({target_locale})")
            print(f"💡 重启 Claude Code 以查看完整的 {language_name} 界面")
            return True
        elif success1 or success2:
            print(f"\n⚠️ 部分切换成功")
            return True
        else:
            print(f"\n❌ 语言切换失败")
            return False
    
    def show_current_language(self) -> bool:
        """显示当前语言状态"""
        current_locale = self.localizer.get_current_locale()
        language_name = self._get_locale_name(current_locale)
        
        print(f"=== 当前语言状态 ===")
        print(f"📍 语言：{language_name}")
        print(f"🔧 代码：{current_locale}")
        print(f"🌐 SuperClaude：✅ 使用 {language_name}")
        print(f"💻 Claude Code：✅ 命令描述使用 {language_name}")
        
        # 显示一个示例命令
        print(f"\n📋 命令描述示例：")
        test_desc = self.localizer.get_text('commands.test')
        print(f"  /sc:test → {test_desc}")
        
        return True
    
    def list_languages(self) -> bool:
        """列出所有可用语言"""
        print("=== 可用语言列表 ===")
        print(f"{'代码':<8} {'语言名称':<20} {'本地名称':<15} {'状态'}")
        print("─" * 60)
        
        # 所有支持的语言
        languages = [
            ('en_US', 'English (US)', 'English'),
            ('zh_CN', 'Simplified Chinese', '简体中文'),
            ('zh_TW', 'Traditional Chinese', '繁體中文'),
            ('ja_JP', 'Japanese', '日本語'),
            ('ko_KR', 'Korean', '한국어'),
            ('ru_RU', 'Russian', 'Русский'),
            ('es_ES', 'Spanish', 'Español'),
            ('de_DE', 'German', 'Deutsch'),
            ('fr_FR', 'French', 'Français'),
            ('ar_SA', 'Arabic', 'العربية')
        ]
        
        current_locale = self.localizer.get_current_locale()
        
        for code, english_name, native_name in languages:
            status = "✅ 当前" if code == current_locale else "✅ 可用"
            print(f"{code:<8} {english_name:<20} {native_name:<15} {status}")
        
        print("\n💡 使用方法：")
        print("  /sc:i18n switch zh_CN    # 切换到简体中文")
        print("  /sc:i18n switch en_US    # 切换到英语")
        print("  /sc:i18n switch ja_JP    # 切换到日语")
        
        print("\n🔧 支持的别名：")
        print("  zh, chinese, cn → zh_CN")
        print("  en, english, us → en_US")
        print("  jp, japanese → ja_JP")
        print("  kr, korean → ko_KR")
        
        return True
    
    def update_claude_code_only(self) -> bool:
        """仅更新 Claude Code 命令描述（不切换 SuperClaude 语言）"""
        current_locale = self.localizer.get_current_locale()
        language_name = self._get_locale_name(current_locale)
        
        print(f"🔧 更新 Claude Code 命令描述为 {language_name}...")
        
        success = self.claude_localizer.update_command_descriptions()
        
        if success:
            print(f"✅ Claude Code 命令描述已更新为 {language_name}")
            print("💡 重启 Claude Code 以查看更改")
        else:
            print("❌ 命令描述更新失败")
        
        return success
    
    def show_help(self):
        """显示帮助信息"""
        print("=== /sc:i18n 命令帮助 ===")
        print()
        print("🌐 用途：切换 SuperClaude 和 Claude Code 的显示语言")
        print()
        print("📝 可用命令：")
        print("  /sc:i18n switch <语言代码>  切换语言")
        print("  /sc:i18n current            查看当前语言")
        print("  /sc:i18n list               列出可用语言")
        print("  /sc:i18n claude-code        仅更新 Claude Code 描述")
        print()
        print("💡 使用示例：")
        print("  /sc:i18n switch zh_CN       # 切换到简体中文")
        print("  /sc:i18n switch en          # 切换到英语（使用别名）")
        print("  /sc:i18n current            # 查看当前语言状态")
        print("  /sc:i18n list               # 查看所有可用语言")
    
    def _resolve_language_code(self, language_input: str) -> Optional[str]:
        """
        解析语言代码，支持别名
        
        Args:
            language_input: 用户输入的语言代码或别名
            
        Returns:
            标准语言代码，如果无法解析则返回 None
        """
        language_input = language_input.lower().strip()
        
        # 检查是否是别名
        if language_input in self.language_aliases:
            return self.language_aliases[language_input]
        
        # 检查是否是标准代码
        standard_codes = ['en_US', 'zh_CN', 'zh_TW', 'ja_JP', 'ko_KR', 
                         'ru_RU', 'es_ES', 'de_DE', 'fr_FR', 'ar_SA']
        
        if language_input.upper() in [code.upper() for code in standard_codes]:
            # 返回正确大小写的代码
            for code in standard_codes:
                if code.upper() == language_input.upper():
                    return code
        
        return None
    
    def _get_locale_name(self, locale_code):
        """获取语言的友好名称"""
        locale_names = {
            'en_US': 'English',
            'zh_CN': '简体中文',
            'zh_TW': '繁體中文',
            'ja_JP': '日本語',
            'ko_KR': '한국어',
            'es_ES': 'Español',
            'fr_FR': 'Français',
            'de_DE': 'Deutsch',
            'ru_RU': 'Русский',
            'ar_SA': 'العربية'
        }
        return locale_names.get(locale_code, locale_code)


def main():
    """主函数 - 测试 i18n 命令处理"""
    handler = I18nCommandHandler()
    
    print("=== SuperClaude V4 - /sc:i18n 命令处理器测试 ===")
    print()
    
    # 测试各种命令
    test_commands = [
        "current",
        "list", 
        "switch zh_CN",
        "current",
        "switch en",
        "current"
    ]
    
    for cmd in test_commands:
        print(f"🔸 测试命令：/sc:i18n {cmd}")
        handler.handle_command(cmd)
        print("─" * 50)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 命令行模式
        handler = I18nCommandHandler()
        command_args = " ".join(sys.argv[1:])
        success = handler.handle_command(command_args)
        sys.exit(0 if success else 1)
    else:
        # 测试模式
        main()