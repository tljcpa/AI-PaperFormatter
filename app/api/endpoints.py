import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.template_loader import template_loader
from app.core.merger import MergerEngine
from app.engine.rag_engine import rag_engine
from app.engine.llm_engine import llm_engine
from app.engine.renderer import renderer
from app.models.schema import DocumentDSL

router = APIRouter()

def cleanup_temp_file(path: str):
    """后台任务：清理临时文件"""
    if os.path.exists(path):
        os.remove(path)

@router.post("/generate", summary="核心生成接口")
async def generate_paper(
    background_tasks: BackgroundTasks,
    source_file: UploadFile = File(..., description="论文草稿 (.md/.txt/.docx)"),
    rule_file: UploadFile = File(None, description="学校排版规范PDF (可选)"),
    school_id: str = Form(..., description="学校标识 (如 shenyang_chem)"),
    user_prompt: str = Form("", description="用户自然语言指令 (User Override)")
):
    task_id = str(uuid.uuid4())
    
    # --- Step 1: File Handling ---
    # 保存源文件
    source_ext = source_file.filename.split('.')[-1]
    source_path = os.path.join(settings.UPLOAD_DIR, f"{task_id}_source.{source_ext}")
    with open(source_path, "wb") as buffer:
        shutil.copyfileobj(source_file.file, buffer)
        
    # 保存规则文件 (如果有)
    has_custom_rules = False
    if rule_file:
        rule_path = os.path.join(settings.UPLOAD_DIR, f"{task_id}_rule.pdf")
        with open(rule_path, "wb") as buffer:
            shutil.copyfileobj(rule_file.file, buffer)
        
        # Ingest to RAG (Level 2 Source)
        template_loader.ingest_user_rule_file(rule_path, school_id)
        has_custom_rules = True
        background_tasks.add_task(cleanup_temp_file, rule_path)

    # --- Step 2: Knowledge Retrieval (The Hybrid Loader) ---
    # L3: Static JSON
    json_preset = template_loader.get_preset_rules(school_id)
    
    # L2: RAG Context
    rag_context = ""
    if has_custom_rules or json_preset is None:
        # 如果有上传新规，或者没找到静态预设，就去查向量库
        # 构造一个通用的 query 来把所有格式要点查出来
        rag_context = rag_engine.search_rules("字体 字号 行距 标题格式 页边距", school_id)

    # --- Step 3: LLM Orchestration ---
    # 3.1 C-Model: 解析样式
    # 如果有 RAG 上下文或用户指令，才需要调用解析模型
    rag_extracted_config = {}
    if rag_context or user_prompt:
        rag_extracted_config = llm_engine.parse_layout_config(rag_context, user_prompt)
    
    # 3.2 B-Model: 润色内容 (简化版：直接读文本)
    # TODO: 生产环境需要根据文件类型(docx/md)做精细化 Loader
    with open(source_path, 'r', encoding='utf-8', errors='ignore') as f:
        raw_text = f.read()
    
    # 这里的 user_prompt 实际上包含了样式指令，我们暂不把它传给 Polisher，只传给 Parser
    # Polisher 只负责让话变得好听
    content_blocks = llm_engine.polish_content(raw_text)

    # --- Step 4: The Merger (Logic Core) ---
    # 执行四级合并：UserPrompt (in parser result) > RAG > JSON > Default
    # 注意：LLM Parser 其实已经把 user_prompt 和 rag_context 融合在 rag_extracted_config 里了
    # 但为了架构严谨，我们通常把 LLM 解析出的结果视为 Level 2 + Level 1 的混合体
    
    final_style_config = MergerEngine.merge(
        user_prompt_dict=None, # 用户指令已经被 LLM 消化在 rag_extracted_config 里了
        rag_extracted_dict=rag_extracted_config,
        json_preset_dict=json_preset
    )

    # --- Step 5: Construct DSL ---
    dsl = DocumentDSL(
        meta={"task_id": task_id, "school_id": school_id},
        style_config=final_style_config,
        content_blocks=content_blocks
    )

    # --- Step 6: Rendering ---
    output_filename = f"{task_id}_output.docx"
    output_path = os.path.join(settings.UPLOAD_DIR, output_filename)
    
    renderer.render(dsl, output_path)

    # Cleanup source
    background_tasks.add_task(cleanup_temp_file, source_path)
    # Cleanup output eventually (not immediately, wait for download)
    
    return FileResponse(
        output_path, 
        filename=f"Paper_{school_id}.docx", 
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ) 
