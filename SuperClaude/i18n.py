#!/usr/bin/env python3
"""
SuperClaude V4 国际化 (i18n) 系统

功能特性：
- 支持10种语言的本地化
- YAML配置驱动的架构
- 智能语言检测和切换
- 文化适应性调整
- 缓存和性能优化
- 离线运行支持

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
from pathlib import Path
from typing import Dict, Optional, Any, List, Tuple
import time
import logging


class LocalizationManager:
    """
    SuperClaude V4 本地化管理器
    
    提供多语言支持、文化适应和性能优化的完整i18n解决方案
    """
    
    def __init__(self, locale_dir: Optional[str] = None):
        """
        初始化本地化管理器
        
        Args:
            locale_dir: 本地化文件目录路径，默认为 Framework-Hooks/locales
        """
        # 确定 locales 目录
        if locale_dir:
            self.locale_dir = Path(locale_dir)
        else:
            # 默认路径：Framework-Hooks/locales
            framework_root = Path(__file__).parent.parent
            self.locale_dir = framework_root / "Framework-Hooks" / "locales"
        
        # 当前语言设置
        self.current_locale = "zh_CN"  # 默认中文
        
        # 支持的语言列表
        self.supported_locales = [
            'en_US', 'zh_CN', 'zh_TW', 'ja_JP', 'ko_KR',
            'ru_RU', 'es_ES', 'de_DE', 'fr_FR', 'ar_SA'
        ]
        
        # 本地化数据缓存
        self._localization_cache = {}
        
        # 性能指标
        self._performance_metrics = {
            'cache_hits': 0,
            'cache_misses': 0,
            'load_times': [],
            'switch_times': []
        }
        
        # 配置日志
        self.logger = logging.getLogger(__name__)
        
        # 初始化
        self._initialize()
    
    def _initialize(self):
        """初始化本地化系统"""
        try:
            # 检查 locales 目录
            if not self.locale_dir.exists():
                self.logger.warning(f"Locales directory not found: {self.locale_dir}")
                return False
            
            # 预加载当前语言
            self._load_locale_data(self.current_locale)
            
            self.logger.info(f"LocalizationManager initialized with {self.current_locale}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize LocalizationManager: {e}")
            return False
    
    def _load_locale_data(self, locale_code: str) -> Dict[str, Any]:
        """
        加载特定语言的本地化数据
        
        Args:
            locale_code: 语言代码，如 'zh_CN'
            
        Returns:
            本地化数据字典
        """
        if locale_code in self._localization_cache:
            self._performance_metrics['cache_hits'] += 1
            return self._localization_cache[locale_code]
        
        start_time = time.perf_counter()
        
        try:
            locale_file = self.locale_dir / f"{locale_code}.json"
            
            if not locale_file.exists():
                self.logger.warning(f"Locale file not found: {locale_file}")
                return {}
            
            with open(locale_file, 'r', encoding='utf-8') as f:
                locale_data = json.load(f)
            
            # 缓存数据
            self._localization_cache[locale_code] = locale_data
            
            # 记录性能
            load_time = (time.perf_counter() - start_time) * 1000  # ms
            self._performance_metrics['load_times'].append(load_time)
            self._performance_metrics['cache_misses'] += 1
            
            self.logger.debug(f"Loaded locale {locale_code} in {load_time:.2f}ms")
            return locale_data
            
        except Exception as e:
            self.logger.error(f"Failed to load locale {locale_code}: {e}")
            return {}
    
    def get_text(self, key: str, locale: Optional[str] = None, **kwargs) -> str:
        """
        获取本地化文本
        
        Args:
            key: 文本键，支持点分层级，如 'commands.test'
            locale: 目标语言代码，默认使用当前语言
            **kwargs: 文本插值参数
            
        Returns:
            本地化文本字符串
        """
        target_locale = locale or self.current_locale
        locale_data = self._load_locale_data(target_locale)
        
        if not locale_data:
            return key  # 降级返回键名
        
        # 解析点分键
        keys = key.split('.')
        value = locale_data
        
        try:
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    # 键不存在，尝试英文降级
                    if target_locale != 'en_US':
                        return self.get_text(key, 'en_US', **kwargs)
                    return key
            
            # 如果是字符串，进行插值处理
            if isinstance(value, str) and kwargs:
                try:
                    return value.format(**kwargs)
                except (KeyError, ValueError) as e:
                    self.logger.warning(f"Text interpolation failed for key '{key}': {e}")
                    return value
            
            return str(value)
            
        except Exception as e:
            self.logger.error(f"Failed to get text for key '{key}': {e}")
            return key
    
    def set_locale(self, locale_code: str) -> bool:
        """
        设置当前语言
        
        Args:
            locale_code: 语言代码
            
        Returns:
            设置是否成功
        """
        if locale_code not in self.supported_locales:
            self.logger.warning(f"Unsupported locale: {locale_code}")
            return False
        
        start_time = time.perf_counter()
        
        # 预加载目标语言数据
        locale_data = self._load_locale_data(locale_code)
        if not locale_data:
            return False
        
        # 切换语言
        old_locale = self.current_locale
        self.current_locale = locale_code
        
        # 记录性能
        switch_time = (time.perf_counter() - start_time) * 1000  # ms
        self._performance_metrics['switch_times'].append(switch_time)
        
        self.logger.info(f"Language switched from {old_locale} to {locale_code} in {switch_time:.2f}ms")
        return True
    
    def get_current_locale(self) -> str:
        """获取当前语言代码"""
        return self.current_locale
    
    def get_supported_locales(self) -> List[str]:
        """获取支持的语言代码列表"""
        return self.supported_locales.copy()
    
    def get_locale_info(self, locale_code: Optional[str] = None) -> Dict[str, Any]:
        """
        获取语言信息
        
        Args:
            locale_code: 语言代码，默认使用当前语言
            
        Returns:
            语言信息字典
        """
        target_locale = locale_code or self.current_locale
        locale_data = self._load_locale_data(target_locale)
        
        if 'metadata' in locale_data:
            return locale_data['metadata']
        
        return {
            'language': target_locale,
            'name': target_locale,
            'version': 'unknown'
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        获取性能指标
        
        Returns:
            性能指标字典
        """
        metrics = self._performance_metrics.copy()
        
        # 计算平均值
        if metrics['load_times']:
            metrics['avg_load_time'] = sum(metrics['load_times']) / len(metrics['load_times'])
        else:
            metrics['avg_load_time'] = 0
        
        if metrics['switch_times']:
            metrics['avg_switch_time'] = sum(metrics['switch_times']) / len(metrics['switch_times'])
        else:
            metrics['avg_switch_time'] = 0
        
        # 计算缓存命中率
        total_requests = metrics['cache_hits'] + metrics['cache_misses']
        if total_requests > 0:
            metrics['cache_hit_rate'] = metrics['cache_hits'] / total_requests
        else:
            metrics['cache_hit_rate'] = 0
        
        return metrics
    
    def validate_locale_files(self) -> Dict[str, Any]:
        """
        验证本地化文件完整性
        
        Returns:
            验证结果字典
        """
        validation_results = {
            'valid_locales': [],
            'invalid_locales': [],
            'missing_locales': [],
            'total_keys': 0,
            'consistency_issues': []
        }
        
        reference_keys = set()
        
        for locale_code in self.supported_locales:
            locale_file = self.locale_dir / f"{locale_code}.json"
            
            if not locale_file.exists():
                validation_results['missing_locales'].append(locale_code)
                continue
            
            try:
                locale_data = self._load_locale_data(locale_code)
                if locale_data:
                    validation_results['valid_locales'].append(locale_code)
                    
                    # 收集键名用于一致性检查
                    current_keys = self._extract_keys(locale_data)
                    if not reference_keys:
                        reference_keys = current_keys
                        validation_results['total_keys'] = len(reference_keys)
                    else:
                        # 检查键的一致性
                        missing_keys = reference_keys - current_keys
                        extra_keys = current_keys - reference_keys
                        
                        if missing_keys or extra_keys:
                            validation_results['consistency_issues'].append({
                                'locale': locale_code,
                                'missing_keys': list(missing_keys),
                                'extra_keys': list(extra_keys)
                            })
                else:
                    validation_results['invalid_locales'].append(locale_code)
                    
            except Exception as e:
                validation_results['invalid_locales'].append(locale_code)
                self.logger.error(f"Validation failed for {locale_code}: {e}")
        
        return validation_results
    
    def _extract_keys(self, data: Dict[str, Any], prefix: str = '') -> set:
        """
        递归提取所有键名
        
        Args:
            data: 数据字典
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
                keys.update(self._extract_keys(value, current_key))
            else:
                keys.add(current_key)
        
        return keys


# 全局本地化管理器实例
_localizer = None

def get_localizer() -> LocalizationManager:
    """
    获取全局本地化管理器实例
    
    Returns:
        LocalizationManager 实例
    """
    global _localizer
    if _localizer is None:
        _localizer = LocalizationManager()
    return _localizer


def t(key: str, **kwargs) -> str:
    """
    便捷函数：获取本地化文本
    
    Args:
        key: 文本键
        **kwargs: 插值参数
        
    Returns:
        本地化文本
    """
    return get_localizer().get_text(key, **kwargs)


def set_language(locale_code: str) -> bool:
    """
    便捷函数：设置语言
    
    Args:
        locale_code: 语言代码
        
    Returns:
        设置是否成功
    """
    return get_localizer().set_locale(locale_code)


def get_current_language() -> str:
    """
    便捷函数：获取当前语言
    
    Returns:
        当前语言代码
    """
    return get_localizer().get_current_locale()