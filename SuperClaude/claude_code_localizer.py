#!/usr/bin/env python3
"""
Claude Code 命令描述本地化工具

解决 Claude Code 显示英文命令描述的问题
通过直接更新 .md 文件的 YAML frontmatter 实现本地化显示
"""

import sys
import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import shutil

# 添加路径以导入模块
sys.path.insert(0, str(Path(__file__).parent.parent))

from SuperClaude.i18n import get_localizer


class ClaudeCodeLocalizer:
    """Claude Code 命令描述本地化器"""
    
    def __init__(self):
        self.localizer = get_localizer()
        
        # Claude Code 命令文件路径
        self.commands_dir = Path("/Users/ray/.claude/commands/sc")
        
        # 支持的命令列表
        self.commands = [
            'analyze', 'build', 'cleanup', 'design', 'document',
            'estimate', 'explain', 'git', 'i18n', 'implement', 
            'improve', 'index', 'load', 'spawn', 'task',
            'test', 'troubleshoot', 'workflow'
        ]
        
        # 备份目录
        self.backup_dir = Path("/Users/ray/workspace/sc/SuperClaude_Framework/backups/claude_commands")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def parse_markdown_file(self, file_path: Path) -> Tuple[Dict, str]:
        """
        解析 Markdown 文件的 YAML frontmatter 和内容
        
        Returns:
            (frontmatter_dict, content)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否有 YAML frontmatter
            if not content.startswith('---'):
                return {}, content
            
            # 分离 frontmatter 和 content
            parts = content.split('---', 2)
            if len(parts) < 3:
                return {}, content
                
            frontmatter_str = parts[1].strip()
            main_content = parts[2].lstrip('\n')
            
            # 简单解析 YAML frontmatter（避免依赖 yaml 库）
            frontmatter = {}
            for line in frontmatter_str.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    
                    if key == 'allowed-tools':
                        # 处理数组格式
                        value = value.strip('[]')
                        frontmatter[key] = [tool.strip() for tool in value.split(',')]
                    else:
                        frontmatter[key] = value
            
            return frontmatter, main_content
            
        except Exception as e:
            print(f"❌ 解析文件失败 {file_path}: {e}")
            return {}, ""
    
    def write_markdown_file(self, file_path: Path, frontmatter: Dict, content: str):
        """
        写入 Markdown 文件，包含 YAML frontmatter
        """
        try:
            # 构建 frontmatter 字符串
            frontmatter_lines = ['---']
            
            for key, value in frontmatter.items():
                if key == 'allowed-tools' and isinstance(value, list):
                    # 处理数组格式
                    tools_str = '[' + ', '.join(value) + ']'
                    frontmatter_lines.append(f'{key}: {tools_str}')
                else:
                    frontmatter_lines.append(f'{key}: "{value}"')
            
            frontmatter_lines.append('---')
            
            # 组合完整内容
            full_content = '\n'.join(frontmatter_lines) + '\n\n' + content
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
                
        except Exception as e:
            print(f"❌ 写入文件失败 {file_path}: {e}")
            raise
    
    def backup_command_files(self):
        """备份所有命令文件"""
        print("📦 备份原始命令文件...")
        
        for command in self.commands:
            src_file = self.commands_dir / f"{command}.md"
            if src_file.exists():
                backup_file = self.backup_dir / f"{command}.md.backup"
                shutil.copy2(src_file, backup_file)
                print(f"  ✅ 备份: {command}.md")
        
        print("📦 备份完成")
    
    def update_command_descriptions(self, target_locale: Optional[str] = None):
        """
        更新所有命令文件的描述为指定语言
        
        Args:
            target_locale: 目标语言代码，如 'zh_CN', 'en_US'。None 表示使用当前语言
        """
        if target_locale:
            success = self.localizer.set_locale(target_locale)
            if not success:
                print(f"❌ 切换到语言 {target_locale} 失败")
                return False
        
        current_locale = self.localizer.get_current_locale()
        locale_name = self._get_locale_name(current_locale)
        
        print(f"🌐 更新 Claude Code 命令描述为: {locale_name} ({current_locale})")
        print(f"📁 目标目录: {self.commands_dir}")
        
        if not self.commands_dir.exists():
            print(f"❌ 命令目录不存在: {self.commands_dir}")
            return False
        
        updated_count = 0
        failed_count = 0
        
        for command in self.commands:
            try:
                # 文件路径
                file_path = self.commands_dir / f"{command}.md"
                if not file_path.exists():
                    print(f"⚠️  文件不存在: {command}.md")
                    continue
                
                # 获取本地化描述
                desc_key = f'commands.{command}'
                localized_desc = self.localizer.get_text(desc_key)
                
                if not localized_desc or localized_desc == desc_key:
                    print(f"⚠️  未找到翻译: {command}")
                    continue
                
                # 解析文件
                frontmatter, content = self.parse_markdown_file(file_path)
                
                # 更新描述
                original_desc = frontmatter.get('description', '')
                frontmatter['description'] = localized_desc
                
                # 写回文件
                self.write_markdown_file(file_path, frontmatter, content)
                
                print(f"  ✅ {command}: {localized_desc}")
                updated_count += 1
                
            except Exception as e:
                print(f"❌ 更新失败 {command}: {e}")
                failed_count += 1
        
        print(f"\n📊 更新统计:")
        print(f"  ✅ 成功: {updated_count}")
        print(f"  ❌ 失败: {failed_count}")
        print(f"  📝 总计: {len(self.commands)}")
        
        if updated_count > 0:
            print(f"\n🎉 Claude Code 现在将显示{locale_name}命令描述！")
            print("💡 重启 Claude Code 以看到更改")
        
        return updated_count > 0
    
    def restore_from_backup(self):
        """从备份恢复命令文件"""
        print("🔄 从备份恢复命令文件...")
        
        restored_count = 0
        
        for command in self.commands:
            backup_file = self.backup_dir / f"{command}.md.backup"
            target_file = self.commands_dir / f"{command}.md"
            
            if backup_file.exists():
                shutil.copy2(backup_file, target_file)
                print(f"  ✅ 恢复: {command}.md")
                restored_count += 1
        
        print(f"🔄 恢复完成，共恢复 {restored_count} 个文件")
        return restored_count > 0
    
    def show_current_descriptions(self):
        """显示当前所有命令的描述"""
        current_locale = self.localizer.get_current_locale()
        locale_name = self._get_locale_name(current_locale)
        
        print(f"=== 当前 Claude Code 命令描述 ===")
        print(f"📍 当前语言: {locale_name} ({current_locale})")
        print(f"📁 读取目录: {self.commands_dir}")
        print()
        
        for command in sorted(self.commands):
            file_path = self.commands_dir / f"{command}.md"
            if file_path.exists():
                frontmatter, _ = self.parse_markdown_file(file_path)
                desc = frontmatter.get('description', '[无描述]')
                print(f"  /sc:{command:<12} {desc}")
            else:
                print(f"  /sc:{command:<12} [文件不存在]")
    
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
    """主函数 - 演示 Claude Code 本地化"""
    localizer = ClaudeCodeLocalizer()
    
    print("=== SuperClaude V4 - Claude Code 本地化工具 ===")
    print("🎯 解决 Claude Code 显示英文描述的问题")
    print()
    
    # 显示当前描述
    print("📋 当前状态:")
    localizer.show_current_descriptions()
    
    print("\n" + "="*60 + "\n")
    
    # 备份文件
    localizer.backup_command_files()
    
    print("\n" + "="*60 + "\n")
    
    # 更新为中文
    print("🚀 开始本地化...")
    success = localizer.update_command_descriptions('zh_CN')
    
    if success:
        print("\n" + "="*60 + "\n")
        
        # 显示更新后的描述
        print("📋 更新后状态:")
        localizer.show_current_descriptions()
        
        print("\n" + "="*60 + "\n")
        print("🎉 本地化完成！")
        print("💡 重启 Claude Code 以查看中文命令描述")
        print("🔄 如需恢复英文，运行: python claude_code_localizer.py --restore")
    
    return success


if __name__ == "__main__":
    import sys
    
    if "--restore" in sys.argv:
        localizer = ClaudeCodeLocalizer()
        localizer.restore_from_backup()
    elif "--english" in sys.argv:
        localizer = ClaudeCodeLocalizer()
        localizer.update_command_descriptions('en_US')
    else:
        main()