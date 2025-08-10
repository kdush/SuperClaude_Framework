#!/usr/bin/env python3
"""
SuperClaude V4 英文参考翻译

高质量的英文技术翻译，遵循国际软件开发标准和最佳实践
作为所有其他语言翻译的权威源头
"""

# 英文参考翻译 - 作为翻译架构的新源头
ENGLISH_REFERENCE_COMMANDS = {
    "analyze": "Execute comprehensive code analysis across quality, security, performance, and architecture domains.",
    "build": "Build, compile, and package projects with comprehensive error handling and optimization.", 
    "cleanup": "Systematically clean up code, remove dead code, optimize imports, and improve project structure.",
    "design": "Design system architecture, APIs, component interfaces, and technical specifications.",
    "document": "Generate precise, focused documentation for specific components, functions, or features.",
    "estimate": "Generate accurate development estimates for tasks, features, or projects based on complexity analysis.",
    "explain": "Provide clear, comprehensive explanations of code functionality, concepts, or system behavior.",
    "git": "Execute Git operations with intelligent commit messages, branch management, and workflow optimization.",
    "i18n": "Manage multi-language system with intelligent language switching, persona localization, translation validation, and cultural adaptation across 10 languages.",
    "implement": "Implement features, components, and code functionality with intelligent expert activation and comprehensive development support.",
    "improve": "Apply systematic improvements to code quality, performance, maintainability, and best practices.",
    "index": "Create and maintain comprehensive project documentation, indexes, and knowledge base.",
    "load": "Load and analyze project context, configurations, dependencies, and environment settings.",
    "spawn": "Break down complex requests into manageable subtasks and coordinate their execution.",
    "task": "Execute complex tasks with intelligent workflow management, cross-session persistence, hierarchical task organization, and advanced orchestration capabilities.",
    "test": "Execute tests, generate comprehensive test reports, and maintain test coverage standards.",
    "troubleshoot": "Systematically diagnose and resolve issues in code, builds, deployments, or system behavior.",
    "workflow": "Analyze Product Requirements Documents (PRDs) and feature specifications to generate comprehensive, step-by-step implementation workflows with expert guidance, dependency mapping, and automated task orchestration."
}

# 英文参考UI翻译
ENGLISH_REFERENCE_UI = {
    "welcome": "Welcome to SuperClaude V4",
    "language_switched": "Language switched to {language}",
    "current_language": "Current language: {language}",
    "available_languages": "Available languages"
}

# 英文参考错误消息
ENGLISH_REFERENCE_ERRORS = {
    "file_not_found": "File not found: {filename}",
    "invalid_language": "Unsupported language code: {code}",
    "switch_failed": "Language switch failed"
}

# 英文参考角色描述
ENGLISH_REFERENCE_PERSONAS = {
    "architect": {
        "name": "System Architect",
        "description": "Expert focused on system design and long-term architectural decisions"
    },
    "frontend": {
        "name": "Frontend Specialist", 
        "description": "User experience expert and accessibility advocate"
    },
    "backend": {
        "name": "Backend Engineer",
        "description": "Reliability engineer and API specialist"
    },
    "security": {
        "name": "Security Expert",
        "description": "Threat modeling specialist and vulnerability assessment expert"
    },
    "qa": {
        "name": "Quality Assurance",
        "description": "Quality advocate and testing specialist"
    },
    "devops": {
        "name": "DevOps Engineer", 
        "description": "Infrastructure specialist and deployment automation expert"
    }
}

# 英文参考系统消息
ENGLISH_REFERENCE_SYSTEM = {
    "initializing": "Initializing...",
    "ready": "System ready",
    "performance": "Performance metrics",
    "cache_hit_rate": "Cache hit rate",
    "avg_response_time": "Average response time"
}

# 完整英文参考翻译结构
ENGLISH_REFERENCE_LOCALE = {
    "metadata": {
        "language": "en_US",
        "name": "English (US)",
        "version": "1.0.0",
        "total_items": 42,
        "build_cost": 0.000001,
        "quality_score": 1.0,
        "is_reference": True,  # 标记为参考源
        "translation_source": True  # 标记为翻译源头
    },
    "commands": ENGLISH_REFERENCE_COMMANDS,
    "ui": ENGLISH_REFERENCE_UI,
    "errors": ENGLISH_REFERENCE_ERRORS,
    "personas": ENGLISH_REFERENCE_PERSONAS,
    "system": ENGLISH_REFERENCE_SYSTEM
}

def get_english_reference() -> dict:
    """获取完整的英文参考翻译"""
    return ENGLISH_REFERENCE_LOCALE

def get_english_commands() -> dict:
    """获取英文命令翻译"""
    return ENGLISH_REFERENCE_COMMANDS

if __name__ == "__main__":
    import json
    print("🇺🇸 SuperClaude V4 English Reference Translations")
    print("=" * 50)
    
    reference = get_english_reference()
    
    print(f"📊 Total items: {reference['metadata']['total_items']}")
    print(f"📊 Quality score: {reference['metadata']['quality_score']}")
    print(f"🔄 Translation source: {reference['metadata']['translation_source']}")
    
    print("\n📋 Command Translations:")
    for cmd, desc in reference['commands'].items():
        print(f"  ✅ {cmd}: {desc}")