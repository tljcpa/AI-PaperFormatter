import json
import logging
import os
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.core.config import settings
from langchain_core.output_parsers import StrOutputParser

logger = logging.getLogger(__name__)

class LLMEngine:
    def __init__(self):
        # 1. 初始化模型
        self.llm = ChatOpenAI(
            model="glm-4",
            api_key=settings.ZHIPUAI_API_KEY,
            base_url="https://open.bigmodel.cn/api/paas/v4/",
            temperature=0.1,
            model_kwargs={"response_format": {"type": "json_object"}}
        )
        
        # 2. 自动加载字体配置文件 (使用绝对路径修复)
        self.font_config = self._load_font_config()

    def _load_font_config(self) -> str:
        """
        读取 data/font_config.json
        *** 修复：使用基于文件位置的绝对路径，防止找不到文件 ***
        """
        try:
            # 获取当前脚本 (llm_engine.py) 的目录: app/engine/
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 向上退两级回到根目录，再进入 data 目录
            # 路径: app/engine/../../data/font_config.json
            project_root = os.path.dirname(os.path.dirname(current_dir))
            config_path = os.path.join(project_root, "data", "font_config.json")

            if os.path.exists(config_path):
                logger.info(f"✅ Loaded font config from: {config_path}")
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    return json.dumps(config_data, ensure_ascii=False, indent=2)
            else:
                # 如果还是找不到，为了防止"变回宋体"，这里保留一份硬编码的保底数据
                logger.warning(f"⚠️ Font config not found at {config_path}. Using fallback mapping.")
                fallback_map = {
                    "font_map_cn": {
                        "宋体": "SimSun", "黑体": "SimHei", "楷体": "KaiTi", 
                        "仿宋": "FangSong", "微软雅黑": "Microsoft YaHei",
                        "隶书": "LiSu", "幼圆": "YouYuan"
                    },
                    "size_map": {
                        "小四": 12.0, "四号": 14.0, "三号": 16.0
                    }
                }
                return json.dumps(fallback_map, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Failed to load font config: {e}")
            return "Error loading font mapping."

    def parse_layout_config(self, context: str, user_prompt: str) -> Dict[str, Any]:
        """
        C-Model: 提取排版参数
        """
        logger.debug("Calling C-Model for Layout Parsing...")
        
        prompt_template = """
        You are an expert academic formatting engine. Extract style rules based on the context and user request.
        
        Context from Rule Manual:
        {context}

        User Request:
        {user_prompt}

        Task: Return a JSON object defining the style rules.

        *** FONT & SIZE MAPPING TABLE (CRITICAL) ***
        Please STRICTLY refer to the following JSON table for converting Chinese names to System codes:
        
        {font_mapping_context}

        *** RULE FOR UNKNOWN FONTS ***
        If the user asks for a font NOT in the table above, output its English name directly (e.g., "Helvetica").

        Format example:
        {{
            "heading_1": {{ "font_name": "SimHei", "font_size": 16.0, "align": "CENTER", "line_spacing": 1.5, "is_bold": true }},
            "body_text": {{ "font_name": "KaiTi", "font_size": 12.0, "align": "JUSTIFY", "line_spacing": 1.5 }}
        }}
        
        Return ONLY valid JSON.
        """
        
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            response_str = chain.invoke({
                "context": context, 
                "user_prompt": user_prompt,
                "font_mapping_context": self.font_config
            })
            
            cleaned_response = response_str.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
                
            return json.loads(cleaned_response)
        except Exception as e:
            logger.error(f"Layout Parsing failed: {e}")
            return {}

    def polish_content(self, raw_text: str, rules: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        B-Model: 结构化润色
        """
        logger.debug("Calling B-Model for Polishing...")
        
        prompt_template = """
        You are an academic paper formatting assistant. Your task is to split the input text into logical blocks.

        Rules:
        1. Identify headings, captions, and body text.
        2. **CRITICAL**: Escape double quotes inside text with backslash (\\"). Example: "She said \\"Hello\\""
        3. Return ONLY valid JSON.

        Output JSON format:
        {{
            "blocks": [
                {{ "type": "heading_1", "text": "Chapter 1" }},
                {{ "type": "body_text", "text": "Content here..." }}
            ]
        }}

        Input Text:
        {raw_text}
        """

        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | self.llm | StrOutputParser()

        try:
            response_str = chain.invoke({"raw_text": raw_text})
            
            cleaned_response = response_str.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]

            data = json.loads(cleaned_response)
            
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and "blocks" in data:
                return data["blocks"]
            else:
                return [{"type": "body_text", "text": raw_text}]

        except Exception as e:
            logger.error(f"LLM Polishing failed (returning raw text): {e}")
            return [{"type": "body_text", "text": raw_text}]

llm_engine = LLMEngine()