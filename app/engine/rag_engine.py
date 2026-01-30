from typing import List
# 使用 OpenAI 适配器连接智谱 Embedding
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.core.config import settings

class RAGEngine:
    def __init__(self):
        # 初始化 Embedding (智谱 embedding-3)
        self.embedding_function = OpenAIEmbeddings(
            model=settings.MODEL_EMBED,         
            openai_api_key=settings.ZHIPUAI_API_KEY,
            openai_api_base=settings.OPENAI_BASE_URL,
            check_embedding_ctx_length=False
        )
        
        # 初始化 ChromaDB (本地持久化)
        self.vector_store = Chroma(
            collection_name="school_rules",
            embedding_function=self.embedding_function,
            persist_directory=settings.CHROMA_PERSIST_DIRECTORY
        )

    def add_documents(self, documents: List[Document], school_id: str):
        """添加文档并打上 school_id 标签"""
        for doc in documents:
            doc.metadata["school_id"] = school_id
        self.vector_store.add_documents(documents)

    def search_rules(self, query: str, school_id: str, k: int = 4) -> str:
        """检索特定学校的规则"""
        results = self.vector_store.similarity_search(
            query, 
            k=k,
            filter={"school_id": school_id}
        )
        return "\n\n".join([doc.page_content for doc in results])
    
    def as_retriever(self, school_id: str):
        """暴露给 LangChain Chain 使用"""
        return self.vector_store.as_retriever(
            search_kwargs={"filter": {"school_id": school_id}, "k": 4}
        )

# 单例导出
rag_engine = RAGEngine() 
