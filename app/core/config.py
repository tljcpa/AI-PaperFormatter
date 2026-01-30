import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # --- Basic API Configuration (Zhipu via OpenAI SDK) ---
    # 智谱 GLM-4 的兼容 API 地址
    OPENAI_BASE_URL: str = "https://open.bigmodel.cn/api/paas/v4/"
    # 这里填写智谱的 API Key
    ZHIPUAI_API_KEY: str

    # --- Model Constants ---
    # B-Model: 负责高质量润色 (学术能力强)
    MODEL_POLISH: str = "glm-4-plus"
    # C-Model: 负责快速规则提取与结构化 (速度快、成本低)
    MODEL_PARSE: str = "glm-4-flash"
    # Embedding: 负责 RAG 向量化 (API模式)
    MODEL_EMBED: str = "embedding-3"

    # --- Directories ---
    CHROMA_PERSIST_DIRECTORY: str = "./data/chroma_db"
    UPLOAD_DIR: str = "./data/uploads"
    RULES_DIR: str = "./data/rules"
    TEMPLATE_SOURCE_DIR: str = "./data/templates_source"

    # --- Security ---
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # Load from .env file
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        case_sensitive=True,
        extra="ignore"
    )

# 实例化配置对象
settings = Settings()

# 确保必要的目录存在
os.makedirs(settings.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.RULES_DIR, exist_ok=True)
os.makedirs(settings.TEMPLATE_SOURCE_DIR, exist_ok=True)