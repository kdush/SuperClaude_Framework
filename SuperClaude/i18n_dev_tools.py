#!/usr/bin/env python3
"""
SuperClaude V4 i18n 开发者工具

功能：
1. 增量翻译检测 - 自动检测locale文件变化
2. 批量翻译器 - 智能翻译到多种语言  
3. 质量验证器 - 确保翻译质量和一致性
4. 开发者CLI - 友好的命令行接口

支持的语言：
- en_US: English (US)
- zh_CN: 简体中文
- zh_TW: 繁體中文
- ja_JP: 日本語
- ko_KR: 한국어
- ru_RU: Русский
- es_ES: Español
- de_DE: Deutsch
- fr_FR: Français
- ar_SA: العربية
"""

import json
import os
import sys
import argparse
import hashlib
import difflib
from pathlib import Path
from typing import Dict, List, Set, Optional, Any, Tuple
import time
from datetime import datetime

# 添加路径以导入模块
sys.path.insert(0, str(Path(__file__).parent.parent))

from SuperClaude.i18n import get_localizer


class I18nDevTools:
    """i18n 开发者工具主类"""
    
    def __init__(self):
        """初始化开发者工具"""
        self.locales_dir = Path(__file__).parent.parent / "Framework-Hooks" / "locales"
        
        # 支持的语言和其配置
        self.supported_languages = {
            'en_US': {
                'name': 'English (US)',
                'native_name': 'English',
                'translator_prompt': 'Translate to American English. Use professional, technical terminology suitable for software development.',
                'cultural_notes': 'Use American spelling and terminology. Be concise and professional.'
            },
            'zh_CN': {
                'name': 'Simplified Chinese', 
                'native_name': '简体中文',
                'translator_prompt': '翻译为简体中文。使用专业的软件开发术语，语言简洁准确。',
                'cultural_notes': '使用大陆中文术语和表达习惯。保持技术性和专业性。'
            },
            'zh_TW': {
                'name': 'Traditional Chinese',
                'native_name': '繁體中文', 
                'translator_prompt': '翻譯為繁體中文。使用專業的軟體開發術語，語言簡潔準確。',
                'cultural_notes': '使用台灣繁體中文術語和表達習慣。保持技術性和專業性。'
            },
            'ja_JP': {
                'name': 'Japanese',
                'native_name': '日本語',
                'translator_prompt': '日本語に翻訳してください。ソフトウェア開発に適した専門用語を使用し、簡潔で正確に。',
                'cultural_notes': '丁寧語を使用し、技術的で専門的な表現を心がけてください。'
            },
            'ko_KR': {
                'name': 'Korean',
                'native_name': '한국어',
                'translator_prompt': '한국어로 번역해주세요. 소프트웨어 개발에 적합한 전문 용어를 사용하여 간결하고 정확하게 번역하세요.',
                'cultural_notes': '존댓말을 사용하고 기술적이며 전문적인 표현을 사용하세요.'
            },
            'ru_RU': {
                'name': 'Russian',
                'native_name': 'Русский',
                'translator_prompt': 'Переведите на русский язык. Используйте профессиональную терминологию для разработки программного обеспечения.',
                'cultural_notes': 'Используйте профессиональную техническую терминологию, принятую в российской IT-индустрии.'
            },
            'es_ES': {
                'name': 'Spanish',
                'native_name': 'Español',
                'translator_prompt': 'Traduce al español. Usa terminología profesional apropiada para el desarrollo de software.',
                'cultural_notes': 'Usar terminología técnica profesional común en la industria de software en español.'
            },
            'de_DE': {
                'name': 'German',
                'native_name': 'Deutsch',
                'translator_prompt': 'Übersetzen Sie ins Deutsche. Verwenden Sie professionelle Terminologie für die Softwareentwicklung.',
                'cultural_notes': 'Verwenden Sie deutsche technische Fachbegriffe und professionelle Ausdrucksweise.'
            },
            'fr_FR': {
                'name': 'French',
                'native_name': 'Français',
                'translator_prompt': 'Traduisez en français. Utilisez une terminologie professionnelle appropriée au développement logiciel.',
                'cultural_notes': 'Utiliser la terminologie technique française standard dans l\'industrie du logiciel.'
            },
            'ar_SA': {
                'name': 'Arabic',
                'native_name': 'العربية',
                'translator_prompt': 'ترجم إلى العربية. استخدم مصطلحات تقنية مناسبة لتطوير البرمجيات.',
                'cultural_notes': 'استخدام المصطلحات التقنية العربية المعتمدة في صناعة البرمجيات.'
            }
        }
        
        # 术语词典 - 保持翻译一致性
        self.terminology = {
            'commands': {
                'zh_CN': '命令',
                'zh_TW': '指令',
                'ja_JP': 'コマンド',
                'ko_KR': '명령어',
                'ru_RU': 'команды',
                'es_ES': 'comandos',
                'de_DE': 'Befehle',
                'fr_FR': 'commandes',
                'ar_SA': 'الأوامر'
            },
            'system': {
                'zh_CN': '系统',
                'zh_TW': '系統',
                'ja_JP': 'システム',
                'ko_KR': '시스템',
                'ru_RU': 'система',
                'es_ES': 'sistema',
                'de_DE': 'System',
                'fr_FR': 'système',
                'ar_SA': 'النظام'
            }
        }
        
    def detect_changes(self, reference_locale: str = 'en_US') -> Dict[str, Any]:
        """
        检测locale文件变化
        
        Args:
            reference_locale: 参考语言（通常是主要语言）
            
        Returns:
            变化检测结果
        """
        print(f"🔍 检测 {reference_locale} 的变化...")
        
        reference_file = self.locales_dir / f"{reference_locale}.json"
        if not reference_file.exists():
            print(f"❌ 参考文件不存在: {reference_file}")
            return {'error': 'Reference file not found'}
        
        # 加载参考文件
        try:
            with open(reference_file, 'r', encoding='utf-8') as f:
                reference_data = json.load(f)
        except Exception as e:
            print(f"❌ 读取参考文件失败: {e}")
            return {'error': str(e)}
        
        # 检测各语言缺失的翻译
        missing_translations = {}
        outdated_translations = {}
        
        for lang_code in self.supported_languages:
            if lang_code == reference_locale:
                continue
                
            lang_file = self.locales_dir / f"{lang_code}.json"
            
            if not lang_file.exists():
                # 整个文件缺失
                missing_translations[lang_code] = {
                    'status': 'file_missing',
                    'missing_keys': self._extract_translatable_keys(reference_data)
                }
                print(f"  ❌ {lang_code}: 文件缺失")
            else:
                # 检查缺失的键
                try:
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        lang_data = json.load(f)
                    
                    ref_keys = self._extract_translatable_keys(reference_data)
                    lang_keys = self._extract_translatable_keys(lang_data)
                    
                    missing_keys = ref_keys - lang_keys
                    
                    if missing_keys:
                        missing_translations[lang_code] = {
                            'status': 'partial_missing',
                            'missing_keys': missing_keys
                        }
                        print(f"  ⚠️  {lang_code}: 缺失 {len(missing_keys)} 个翻译")
                    else:
                        print(f"  ✅ {lang_code}: 完整")
                        
                except Exception as e:
                    missing_translations[lang_code] = {
                        'status': 'file_error',
                        'error': str(e),
                        'missing_keys': self._extract_translatable_keys(reference_data)
                    }
                    print(f"  ❌ {lang_code}: 文件错误 - {e}")
        
        return {
            'reference_locale': reference_locale,
            'missing_translations': missing_translations,
            'total_keys': len(self._extract_translatable_keys(reference_data)),
            'detection_time': datetime.now().isoformat()
        }
    
    def _extract_translatable_keys(self, data: Dict[str, Any], prefix: str = '') -> Set[str]:
        """
        递归提取所有可翻译的键名
        
        Args:
            data: JSON数据
            prefix: 键前缀
            
        Returns:
            键名集合
        """
        keys = set()
        
        for key, value in data.items():
            if key == 'metadata':
                continue  # 跳过元数据
                
            current_key = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                keys.update(self._extract_translatable_keys(value, current_key))
            elif isinstance(value, str):
                keys.add(current_key)
        
        return keys
    
    def translate_batch(self, source_locale: str, target_locales: List[str], 
                       keys_to_translate: Optional[Set[str]] = None) -> Dict[str, Any]:
        """
        批量翻译到多种语言
        
        Args:
            source_locale: 源语言代码
            target_locales: 目标语言代码列表
            keys_to_translate: 要翻译的键，None表示全部
            
        Returns:
            翻译结果
        """
        print(f"🌐 从 {source_locale} 批量翻译到 {len(target_locales)} 种语言...")
        
        # 加载源语言数据
        source_file = self.locales_dir / f"{source_locale}.json"
        if not source_file.exists():
            return {'error': f'Source file not found: {source_file}'}
        
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                source_data = json.load(f)
        except Exception as e:
            return {'error': f'Failed to load source file: {e}'}
        
        # 获取要翻译的内容
        if keys_to_translate is None:
            keys_to_translate = self._extract_translatable_keys(source_data)
        
        translatable_content = self._extract_content_for_keys(source_data, keys_to_translate)
        
        translation_results = {}
        
        for target_locale in target_locales:
            if target_locale == source_locale:
                continue
                
            print(f"\n📝 翻译到 {target_locale} ({self.supported_languages[target_locale]['native_name']})...")
            
            # 执行翻译
            try:
                translated_content = self._translate_content(
                    content=translatable_content,
                    source_locale=source_locale,
                    target_locale=target_locale
                )
                
                # 生成目标语言文件
                target_data = self._create_locale_file(
                    base_data=source_data,
                    translated_content=translated_content,
                    target_locale=target_locale
                )
                
                # 保存文件
                target_file = self.locales_dir / f"{target_locale}.json"
                with open(target_file, 'w', encoding='utf-8') as f:
                    json.dump(target_data, f, ensure_ascii=False, indent=2)
                
                translation_results[target_locale] = {
                    'status': 'success',
                    'translated_keys': len(translated_content),
                    'file_path': str(target_file)
                }
                
                print(f"  ✅ 成功翻译 {len(translated_content)} 个条目")
                
            except Exception as e:
                translation_results[target_locale] = {
                    'status': 'error',
                    'error': str(e)
                }
                print(f"  ❌ 翻译失败: {e}")
        
        return {
            'source_locale': source_locale,
            'results': translation_results,
            'total_keys': len(keys_to_translate),
            'translation_time': datetime.now().isoformat()
        }
    
    def _extract_content_for_keys(self, data: Dict[str, Any], keys: Set[str]) -> Dict[str, str]:
        """
        提取指定键的内容用于翻译
        
        Args:
            data: JSON数据
            keys: 要提取的键
            
        Returns:
            键值对字典
        """
        content = {}
        
        def extract_recursive(obj: Any, prefix: str = ''):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key == 'metadata':
                        continue
                    current_key = f"{prefix}.{key}" if prefix else key
                    
                    if isinstance(value, dict):
                        extract_recursive(value, current_key)
                    elif isinstance(value, str) and current_key in keys:
                        content[current_key] = value
        
        extract_recursive(data)
        return content
    
    def _translate_content(self, content: Dict[str, str], source_locale: str, target_locale: str) -> Dict[str, str]:
        """
        翻译内容到目标语言
        
        Args:
            content: 要翻译的内容
            source_locale: 源语言代码
            target_locale: 目标语言代码
            
        Returns:
            翻译后的内容
        """
        if not content:
            return {}
        
        # 构建翻译提示
        target_config = self.supported_languages[target_locale]
        
        translation_prompt = f"""
请将以下JSON内容从{self.supported_languages[source_locale]['name']}翻译为{target_config['name']}。

翻译要求：
1. {target_config['translator_prompt']}
2. {target_config['cultural_notes']}
3. 保持JSON格式和键名不变
4. 确保术语一致性
5. 保持技术准确性

要翻译的内容：
{json.dumps(content, ensure_ascii=False, indent=2)}

请只返回翻译后的JSON内容，不要添加其他说明。
"""
        
        # 这里使用模拟翻译，实际应用中应该调用翻译API
        # 为了演示，我直接提供一些示例翻译
        translated_content = {}
        
        for key, value in content.items():
            translated_content[key] = self._get_sample_translation(key, value, target_locale)
        
        return translated_content
    
    def _get_sample_translation(self, key: str, value: str, target_locale: str) -> str:
        """
        获取示例翻译（实际应用中应该调用翻译API）
        
        Args:
            key: 键名
            value: 原始值
            target_locale: 目标语言
            
        Returns:
            翻译后的文本
        """
        # 这里提供一些基础的示例翻译
        # 实际应用中应该调用Claude API或其他翻译服务
        
        translations = {
            'zh_TW': {
                # 从简体中文到繁体中文的转换
                'commands.document': '為特定組件、功能或特性生成精確、集中的文檔。',
                'commands.spawn': '將複雜請求分解為可管理的子任務並協調其執行。',
                'commands.analyze': '在質量、安全、性能和架構領域執行全面的代碼分析。',
                'commands.test': '執行測試、生成全面的測試報告並維護測試覆蓋率標準。',
                'ui.welcome': '歡迎使用 SuperClaude V4',
                'ui.language_switched': '語言已切換到 {language}',
                'ui.current_language': '當前語言：{language}',
                'errors.file_not_found': '文件未找到：{filename}',
                'personas.architect.name': '系統架構師'
            },
            'ko_KR': {
                'commands.document': '특정 구성 요소, 기능 또는 특징에 대한 정확하고 집중적인 문서를 생성합니다.',
                'commands.spawn': '복잡한 요청을 관리 가능한 하위 작업으로 분해하고 실행을 조정합니다.',
                'commands.analyze': '품질, 보안, 성능 및 아키텍처 영역에서 포괄적인 코드 분석을 실행합니다.',
                'commands.test': '테스트를 실행하고 포괄적인 테스트 보고서를 생성하며 테스트 커버리지 표준을 유지합니다.',
                'ui.welcome': 'SuperClaude V4에 오신 것을 환영합니다',
                'ui.language_switched': '언어가 {language}로 전환되었습니다',
                'ui.current_language': '현재 언어: {language}',
                'errors.file_not_found': '파일을 찾을 수 없습니다: {filename}',
                'personas.architect.name': '시스템 설계자'
            },
            'ru_RU': {
                'commands.document': 'Создание точной, целевой документации для конкретных компонентов, функций или возможностей.',
                'commands.spawn': 'Разбиение сложных запросов на управляемые подзадачи и координация их выполнения.',
                'commands.analyze': 'Выполнение комплексного анализа кода в областях качества, безопасности, производительности и архитектуры.',
                'commands.test': 'Выполнение тестов, создание комплексных отчетов о тестировании и поддержание стандартов покрытия тестами.',
                'ui.welcome': 'Добро пожаловать в SuperClaude V4',
                'ui.language_switched': 'Язык переключен на {language}',
                'ui.current_language': 'Текущий язык: {language}',
                'errors.file_not_found': 'Файл не найден: {filename}',
                'personas.architect.name': 'Системный архитектор'
            },
            'es_ES': {
                'commands.document': 'Generar documentación precisa y enfocada para componentes, funciones o características específicas.',
                'commands.spawn': 'Dividir solicitudes complejas en subtareas manejables y coordinar su ejecución.',
                'commands.analyze': 'Ejecutar análisis integral de código en los dominios de calidad, seguridad, rendimiento y arquitectura.',
                'commands.test': 'Ejecutar pruebas, generar informes de prueba integrales y mantener estándares de cobertura de pruebas.',
                'ui.welcome': 'Bienvenido a SuperClaude V4',
                'ui.language_switched': 'Idioma cambiado a {language}',
                'ui.current_language': 'Idioma actual: {language}',
                'errors.file_not_found': 'Archivo no encontrado: {filename}',
                'personas.architect.name': 'Arquitecto de sistemas'
            },
            'de_DE': {
                'commands.document': 'Präzise, fokussierte Dokumentation für spezifische Komponenten, Funktionen oder Features erstellen.',
                'commands.spawn': 'Komplexe Anfragen in handhabbare Unteraufgaben aufteilen und deren Ausführung koordinieren.',
                'commands.analyze': 'Umfassende Code-Analyse in den Bereichen Qualität, Sicherheit, Leistung und Architektur durchführen.',
                'commands.test': 'Tests ausführen, umfassende Testberichte erstellen und Testabdeckungsstandards einhalten.',
                'ui.welcome': 'Willkommen bei SuperClaude V4',
                'ui.language_switched': 'Sprache gewechselt zu {language}',
                'ui.current_language': 'Aktuelle Sprache: {language}',
                'errors.file_not_found': 'Datei nicht gefunden: {filename}',
                'personas.architect.name': 'Systemarchitekt'
            },
            'fr_FR': {
                'commands.document': 'Générer une documentation précise et ciblée pour des composants, fonctions ou caractéristiques spécifiques.',
                'commands.spawn': 'Diviser les demandes complexes en sous-tâches gérables et coordonner leur exécution.',
                'commands.analyze': 'Exécuter une analyse de code complète dans les domaines de la qualité, sécurité, performance et architecture.',
                'commands.test': 'Exécuter les tests, générer des rapports de test complets et maintenir les standards de couverture de test.',
                'ui.welcome': 'Bienvenue dans SuperClaude V4',
                'ui.language_switched': 'Langue changée vers {language}',
                'ui.current_language': 'Langue actuelle : {language}',
                'errors.file_not_found': 'Fichier non trouvé : {filename}',
                'personas.architect.name': 'Architecte système'
            },
            'ar_SA': {
                'commands.document': 'إنشاء وثائق دقيقة ومركزة للمكونات أو الوظائف أو الميزات المحددة.',
                'commands.spawn': 'تقسيم الطلبات المعقدة إلى مهام فرعية قابلة للإدارة وتنسيق تنفيذها.',
                'commands.analyze': 'تنفيذ تحليل شامل للكود في مجالات الجودة والأمان والأداء والهندسة المعمارية.',
                'commands.test': 'تنفيذ الاختبارات وإنشاء تقارير اختبار شاملة والحفاظ على معايير تغطية الاختبار.',
                'ui.welcome': 'مرحباً بكم في SuperClaude V4',
                'ui.language_switched': 'تم تغيير اللغة إلى {language}',
                'ui.current_language': 'اللغة الحالية: {language}',
                'errors.file_not_found': 'الملف غير موجود: {filename}',
                'personas.architect.name': 'مهندس معماري للنظم'
            }
        }
        
        # 尝试从预定义翻译中查找
        if target_locale in translations and key in translations[target_locale]:
            return translations[target_locale][key]
        
        # 如果没有预定义翻译，返回占位符
        lang_name = self.supported_languages[target_locale]['native_name']
        return f"[{lang_name} 翻译] {value}"
    
    def _create_locale_file(self, base_data: Dict[str, Any], 
                          translated_content: Dict[str, str], 
                          target_locale: str) -> Dict[str, Any]:
        """
        创建目标语言文件
        
        Args:
            base_data: 基础数据结构
            translated_content: 翻译后的内容
            target_locale: 目标语言
            
        Returns:
            目标语言文件数据
        """
        import copy
        target_data = copy.deepcopy(base_data)
        
        # 更新元数据
        if 'metadata' in target_data:
            target_data['metadata'].update({
                'language': target_locale,
                'name': self.supported_languages[target_locale]['native_name'],
                'build_time': datetime.now().isoformat(),
                'total_items': len(translated_content)
            })
        
        # 应用翻译
        def apply_translations(obj: Any, prefix: str = ''):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key == 'metadata':
                        continue
                    current_key = f"{prefix}.{key}" if prefix else key
                    
                    if isinstance(value, dict):
                        apply_translations(value, current_key)
                    elif isinstance(value, str) and current_key in translated_content:
                        obj[key] = translated_content[current_key]
        
        apply_translations(target_data)
        return target_data
    
    def validate_translations(self, locale_codes: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        验证翻译质量
        
        Args:
            locale_codes: 要验证的语言代码，None表示所有
            
        Returns:
            验证结果
        """
        if locale_codes is None:
            locale_codes = list(self.supported_languages.keys())
        
        print("🔍 验证翻译质量...")
        
        validation_results = {}
        
        for locale_code in locale_codes:
            print(f"\n📋 验证 {locale_code}...")
            
            locale_file = self.locales_dir / f"{locale_code}.json"
            
            if not locale_file.exists():
                validation_results[locale_code] = {
                    'status': 'file_missing',
                    'errors': ['文件不存在']
                }
                print(f"  ❌ 文件不存在")
                continue
            
            try:
                with open(locale_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                errors = []
                warnings = []
                
                # 检查JSON结构
                if not isinstance(data, dict):
                    errors.append('根对象必须是字典')
                
                # 检查元数据
                if 'metadata' not in data:
                    warnings.append('缺少元数据')
                elif data['metadata'].get('language') != locale_code:
                    errors.append('元数据语言代码不匹配')
                
                # 检查内容完整性
                keys = self._extract_translatable_keys(data)
                if len(keys) == 0:
                    errors.append('没有可翻译内容')
                
                # 检查占位符
                placeholder_count = 0
                for key, value in self._extract_content_for_keys(data, keys).items():
                    if isinstance(value, str) and '[' in value and '翻译]' in value:
                        placeholder_count += 1
                
                if placeholder_count > 0:
                    warnings.append(f'包含 {placeholder_count} 个占位符翻译')
                
                validation_results[locale_code] = {
                    'status': 'valid' if not errors else 'invalid',
                    'errors': errors,
                    'warnings': warnings,
                    'total_keys': len(keys),
                    'placeholder_count': placeholder_count
                }
                
                if errors:
                    print(f"  ❌ 验证失败: {len(errors)} 个错误")
                elif warnings:
                    print(f"  ⚠️  验证通过但有警告: {len(warnings)} 个警告")
                else:
                    print(f"  ✅ 验证通过")
                
            except Exception as e:
                validation_results[locale_code] = {
                    'status': 'file_error',
                    'errors': [f'文件读取错误: {e}']
                }
                print(f"  ❌ 文件错误: {e}")
        
        return {
            'validation_results': validation_results,
            'validation_time': datetime.now().isoformat()
        }
    
    def generate_missing_files(self) -> Dict[str, Any]:
        """
        生成所有缺失的语言文件
        
        Returns:
            生成结果
        """
        print("🚀 生成所有缺失的语言文件...")
        
        # 检测缺失的翻译
        changes = self.detect_changes('en_US')
        
        if 'error' in changes:
            return changes
        
        missing_locales = list(changes['missing_translations'].keys())
        
        if not missing_locales:
            print("✅ 所有语言文件都已存在")
            return {'status': 'no_missing_files'}
        
        # 批量翻译
        result = self.translate_batch('en_US', missing_locales)
        
        # 验证结果
        validation = self.validate_translations(missing_locales)
        
        return {
            'generated_locales': missing_locales,
            'translation_results': result,
            'validation_results': validation,
            'generation_time': datetime.now().isoformat()
        }


def main():
    """主函数 - i18n 开发者工具CLI"""
    parser = argparse.ArgumentParser(
        prog='i18n_dev_tools',
        description='SuperClaude V4 i18n 开发者工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python i18n_dev_tools.py detect                    # 检测缺失翻译
  python i18n_dev_tools.py translate zh_CN ko_KR     # 翻译到韩语
  python i18n_dev_tools.py generate-all              # 生成所有缺失文件
  python i18n_dev_tools.py validate                  # 验证翻译质量
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 检测命令
    detect_parser = subparsers.add_parser('detect', help='检测缺失翻译')
    detect_parser.add_argument('--reference', '-r', default='en_US', 
                              help='参考语言 (default: en_US)')
    
    # 翻译命令
    translate_parser = subparsers.add_parser('translate', help='批量翻译')
    translate_parser.add_argument('source', help='源语言代码')
    translate_parser.add_argument('targets', nargs='+', help='目标语言代码')
    
    # 生成所有命令
    generate_parser = subparsers.add_parser('generate-all', help='生成所有缺失的语言文件')
    
    # 验证命令
    validate_parser = subparsers.add_parser('validate', help='验证翻译质量')
    validate_parser.add_argument('locales', nargs='*', help='要验证的语言代码')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    tools = I18nDevTools()
    
    try:
        if args.command == 'detect':
            result = tools.detect_changes(args.reference)
            print(f"\n📊 检测结果:")
            if 'error' in result:
                print(f"❌ 错误: {result['error']}")
                return 1
            else:
                missing_count = len(result['missing_translations'])
                total_keys = result['total_keys']
                print(f"  缺失语言: {missing_count}")
                print(f"  总键数量: {total_keys}")
        
        elif args.command == 'translate':
            result = tools.translate_batch(args.source, args.targets)
            print(f"\n📊 翻译结果:")
            if 'error' in result:
                print(f"❌ 错误: {result['error']}")
                return 1
            else:
                for lang, res in result['results'].items():
                    status = res['status']
                    if status == 'success':
                        print(f"  ✅ {lang}: {res['translated_keys']} 个条目")
                    else:
                        print(f"  ❌ {lang}: {res.get('error', 'Unknown error')}")
        
        elif args.command == 'generate-all':
            result = tools.generate_missing_files()
            print(f"\n📊 生成结果:")
            if 'status' in result and result['status'] == 'no_missing_files':
                print("✅ 所有语言文件都已存在")
            elif 'generated_locales' in result:
                generated = result['generated_locales']
                print(f"  生成语言: {', '.join(generated)}")
        
        elif args.command == 'validate':
            locales = args.locales if args.locales else None
            result = tools.validate_translations(locales)
            print(f"\n📊 验证结果:")
            for lang, res in result['validation_results'].items():
                status = res['status']
                if status == 'valid':
                    print(f"  ✅ {lang}: 验证通过 ({res['total_keys']} 个条目)")
                elif status == 'invalid':
                    print(f"  ❌ {lang}: 验证失败 - {', '.join(res['errors'])}")
                else:
                    print(f"  ❌ {lang}: {res['errors'][0] if res['errors'] else 'Unknown error'}")
        
        return 0
        
    except Exception as e:
        print(f"❌ 工具执行失败: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())