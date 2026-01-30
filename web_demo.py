import streamlit as st
import requests
import time

# --- 配置 ---
BACKEND_URL = "http://127.0.0.1:8000/api/v1/generate"
DEFAULT_SCHOOL = "shenyang_chem"

# --- 页面设置 ---
st.set_page_config(
    page_title="AI 论文排版助手",
    page_icon="📄",
    layout="centered"
)

# --- 标题与介绍 ---
st.title("📄 AI-PaperFormatter 演示平台")
st.markdown("""
> **基于 RAG + LLM 的智能排版引擎** > 上传草稿，一键生成符合学校规范的完美论文。
""")

st.divider()

# --- 侧边栏配置 ---
with st.sidebar:
    st.header("⚙️ 排版设置")
    school_id = st.text_input("学校标识 (School ID)", value=DEFAULT_SCHOOL, help="例如: shenyang_chem")
    
    st.subheader("🔧 高级选项")
    user_prompt = st.text_area(
        "强制指令 (User Override)", 
        placeholder="例如：把所有一级标题改成红色...",
        help="你的指令优先级高于学校模板"
    )
    
    st.info("💡 提示：目前仅预设了 'shenyang_chem' 模板。")

# --- 主区域：文件上传 ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 上传草稿 (必选)")
    source_file = st.file_uploader("支持 .txt, .md, .docx", type=["txt", "md", "docx"])

with col2:
    st.subheader("2. 上传新规范 (可选)")
    rule_file = st.file_uploader("排版手册 .pdf (用于 RAG)", type=["pdf"])

# --- 生成按钮与逻辑 ---
st.divider()

if st.button("🚀 开始 AI 排版", type="primary", use_container_width=True):
    if not source_file:
        st.error("请先上传论文草稿！")
    else:
        # 准备数据
        files = {
            "source_file": (source_file.name, source_file, source_file.type)
        }
        if rule_file:
            files["rule_file"] = (rule_file.name, rule_file, rule_file.type)
            
        data = {
            "school_id": school_id,
            "user_prompt": user_prompt
        }

        # 进度条模拟
        progress_text = "正在连接 AI 引擎..."
        my_bar = st.progress(0, text=progress_text)

        try:
            # 模拟进度 (为了演示效果)
            for percent_complete in range(10):
                time.sleep(0.05)
                my_bar.progress(percent_complete + 10, text="正在解析文档结构...")

            # 发送请求
            with st.spinner('🤖 AI 正在疯狂排版中 (润色 + 渲染)...'):
                response = requests.post(BACKEND_URL, files=files, data=data)

            if response.status_code == 200:
                my_bar.progress(100, text="排版完成！")
                st.success("✅ 生成成功！请下载下方文件。")
                
                # 获取文件名
                content_disposition = response.headers.get("content-disposition", "")
                if "filename=" in content_disposition:
                    filename = content_disposition.split("filename=")[1].strip('"')
                else:
                    filename = f"Paper_{school_id}.docx"

                # 下载按钮
                st.download_button(
                    label="📥 下载排版好的 Word 文档",
                    data=response.content,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    type="primary"
                )
            else:
                my_bar.empty()
                st.error(f"❌ 生成失败: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("❌ 无法连接到后端服务。请检查 main.py 是否正在运行！")