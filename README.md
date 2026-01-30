这是一个为你定制的完整项目描述，涵盖了我们刚刚实现的所有高级功能（双字体控制、智能配置驱动、JSON容错等）以及涉及的技术栈。

你可以直接复制下面的代码块，保存为 `README.md` 或者放在你的项目文档中。

```markdown
# 🎓 AI-PaperFormatter (智能论文排版助手)

## 📖 项目简介
AI-PaperFormatter 是一个基于大语言模型（LLM）的自动化学术论文排版系统。它能够理解用户的自然语言排版指令（如“正文用楷体，英文用 Arial”），或者根据预设的学校论文规范，将纯文本草稿自动转换为格式完美的 Word 文档。

本项目解决了传统排版中“中西文字体分离设置”、“复杂格式调整繁琐”等痛点，实现了从规则解析到文档生成的全链路自动化。

---

## ✨ 核心功能

### 1. 🤖 双模型智能引擎 (Dual-Model Engine)
* **C-Model (Config Engine)**: 负责解析排版规则。支持从自然语言指令中提取字体、字号、行距、对齐方式等参数。
    * *亮点*: 内置强大的**字体映射系统**，能自动将口语化的“楷体”、“小四”转换为系统可识别的 `KaiTi` 和 `12.0pt`。
* **B-Model (Block Engine)**: 负责内容结构化。自动识别文章中的标题、正文、图片说明，并进行结构化切分，同时具备 JSON 格式容错和符号转义能力。

### 2. 🔠 中西文双字体独立控制 (Smart Dual-Font Rendering)
突破了普通 Word 库的限制，实现了**中英文字体分离渲染**：
* 支持“双通道”指定：例如中文使用 **宋体**，英文/数字使用 **Times New Roman**。
* 支持智能回退策略：如果用户未指定英文字体，系统会根据中文字体类型（衬线/无衬线）自动匹配最合适的英文字体（如黑体配 Arial，宋体配 Times）。

### 3. ⚙️ 配置驱动架构 (Config-Driven Architecture)
* **外部化配置**: 字体映射表（`font_config.json`）与代码逻辑分离，无需修改代码即可扩展支持新字体（如“方正小篆”）。
* **动态加载**: 系统启动时自动加载最新的字体和字号配置，具备极强的扩展性。

### 4. 📄 所见即所得的文档生成
* 基于 `python-docx` 深度定制的渲染器，直接操作 Word底层 XML (`w:eastAsia`)，确保格式在任何设备上打开都标准统一。

---

## 🛠 技术栈 (Tech Stack)

### 核心语言
* **Python 3.10+**: 项目开发语言。

### Web 框架 & API
* **FastAPI**: 高性能后端 API 框架，提供 RESTful 接口。
* **Uvicorn**: ASGI 服务器，负责承载后端服务。
* **Streamlit**: 前端交互界面，提供文件上传、指令输入和实时反馈。

### AI & LLM 生态
* **LangChain**: 大模型应用开发框架，管理 Prompt Template 和 Chain。
* **ZhipuAI (GLM-4)**: 智谱 AI 大模型，提供强大的语义理解和 JSON 格式化输出能力。
* **Pydantic**: 数据结构定义与校验，确保排版参数的类型安全。

### 文档处理
* **python-docx**: 用于生成 `.docx` 文件。
* **lxml / OpenXML**: 用于处理 Word 文档底层的 XML 命名空间，实现中西文分体设置。

### 工具与规范
* **JSON**: 数据交换格式。
* **Requests**: 前后端通信。

---

## 📂 项目结构概览

```text
AI-PaperFormatter/
├── app/
│   ├── api/            # API 路由定义
│   ├── core/           # 核心配置与合并逻辑
│   ├── engine/         # AI 引擎核心
│   │   ├── llm_engine.py   # 大模型交互 (C-Model & B-Model)
│   │   └── renderer.py     # Word 渲染器 (含双字体逻辑)
│   ├── models/         # Pydantic 数据模型 (Schema)
│   └── main.py         # 后端启动入口
├── data/
│   ├── font_config.json    # 字体/字号映射配置文件
│   └── rules/              # 学校预设规则库
├── web_demo.py         # Streamlit 前端页面
├── requirements.txt    # 项目依赖列表
└── README.md           # 项目说明文档

```

---

## 🚀 快速开始

1. **环境安装**
```bash
pip install -r requirements.txt

```


2. **启动后端服务 (Backend)**
```bash
py -3.10 -m app.main

```


3. **启动前端界面 (Frontend)**
```bash
streamlit run web_demo.py

```


4. **使用示例**
* 在网页输入指令：*"把标题改成黑体二号，正文中文用楷体，英文用 Arial，行距 1.5 倍"*
* 上传文本草稿，点击生成即可获得排版好的 Word 文档。



```

```
