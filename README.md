# AI-PaperFormatter
📑 AI-PaperFormatter：基于大模型的智能学术论文排版系统
📖 项目简介
AI-PaperFormatter 是一款基于 LLM（大语言模型）的自动化排版工具，旨在解决学术论文写作中繁琐的格式调整问题。用户只需上传纯文本草稿，系统即可根据指定的学校模板（或用户口语化指令），利用 RAG 技术和 LLM 语义理解，自动生成符合严格学术规范的 Word 文档。

本项目采用前后端分离架构，实现了从文本清洗、结构化解析、样式提取到最终文档渲染的全链路自动化。

🛠 技术栈 (Tech Stack)
本项目集成了现代 Python Web 开发与 AIGC 领域的多种主流技术：

1. 核心框架与后端 (Core & Backend)
Python 3.10+: 项目开发语言。

FastAPI: 高性能异步 Web 框架，提供 RESTful API 接口 (POST /generate)，负责处理排版请求与数据流转。

Uvicorn: 基于 uvloop 的 ASGI 服务器，提供生产级的高并发支持。

Pydantic V2: 用于构建严格的数据模型 (GlobalStyleConfig)，确保 AI 输出的排版参数（如字号、间距、对齐方式）符合预定义 Schema，杜绝格式错误。

2. 人工智能与编排 (AI & Orchestration)
LangChain: 核心 LLM 编排框架。用于构建 Prompt Template、管理 Chain 的调用流（Chain of Thought），以及处理 Output Parsers。

ZhipuAI (GLM-4): 底层大语言模型。利用其强大的语义理解能力进行：

B-Model: 文本结构化润色（识别标题、正文、图注）。

C-Model: 排版规则提取（将用户口语指令转化为 JSON 配置）。

Prompt Engineering: 包含复杂的提示词工程，如 JSON 格式强制约束、特殊字符转义处理、中英文映射指南等。

3. 文档处理与渲染 (Document Processing)
python-docx: 核心文档生成库。用于操作 Word (.docx) 文件的底层 XML 结构。

OOXML (Open Office XML): 深入使用了 docx.oxml.ns.qn 命名空间，直接操作 Word 底层元素。

双字体渲染算法 (Dual-Font Rendering): 自研的字体控制逻辑，实现了中西文/数字字体独立控制（如：中文用楷体，英文/数字强制用 Times New Roman），解决了传统 Python 库无法区分中英文字体的痛点。

4. 前端交互 (Frontend)
Streamlit: 快速构建的交互式 Web 界面。提供文件上传（Drag & Drop）、实时进度条反馈、排版参数配置及结果文档下载功能。

5. 工程化与配置 (Engineering)
Config-Driven Architecture: 采用配置文件驱动设计（如 font_config.json），将字体映射表与业务代码解耦，支持无需重启即可热更新字体库。

Robust JSON Handling: 内置容错机制，自动修复 LLM 输出的不标准 JSON（如 Markdown 包裹清洗、双引号转义），保证系统稳定性。

🚀 核心功能亮点
智能样式提取 (Intent Parsing)

系统不依赖死板的模板代码，而是通过 LLM 理解用户的自然语言指令（例如：“把标题改成黑体三号，正文用宋体”），动态生成排版规则。

中西文自动分体 (Smart Font Pairing)

针对学术论文的特殊要求，系统内置了智能分体逻辑。即使用户只指定了中文字体，渲染引擎也会自动为其中的英文和数字匹配最合适的西文字体（如：黑体配 Arial，宋体配 Times New Roman）。

结构化内容识别

利用 AI 自动识别文本中的章节标题、正文段落和图片/表格说明，并根据识别结果分别应用不同的样式规则。

高度可扩展性

支持自定义学校模板 (data/rules/*.json) 和字体库 (data/font_config.json)，可轻松适配不同高校的毕业论文格式要求。
