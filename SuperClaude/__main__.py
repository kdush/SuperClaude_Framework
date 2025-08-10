#!/usr/bin/env python3
"""
SuperClaude V4 主入口点

提供命令行界面和安装功能
"""

import sys
import argparse
from pathlib import Path

from .core import SuperClaudeCore
from .installer import install_superclaude, show_version

def main():
    """SuperClaude V4 主函数"""
    parser = argparse.ArgumentParser(
        prog='superclaude',
        description='SuperClaude V4 - Advanced AI Framework for Claude Code',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--version', '-v',
        action='store_true',
        help='显示版本信息'
    )
    
    parser.add_argument(
        '--install',
        action='store_true',
        help='安装 SuperClaude 到 Claude Code'
    )
    
    parser.add_argument(
        '--language', '-l',
        default='zh_CN',
        help='设置默认语言 (default: zh_CN)'
    )
    
    args = parser.parse_args()
    
    if args.version:
        show_version()
        return 0
    
    if args.install:
        success = install_superclaude()
        return 0 if success else 1
    
    # 默认显示帮助
    parser.print_help()
    return 0

if __name__ == '__main__':
    sys.exit(main())