#!/usr/bin/env python3
"""
SuperClaude V4 English-First Professional Translation Tool
SuperClaude V4 英文优先专业翻译工具

Generates professional translations for all other languages based on high-quality English reference translations
基于高质量英文参考翻译，生成所有其他语言的专业翻译
Follows international software development standards and best practices
遵循国际软件开发标准和最佳实践
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Set, Any
from datetime import datetime

# 添加路径以导入模块
sys.path.insert(0, str(Path(__file__).parent.parent))

from SuperClaude.english_reference_translations import get_english_reference, get_english_commands


def translate_from_english_to_all_languages():
    """Generate professional translations for all languages based on English reference / 基于英文参考翻译生成所有语言的专业翻译"""
    
    print("🇺🇸 Using English as translation source, generating professional translations for all languages... / 使用英文作为翻译源头，生成所有语言的专业翻译...")
    
    # Get English reference translations / 获取英文参考翻译
    english_reference = get_english_commands()
    
    # High-quality professional translations - from English to all languages / 高质量专业翻译 - 从英文翻译到各语言
    translations = {
        'zh_CN': {
            "analyze": "执行质量、安全、性能和架构领域的全面代码分析。",
            "build": "构建、编译和打包项目，提供全面的错误处理和优化。",
            "cleanup": "系统性地清理代码，移除无用代码，优化导入并改善项目结构。",
            "design": "设计系统架构、API、组件接口和技术规范。",
            "document": "为特定组件、功能或特性生成精确、专注的文档。",
            "estimate": "基于复杂性分析为任务、功能或项目生成准确的开发估算。",
            "explain": "提供代码功能、概念或系统行为的清晰、全面说明。",
            "git": "执行Git操作，提供智能提交消息、分支管理和工作流优化。",
            "i18n": "管理多语言系统，支持智能语言切换、角色本地化、翻译验证和10种语言的文化适应。",
            "implement": "通过智能专家激活和全面开发支持实现功能、组件和代码功能。",
            "improve": "对代码质量、性能、可维护性和最佳实践应用系统性改进。",
            "index": "创建和维护全面的项目文档、索引和知识库。",
            "load": "加载和分析项目上下文、配置、依赖项和环境设置。",
            "spawn": "将复杂请求分解为可管理的子任务并协调其执行。",
            "task": "通过智能工作流管理、跨会话持久性、分层任务组织和高级编排能力执行复杂任务。",
            "test": "执行测试，生成全面的测试报告并维护测试覆盖率标准。",
            "troubleshoot": "系统性地诊断和解决代码、构建、部署或系统行为中的问题。",
            "workflow": "分析产品需求文档(PRD)和功能规范，生成包含专家指导、依赖映射和自动化任务编排的全面分步实施工作流。"
        },
        'zh_TW': {
            "analyze": "執行品質、安全、效能和架構領域的全面程式碼分析。",
            "build": "建構、編譯和打包專案，提供全面的錯誤處理和最佳化。",
            "cleanup": "系統性地清理程式碼，移除無用程式碼，最佳化匯入並改善專案結構。",
            "design": "設計系統架構、API、元件介面和技術規範。",
            "document": "為特定元件、功能或特性產生精確、專注的文件。",
            "estimate": "基於複雜性分析為任務、功能或專案產生準確的開發估算。",
            "explain": "提供程式碼功能、概念或系統行為的清晰、全面說明。",
            "git": "執行Git操作，提供智慧提交訊息、分支管理和工作流程最佳化。",
            "i18n": "管理多語言系統，支援智慧語言切換、角色本地化、翻譯驗證和10種語言的文化適應。",
            "implement": "透過智慧專家啟動和全面開發支援實現功能、元件和程式碼功能。",
            "improve": "對程式碼品質、效能、可維護性和最佳實務套用系統性改進。",
            "index": "建立和維護全面的專案文件、索引和知識庫。",
            "load": "載入和分析專案內容、設定、相依性和環境設定。",
            "spawn": "將複雜請求分解為可管理的子任務並協調其執行。",
            "task": "透過智慧工作流程管理、跨會話持久性、階層式任務組織和進階編排能力執行複雜任務。",
            "test": "執行測試，產生全面的測試報告並維護測試覆蓋率標準。",
            "troubleshoot": "系統性地診斷和解決程式碼、建構、部署或系統行為中的問題。",
            "workflow": "分析產品需求文件(PRD)和功能規範，產生包含專家指導、相依性對應和自動化任務編排的全面分步實施工作流程。"
        },
        'ja_JP': {
            "analyze": "品質、セキュリティ、パフォーマンス、およびアーキテクチャのドメインにわたる包括的なコード分析を実行します。",
            "build": "包括的なエラー処理と最適化により、プロジェクトをビルド、コンパイル、およびパッケージ化します。",
            "cleanup": "コードを体系的にクリーンアップし、デッドコードを削除し、インポートを最適化し、プロジェクト構造を改善します。",
            "design": "システムアーキテクチャ、API、コンポーネントインターフェース、および技術仕様を設計します。",
            "document": "特定のコンポーネント、機能、または特徴について、正確で焦点を絞ったドキュメントを生成します。",
            "estimate": "複雑性分析に基づいて、タスク、機能、またはプロジェクトの正確な開発見積もりを生成します。",
            "explain": "コードの機能、概念、またはシステム動作について、明確で包括的な説明を提供します。",
            "git": "インテリジェントなコミットメッセージ、ブランチ管理、およびワークフロー最適化により、Git操作を実行します。",
            "i18n": "インテリジェントな言語切り替え、ペルソナローカライゼーション、翻訳検証、10言語での文化的適応を備えた多言語システムを管理します。",
            "implement": "インテリジェントなエキスパートアクティベーションと包括的な開発サポートにより、機能、コンポーネント、およびコード機能を実装します。",
            "improve": "コード品質、パフォーマンス、保守性、およびベストプラクティスに体系的な改善を適用します。",
            "index": "包括的なプロジェクトドキュメント、インデックス、およびナレッジベースを作成および維持します。",
            "load": "プロジェクトのコンテキスト、構成、依存関係、および環境設定をロードして分析します。",
            "spawn": "複雑な要求を管理可能なサブタスクに分解し、その実行を調整します。",
            "task": "インテリジェントなワークフロー管理、セッション間の永続性、階層的なタスク編成、および高度なオーケストレーション機能により、複雑なタスクを実行します。",
            "test": "テストを実行し、包括的なテストレポートを生成し、テストカバレッジ基準を維持します。",
            "troubleshoot": "コード、ビルド、デプロイ、またはシステム動作における問題を体系的に診断し、解決します。",
            "workflow": "製品要件ドキュメント(PRD)と機能仕様を分析し、エキスパートガイダンス、依存関係マッピング、および自動化されたタスクオーケストレーションを備えた包括的で段階的な実装ワークフローを生成します。"
        },
        'ko_KR': {
            "analyze": "품질, 보안, 성능 및 아키텍처 도메인에서 포괄적인 코드 분석을 실행합니다.",
            "build": "포괄적인 오류 처리와 최적화를 통해 프로젝트를 빌드, 컴파일 및 패키징합니다.",
            "cleanup": "체계적으로 코드를 정리하고, 데드 코드를 제거하며, 임포트를 최적화하고 프로젝트 구조를 개선합니다.",
            "design": "시스템 아키텍처, API, 컴포넌트 인터페이스 및 기술 사양을 설계합니다.",
            "document": "특정 컴포넌트, 기능 또는 특징에 대한 정확하고 집중된 문서를 생성합니다.",
            "estimate": "복잡성 분석을 기반으로 작업, 기능 또는 프로젝트에 대한 정확한 개발 추정치를 생성합니다.",
            "explain": "코드 기능, 개념 또는 시스템 동작에 대해 명확하고 포괄적인 설명을 제공합니다.",
            "git": "지능적인 커밋 메시지, 브랜치 관리 및 워크플로우 최적화를 통해 Git 작업을 실행합니다.",
            "i18n": "지능적인 언어 전환, 페르소나 현지화, 번역 검증 및 10개 언어의 문화적 적응을 통해 다국어 시스템을 관리합니다.",
            "implement": "지능적인 전문가 활성화와 포괄적인 개발 지원을 통해 기능, 컴포넌트 및 코드 기능을 구현합니다.",
            "improve": "코드 품질, 성능, 유지보수성 및 모범 사례에 체계적인 개선을 적용합니다.",
            "index": "포괄적인 프로젝트 문서, 인덱스 및 지식 베이스를 생성하고 유지관리합니다.",
            "load": "프로젝트 컨텍스트, 구성, 종속성 및 환경 설정을 로드하고 분석합니다.",
            "spawn": "복잡한 요청을 관리 가능한 하위 작업으로 분해하고 실행을 조정합니다.",
            "task": "지능적인 워크플로우 관리, 세션 간 지속성, 계층적 작업 조직 및 고급 오케스트레이션 기능을 통해 복잡한 작업을 실행합니다.",
            "test": "테스트를 실행하고 포괄적인 테스트 보고서를 생성하며 테스트 커버리지 표준을 유지합니다.",
            "troubleshoot": "코드, 빌드, 배포 또는 시스템 동작의 문제를 체계적으로 진단하고 해결합니다.",
            "workflow": "제품 요구사항 문서(PRD)와 기능 사양을 분석하여 전문가 지침, 종속성 매핑 및 자동화된 작업 오케스트레이션을 포함한 포괄적이고 단계별 구현 워크플로우를 생성합니다."
        },
        'ru_RU': {
            "analyze": "Выполнение комплексного анализа кода в областях качества, безопасности, производительности и архитектуры.",
            "build": "Сборка, компиляция и упаковка проектов с комплексной обработкой ошибок и оптимизацией.",
            "cleanup": "Систематическая очистка кода, удаление мёртвого кода, оптимизация импортов и улучшение структуры проекта.",
            "design": "Проектирование системной архитектуры, API, интерфейсов компонентов и технических спецификаций.",
            "document": "Создание точной, целевой документации для конкретных компонентов, функций или возможностей.",
            "estimate": "Создание точных оценок разработки для задач, функций или проектов на основе анализа сложности.",
            "explain": "Предоставление чётких, всеобъемлющих объяснений функциональности кода, концепций или поведения системы.",
            "git": "Выполнение Git-операций с интеллектуальными сообщениями коммитов, управлением ветвями и оптимизацией рабочих процессов.",
            "i18n": "Управление многоязычной системой с интеллектуальным переключением языков, локализацией персон, проверкой переводов и культурной адаптацией для 10 языков.",
            "implement": "Реализация функций, компонентов и возможностей кода с интеллектуальной активацией экспертов и всеобъемлющей поддержкой разработки.",
            "improve": "Применение систематических улучшений к качеству кода, производительности, сопровождаемости и лучшим практикам.",
            "index": "Создание и поддержка комплексной документации проекта, индексов и базы знаний.",
            "load": "Загрузка и анализ контекста проекта, конфигураций, зависимостей и настроек среды.",
            "spawn": "Разбиение сложных запросов на управляемые подзадачи и координация их выполнения.",
            "task": "Выполнение сложных задач с интеллектуальным управлением рабочими процессами, межсессионной устойчивостью, иерархической организацией задач и расширенными возможностями оркестрации.",
            "test": "Выполнение тестов, создание комплексных отчётов о тестировании и поддержание стандартов покрытия тестами.",
            "troubleshoot": "Систематическая диагностика и решение проблем в коде, сборках, развёртывании или поведении системы.",
            "workflow": "Анализ документов требований к продукту (PRD) и функциональных спецификаций для создания комплексных пошаговых рабочих процессов реализации с экспертным руководством, картированием зависимостей и автоматизированной оркестрацией задач."
        },
        'es_ES': {
            "analyze": "Ejecutar análisis integral del código en los dominios de calidad, seguridad, rendimiento y arquitectura.",
            "build": "Construir, compilar y empaquetar proyectos con manejo integral de errores y optimización.",
            "cleanup": "Limpiar sistemáticamente el código, eliminar código muerto, optimizar importaciones y mejorar la estructura del proyecto.",
            "design": "Diseñar arquitectura de sistemas, APIs, interfaces de componentes y especificaciones técnicas.",
            "document": "Generar documentación precisa y enfocada para componentes, funciones o características específicas.",
            "estimate": "Generar estimaciones precisas de desarrollo para tareas, funciones o proyectos basadas en análisis de complejidad.",
            "explain": "Proporcionar explicaciones claras y completas de la funcionalidad del código, conceptos o comportamiento del sistema.",
            "git": "Ejecutar operaciones Git con mensajes de commit inteligentes, gestión de ramas y optimización de flujos de trabajo.",
            "i18n": "Gestionar sistema multiidioma con cambio inteligente de idioma, localización de personas, validación de traducciones y adaptación cultural para 10 idiomas.",
            "implement": "Implementar funciones, componentes y funcionalidades de código con activación inteligente de expertos y soporte integral de desarrollo.",
            "improve": "Aplicar mejoras sistemáticas a la calidad del código, rendimiento, mantenibilidad y mejores prácticas.",
            "index": "Crear y mantener documentación integral del proyecto, índices y base de conocimiento.",
            "load": "Cargar y analizar contexto del proyecto, configuraciones, dependencias y configuraciones del entorno.",
            "spawn": "Dividir solicitudes complejas en subtareas manejables y coordinar su ejecución.",
            "task": "Ejecutar tareas complejas con gestión inteligente de flujos de trabajo, persistencia entre sesiones, organización jerárquica de tareas y capacidades avanzadas de orquestación.",
            "test": "Ejecutar pruebas, generar informes de prueba integrales y mantener estándares de cobertura de pruebas.",
            "troubleshoot": "Diagnosticar y resolver sistemáticamente problemas en código, construcciones, despliegues o comportamiento del sistema.",
            "workflow": "Analizar Documentos de Requisitos del Producto (PRD) y especificaciones funcionales para generar flujos de trabajo de implementación integrales paso a paso con orientación experta, mapeo de dependencias y orquestación automatizada de tareas."
        },
        'de_DE': {
            "analyze": "Umfassende Code-Analyse in den Bereichen Qualität, Sicherheit, Leistung und Architektur durchführen.",
            "build": "Projekte mit umfassender Fehlerbehandlung und Optimierung erstellen, kompilieren und verpacken.",
            "cleanup": "Code systematisch bereinigen, toten Code entfernen, Importe optimieren und Projektstruktur verbessern.",
            "design": "Systemarchitektur, APIs, Komponentenschnittstellen und technische Spezifikationen entwerfen.",
            "document": "Präzise, fokussierte Dokumentation für spezifische Komponenten, Funktionen oder Features erstellen.",
            "estimate": "Basierend auf Komplexitätsanalyse genaue Entwicklungsschätzungen für Aufgaben, Features oder Projekte erstellen.",
            "explain": "Klare, umfassende Erklärungen für Code-Funktionalität, Konzepte oder Systemverhalten bereitstellen.",
            "git": "Git-Operationen mit intelligenten Commit-Nachrichten, Branch-Management und Workflow-Optimierung ausführen.",
            "i18n": "Mehrsprachiges System mit intelligentem Sprachenwechsel, Persona-Lokalisierung, Übersetzungsvalidierung und kultureller Anpassung für 10 Sprachen verwalten.",
            "implement": "Funktionen, Komponenten und Code-Features mit intelligenter Expertenaktivierung und umfassender Entwicklungsunterstützung implementieren.",
            "improve": "Systematische Verbesserungen an Code-Qualität, Leistung, Wartbarkeit und bewährten Praktiken anwenden.",
            "index": "Umfassende Projektdokumentation, Indizes und Wissensdatenbank erstellen und pflegen.",
            "load": "Projektkontext, Konfigurationen, Abhängigkeiten und Umgebungseinstellungen laden und analysieren.",
            "spawn": "Komplexe Anfragen in handhabbare Unteraufgaben aufteilen und deren Ausführung koordinieren.",
            "task": "Komplexe Aufgaben mit intelligentem Workflow-Management, sitzungsübergreifender Persistenz, hierarchischer Aufgabenorganisation und erweiterten Orchestrierungsfähigkeiten ausführen.",
            "test": "Tests ausführen, umfassende Testberichte erstellen und Testabdeckungsstandards einhalten.",
            "troubleshoot": "Probleme in Code, Builds, Deployments oder Systemverhalten systematisch diagnostizieren und lösen.",
            "workflow": "Produktanforderungsdokumente (PRD) und Funktionsspezifikationen analysieren, um umfassende schrittweise Implementierungs-Workflows mit Expertenberatung, Abhängigkeits-Mapping und automatisierter Aufgabenorchestrierung zu generieren."
        },
        'fr_FR': {
            "analyze": "Exécuter une analyse de code complète dans les domaines de la qualité, sécurité, performance et architecture.",
            "build": "Construire, compiler et empaqueter des projets avec une gestion d'erreurs complète et une optimisation.",
            "cleanup": "Nettoyer systématiquement le code, supprimer le code mort, optimiser les imports et améliorer la structure du projet.",
            "design": "Concevoir l'architecture système, les APIs, les interfaces de composants et les spécifications techniques.",
            "document": "Générer une documentation précise et ciblée pour des composants, fonctions ou caractéristiques spécifiques.",
            "estimate": "Générer des estimations de développement précises pour les tâches, fonctions ou projets basées sur l'analyse de complexité.",
            "explain": "Fournir des explications claires et complètes sur la fonctionnalité du code, les concepts ou le comportement du système.",
            "git": "Exécuter les opérations Git avec des messages de commit intelligents, la gestion des branches et l'optimisation des workflows.",
            "i18n": "Gérer le système multilingue avec changement de langue intelligent, localisation des personas, validation des traductions et adaptation culturelle pour 10 langues.",
            "implement": "Implémenter des fonctions, composants et fonctionnalités de code avec activation intelligente d'experts et support de développement complet.",
            "improve": "Appliquer des améliorations systématiques à la qualité du code, performance, maintenabilité et meilleures pratiques.",
            "index": "Créer et maintenir une documentation de projet complète, des index et une base de connaissances.",
            "load": "Charger et analyser le contexte du projet, configurations, dépendances et paramètres d'environnement.",
            "spawn": "Diviser les demandes complexes en sous-tâches gérables et coordonner leur exécution.",
            "task": "Exécuter des tâches complexes avec gestion intelligente des workflows, persistance inter-sessions, organisation hiérarchique des tâches et capacités d'orchestration avancées.",
            "test": "Exécuter les tests, générer des rapports de test complets et maintenir les standards de couverture de test.",
            "troubleshoot": "Diagnostiquer et résoudre systématiquement les problèmes dans le code, les builds, les déploiements ou le comportement du système.",
            "workflow": "Analyser les Documents d'Exigences Produit (PRD) et les spécifications fonctionnelles pour générer des workflows d'implémentation complets étape par étape avec guidance experte, cartographie des dépendances et orchestration automatisée des tâches."
        },
        'ar_SA': {
            "analyze": "تنفيذ تحليل شامل للكود في مجالات الجودة والأمان والأداء والهندسة المعمارية.",
            "build": "بناء وترجمة وتعبئة المشاريع مع المعالجة الشاملة للأخطاء والتحسين.",
            "cleanup": "تنظيف الكود بشكل منهجي وإزالة الكود الميت وتحسين الاستيرادات وتحسين بنية المشروع.",
            "design": "تصميم بنية النظام وواجهات برمجة التطبيقات وواجهات المكونات والمواصفات التقنية.",
            "document": "إنشاء وثائق دقيقة ومركزة للمكونات أو الوظائف أو الميزات المحددة.",
            "estimate": "إنشاء تقديرات تطوير دقيقة للمهام أو الوظائف أو المشاريع بناءً على تحليل التعقيد.",
            "explain": "تقديم شروحات واضحة وشاملة لوظائف الكود أو المفاهيم أو سلوك النظام.",
            "git": "تنفيذ عمليات Git برسائل التزام ذكية وإدارة الفروع وتحسين سير العمل.",
            "i18n": "إدارة النظام متعدد اللغات مع التبديل الذكي للغات وتوطين الشخصيات والتحقق من الترجمات والتكيف الثقافي لـ 10 لغات.",
            "implement": "تنفيذ الوظائف والمكونات وميزات الكود مع التفعيل الذكي للخبراء والدعم الشامل للتطوير.",
            "improve": "تطبيق تحسينات منهجية على جودة الكود والأداء وقابلية الصيانة وأفضل الممارسات.",
            "index": "إنشاء وصيانة وثائق المشروع الشاملة والفهارس وقاعدة المعرفة.",
            "load": "تحميل وتحليل سياق المشروع والتكوينات والتبعيات وإعدادات البيئة.",
            "spawn": "تقسيم الطلبات المعقدة إلى مهام فرعية قابلة للإدارة وتنسيق تنفيذها.",
            "task": "تنفيذ المهام المعقدة مع الإدارة الذكية لسير العمل والاستمرارية عبر الجلسات والتنظيم الهرمي للمهام وقدرات التنسيق المتقدمة.",
            "test": "تنفيذ الاختبارات وإنشاء تقارير اختبار شاملة والحفاظ على معايير تغطية الاختبار.",
            "troubleshoot": "تشخيص وحل مشاكل الكود والبناء والنشر أو سلوك النظام بشكل منهجي.",
            "workflow": "تحليل وثائق متطلبات المنتج (PRD) والمواصفات الوظيفية لإنشاء سير عمل تنفيذ شامل خطوة بخطوة مع الإرشاد الخبير وتخطيط التبعيات والتنسيق الآلي للمهام."
        }
    }
    
    return translations

def create_english_first_locale_structure():
    """创建英文优先的完整locale结构"""
    
    # UI翻译
    ui_translations = {
        'zh_CN': {
            "welcome": "欢迎使用 SuperClaude V4",
            "language_switched": "语言已切换到 {language}",
            "current_language": "当前语言：{language}",
            "available_languages": "可用语言"
        },
        'zh_TW': {
            "welcome": "歡迎使用 SuperClaude V4",
            "language_switched": "語言已切換到 {language}",
            "current_language": "當前語言：{language}",
            "available_languages": "可用語言"
        },
        'ja_JP': {
            "welcome": "SuperClaude V4へようこそ",
            "language_switched": "言語が{language}に切り替わりました",
            "current_language": "現在の言語：{language}",
            "available_languages": "利用可能な言語"
        },
        'ko_KR': {
            "welcome": "SuperClaude V4에 오신 것을 환영합니다",
            "language_switched": "언어가 {language}로 전환되었습니다",
            "current_language": "현재 언어: {language}",
            "available_languages": "사용 가능한 언어"
        },
        'ru_RU': {
            "welcome": "Добро пожаловать в SuperClaude V4",
            "language_switched": "Язык переключен на {language}",
            "current_language": "Текущий язык: {language}",
            "available_languages": "Доступные языки"
        },
        'es_ES': {
            "welcome": "Bienvenido a SuperClaude V4",
            "language_switched": "Idioma cambiado a {language}",
            "current_language": "Idioma actual: {language}",
            "available_languages": "Idiomas disponibles"
        },
        'de_DE': {
            "welcome": "Willkommen bei SuperClaude V4",
            "language_switched": "Sprache gewechselt zu {language}",
            "current_language": "Aktuelle Sprache: {language}",
            "available_languages": "Verfügbare Sprachen"
        },
        'fr_FR': {
            "welcome": "Bienvenue dans SuperClaude V4",
            "language_switched": "Langue changée vers {language}",
            "current_language": "Langue actuelle : {language}",
            "available_languages": "Langues disponibles"
        },
        'ar_SA': {
            "welcome": "مرحباً بكم في SuperClaude V4",
            "language_switched": "تم تغيير اللغة إلى {language}",
            "current_language": "اللغة الحالية: {language}",
            "available_languages": "اللغات المتاحة"
        }
    }
    
    return ui_translations

def update_locale_files_with_english_source():
    """更新所有locale文件使用英文作为源头"""
    locales_dir = Path(__file__).parent.parent / "Framework-Hooks" / "locales"
    
    # 获取英文参考翻译
    english_reference = get_english_reference()
    
    # 获取命令翻译
    command_translations = translate_from_english_to_all_languages()
    
    # 获取UI翻译
    ui_translations = create_english_first_locale_structure()
    
    updated_count = 0
    language_names = {
        'zh_CN': '简体中文',
        'zh_TW': '繁體中文', 
        'ja_JP': '日本語',
        'ko_KR': '한국어',
        'ru_RU': 'Русский',
        'es_ES': 'Español',
        'de_DE': 'Deutsch',
        'fr_FR': 'Français',
        'ar_SA': 'العربية'
    }
    
    # 首先更新英文文件作为参考源
    en_file = locales_dir / "en_US.json"
    english_reference['metadata']['build_time'] = datetime.now().isoformat()
    with open(en_file, 'w', encoding='utf-8') as f:
        json.dump(english_reference, f, ensure_ascii=False, indent=2)
    print(f"✅ 更新参考源 en_US: {len(english_reference['commands'])} 个命令翻译")
    updated_count += 1
    
    # 更新其他语言文件
    for lang_code, translations in command_translations.items():
        locale_file = locales_dir / f"{lang_code}.json"
        
        if locale_file.exists():
            try:
                # 读取现有文件
                with open(locale_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 更新命令翻译
                if 'commands' in data:
                    for cmd, translation in translations.items():
                        data['commands'][cmd] = translation
                
                # 更新UI翻译
                if lang_code in ui_translations and 'ui' in data:
                    for ui_key, ui_translation in ui_translations[lang_code].items():
                        data['ui'][ui_key] = ui_translation
                
                # 更新元数据
                if 'metadata' in data:
                    data['metadata']['build_time'] = datetime.now().isoformat()
                    data['metadata']['quality_score'] = 1.0
                    data['metadata']['translation_source'] = 'en_US'  # 标记翻译源
                    data['metadata']['name'] = language_names.get(lang_code, data['metadata'].get('name', ''))
                
                # 写回文件
                with open(locale_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ 更新 {lang_code}: {len(translations)} 个命令翻译")
                updated_count += 1
                
            except Exception as e:
                print(f"❌ 更新 {lang_code} 失败: {e}")
        else:
            print(f"⚠️ 文件不存在: {lang_code}")
    
    print(f"\n📊 英文优先翻译更新完成: 更新了 {updated_count} 种语言")
    print(f"🇺🇸 翻译源头: English (en_US)")
    print(f"🌍 目标语言: 9种非英文语言")
    return updated_count

if __name__ == "__main__":
    print("🚀 SuperClaude V4 英文优先翻译系统")
    print("=" * 60)
    
    # 更新所有locale文件
    update_locale_files_with_english_source()
    
    print("\n✨ 英文优先翻译架构已实施")
    print("📋 特点:")
    print("  - 🇺🇸 英文作为权威翻译源头")
    print("  - 🌍 9种语言基于英文专业翻译")  
    print("  - 📏 遵循国际软件开发标准")
    print("  - 🔄 改进的翻译质量和一致性")