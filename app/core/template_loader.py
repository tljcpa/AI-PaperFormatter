import os
import json
from typing import Dict, Any, Optional
from PyPDF2 import PdfReader
from langchain_core.documents import Document

from app.core.config import settings
from app.engine.rag_engine import rag_engine

class TemplateLoader:
    """
    混合模版加载器。
    职责：管理静态 JSON 规则与动态 PDF 规则的加载/入库。
    """

    @staticmethod
    def get_preset_rules(school_id: str) -> Optional[Dict[str, Any]]:
        """
        尝试加载 Level 3 静态预设 (JSON)。
        路径: data/rules/{school_id}.json
        """
        # 安全处理文件名
        safe_name = "".join([c for c in school_id if c.isalnum() or c in ('_', '-')])
        json_path = os.path.join(settings.RULES_DIR, f"{safe_name}.json")

        if not os.path.exists(json_path):
            print(f"DEBUG: No static preset found for {school_id}")
            return None

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"DEBUG: Loaded static preset for {school_id}")
                return data
        except Exception as e:
            print(f"ERROR: Failed to load JSON preset: {e}")
            return None

    @staticmethod
    def ingest_user_rule_file(file_path: str, school_id: str) -> bool:
        """
        处理用户上传的排版规范文件 (PDF)。
        1. 提取文本
        2. 切片
        3. 存入 ChromaDB (Level 2 Source)
        """
        if not file_path.endswith(".pdf"):
            print("WARNING: Only PDF rule files are currently supported for RAG.")
            return False

        try:
            # 1. 简单的 PDF 文本提取
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

            # 2. 简单的切片 (按固定字符数，实际生产可用 RecursiveCharacterTextSplitter)
            chunk_size = 1000
            chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
            
            # 3. 构造 LangChain Document 对象
            documents = [Document(page_content=chunk) for chunk in chunks]

            # 4. 调用 RAG 引擎入库
            rag_engine.add_documents(documents, school_id)
            return True

        except Exception as e:
            print(f"ERROR: Failed to ingest rule file: {e}")
            return False

# 单例导出
template_loader = TemplateLoader() 
