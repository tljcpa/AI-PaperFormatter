import uuid
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field

# --- Enums ---
class ContentType(str, Enum):
    HEADING_1 = "heading_1"
    HEADING_2 = "heading_2"
    HEADING_3 = "heading_3"
    BODY_TEXT = "body_text"
    CAPTION = "caption"
    # 预留钩子，用于后续扩展图文混排
    IMAGE_HOOK = "image_hook"
    TABLE_HOOK = "table_hook"

class Alignment(str, Enum):
    LEFT = "LEFT"
    CENTER = "CENTER"
    RIGHT = "RIGHT"
    JUSTIFY = "JUSTIFY"

# --- Style Definitions ---
class FontStyle(BaseModel):
    """原子样式定义"""
    family: Optional[str] = None      # 字体族 (e.g., "SimSun")
    size: Optional[float] = None      # 字号 (e.g., 12.0)
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    align: Optional[Alignment] = None
    line_spacing: Optional[float] = None # 行距倍数 (e.g., 1.5)
    color: Optional[str] = None       # Hex Color (e.g., "000000")
    
    # 段间距 (单位: Pt)
    space_before: Optional[float] = None
    space_after: Optional[float] = None

class GlobalStyleConfig(BaseModel):
    """全文档样式配置表"""
    global_default: Optional[FontStyle] = Field(default_factory=FontStyle)
    heading_1: Optional[FontStyle] = Field(default_factory=FontStyle)
    heading_2: Optional[FontStyle] = Field(default_factory=FontStyle)
    heading_3: Optional[FontStyle] = Field(default_factory=FontStyle)
    body_text: Optional[FontStyle] = Field(default_factory=FontStyle)
    caption: Optional[FontStyle] = Field(default_factory=FontStyle)

# --- Content Structure ---
class ContentBlock(BaseModel):
    """内容积木块"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: ContentType
    text: str = ""
    
    # 如果是图片或表格，存储相关元数据
    source_data: Optional[str] = None 
    
    # 用户强制覆盖的块级样式 (User Override Block Level)
    style_override: Optional[FontStyle] = None

# --- Main DSL Object ---
class DocumentDSL(BaseModel):
    """核心数据协议对象"""
    meta: Dict[str, Any] = Field(default_factory=lambda: {
        "task_id": str(uuid.uuid4()),
        "school_conf": "unknown"
    })
    
    # 最终合并后的样式配置
    style_config: GlobalStyleConfig
    
    # 有序内容列表
    content_blocks: List[ContentBlock] 
