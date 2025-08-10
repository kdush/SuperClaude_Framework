#!/usr/bin/env python3
"""
SuperClaude V4 安装器

处理 SuperClaude 框架到 Claude Code 的集成安装
"""

import os
import sys
import shutil
from pathlib import Path
from typing import Optional

from . import __version__


def show_version():
    """显示版本信息"""
    print(f"SuperClaude V4 {__version__}")
    print("Advanced AI Framework for Claude Code")
    print("https://github.com/kdush/SuperClaude_Framework")


def install_superclaude() -> bool:
    """
    安装 SuperClaude 到 Claude Code
    
    Returns:
        安装是否成功
    """
    print("=== SuperClaude V4 安装器 ===")
    print("🚀 开始安装 SuperClaude V4 到 Claude Code...")
    
    try:
        # 确定源目录和目标目录
        source_dir = Path(__file__).parent.parent
        claude_dir = Path.home() / ".claude"
        
        print(f"📁 源目录: {source_dir}")
        print(f"🎯 目标目录: {claude_dir}")
        
        if not claude_dir.exists():
            print("❌ Claude Code 配置目录不存在")
            print("💡 请先运行 Claude Code 创建配置目录")
            return False
        
        # 1. 复制 Framework-Hooks
        hooks_source = source_dir / "Framework-Hooks"
        hooks_target = claude_dir / "Framework-Hooks"
        
        if hooks_source.exists():
            print("📋 安装 Framework-Hooks...")
            if hooks_target.exists():
                print("  🔄 更新现有 Framework-Hooks")
                shutil.rmtree(hooks_target)
            shutil.copytree(hooks_source, hooks_target)
            print("  ✅ Framework-Hooks 安装完成")
        
        # 2. 复制核心配置文件
        core_files = {
            "Framework/Core/CLAUDE.md": "CLAUDE.md",
            "Framework/Core/FLAGS.md": "FLAGS.md", 
            "Framework/Core/PRINCIPLES.md": "PRINCIPLES.md",
            "Framework/Core/RULES.md": "RULES.md",
            "Framework/Core/ORCHESTRATOR.md": "ORCHESTRATOR.md"
        }
        
        print("📋 安装核心配置文件...")
        for src_file, dst_file in core_files.items():
            src_path = source_dir / src_file
            dst_path = claude_dir / dst_file
            
            if src_path.exists():
                shutil.copy2(src_path, dst_path)
                print(f"  ✅ {dst_file}")
        
        # 3. 创建命令目录
        commands_target = claude_dir / "commands" / "sc"
        commands_target.mkdir(parents=True, exist_ok=True)
        
        print("📋 安装命令文件...")
        commands_source = source_dir / "Framework" / "Commands"
        if commands_source.exists():
            for cmd_file in commands_source.glob("*.md"):
                dst_path = commands_target / cmd_file.name
                shutil.copy2(cmd_file, dst_path)
                print(f"  ✅ /sc:{cmd_file.stem}")
        
        # 4. 安装 SuperClaude 模块
        superclaude_target = claude_dir / "SuperClaude"
        superclaude_source = source_dir / "SuperClaude"
        
        print("📋 安装 SuperClaude 核心模块...")
        if superclaude_target.exists():
            shutil.rmtree(superclaude_target)
        shutil.copytree(superclaude_source, superclaude_target)
        print("  ✅ SuperClaude 模块安装完成")
        
        # 5. 验证安装
        print("\n🔍 验证安装...")
        
        # 检查关键文件
        key_files = [
            claude_dir / "CLAUDE.md",
            claude_dir / "Framework-Hooks" / "locales" / "zh_CN.json",
            claude_dir / "commands" / "sc" / "i18n.md",
            claude_dir / "SuperClaude" / "i18n.py"
        ]
        
        all_present = True
        for file_path in key_files:
            if file_path.exists():
                print(f"  ✅ {file_path.name}")
            else:
                print(f"  ❌ {file_path.name} 缺失")
                all_present = False
        
        if all_present:
            print("\n🎉 SuperClaude V4 安装成功！")
            print("💡 重启 Claude Code 以开始使用")
            print("🌐 使用 /sc:i18n switch zh_CN 切换到中文界面")
            
            # 初始化 i18n 系统
            try:
                sys.path.insert(0, str(superclaude_target))
                from i18n import get_localizer
                localizer = get_localizer()
                print(f"🔧 i18n 系统已初始化 - 当前语言: {localizer.get_current_locale()}")
            except Exception as e:
                print(f"⚠️  i18n 系统初始化警告: {e}")
            
            return True
        else:
            print("\n❌ 安装验证失败，部分文件缺失")
            return False
            
    except Exception as e:
        print(f"❌ 安装失败: {e}")
        return False


def uninstall_superclaude() -> bool:
    """
    卸载 SuperClaude
    
    Returns:
        卸载是否成功
    """
    print("=== SuperClaude V4 卸载器 ===")
    print("🗑️ 开始卸载 SuperClaude...")
    
    try:
        claude_dir = Path.home() / ".claude"
        
        # 要删除的目录和文件
        items_to_remove = [
            claude_dir / "Framework-Hooks",
            claude_dir / "SuperClaude", 
            claude_dir / "commands" / "sc",
            claude_dir / "CLAUDE.md",
            claude_dir / "FLAGS.md",
            claude_dir / "PRINCIPLES.md",
            claude_dir / "RULES.md",
            claude_dir / "ORCHESTRATOR.md"
        ]
        
        removed_count = 0
        for item in items_to_remove:
            if item.exists():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                print(f"  🗑️ 已删除: {item.name}")
                removed_count += 1
        
        if removed_count > 0:
            print(f"\n🎉 SuperClaude 卸载完成！共删除 {removed_count} 项")
        else:
            print("\n💡 SuperClaude 未安装或已经卸载")
        
        return True
        
    except Exception as e:
        print(f"❌ 卸载失败: {e}")
        return False