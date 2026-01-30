import copy
from typing import Dict, Any, Optional
from app.models.schema import GlobalStyleConfig

# Level 4: System Default (兜底配置 - 中文论文通用)
SYSTEM_DEFAULT_CONFIG = {
    "global_default": {
        "family": "SimSun", "size": 12.0, "line_spacing": 1.5, "color": "000000", "align": "JUSTIFY"
    },
    "heading_1": {
        "family": "SimHei", "size": 16.0, "bold": True, "align": "CENTER", "line_spacing": 1.5
    },
    "heading_2": {
        "family": "SimHei", "size": 14.0, "bold": True, "align": "LEFT", "line_spacing": 1.5
    },
    "body_text": {
        "family": "SimSun", "size": 12.0, "line_spacing": 1.5, "align": "JUSTIFY"
    }
}

class MergerEngine:
    @staticmethod
    def _deep_update(target: Dict, source: Dict) -> Dict:
        """递归合并字典"""
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                MergerEngine._deep_update(target[key], value)
            elif value is not None:
                target[key] = value
        return target

    @staticmethod
    def merge(
        user_prompt_dict: Optional[Dict[str, Any]] = None,
        rag_extracted_dict: Optional[Dict[str, Any]] = None,
        json_preset_dict: Optional[Dict[str, Any]] = None
    ) -> GlobalStyleConfig:
        """
        执行四级合并策略。
        Priority: User (L1) > RAG (L2) > JSON (L3) > Default (L4)
        """
        # 1. Start with System Defaults
        final_config = copy.deepcopy(SYSTEM_DEFAULT_CONFIG)

        # 2. Apply Level 3: Static JSON Presets
        if json_preset_dict:
            final_config = MergerEngine._deep_update(final_config, json_preset_dict)

        # 3. Apply Level 2: Dynamic RAG Rules
        if rag_extracted_dict:
            final_config = MergerEngine._deep_update(final_config, rag_extracted_dict)

        # 4. Apply Level 1: User Override
        if user_prompt_dict:
            final_config = MergerEngine._deep_update(final_config, user_prompt_dict)

        # --- 自动修复: 强制将对齐方式转为大写 (防止 AI 输出小写导致报错) ---
        for key, value in final_config.items():
            if isinstance(value, dict) and "align" in value and isinstance(value["align"], str):
                value["align"] = value["align"].upper()
        # -------------------------------------------------------------
        return GlobalStyleConfig(**final_config) 
