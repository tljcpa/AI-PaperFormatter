import os

target_file = os.path.join("app", "engine", "llm_engine.py")

def patch_json_parser():
    if not os.path.exists(target_file):
        print(f"❌ 找不到文件: {target_file}")
        return

    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 我们要劫持 json.loads 之前，先做一个简单的清洗
    # 找到 parse_json_markdown 函数（或者处理输出的地方）
    # 由于 LangChain 封装较深，我们直接修改 prompt 提示词，强制要求 AI 转义引号
    
    # 方案：修改提示词，明确要求转义
    search_str = 'Output JSON format: {"'
    replace_str = 'Output JSON format (Escape inner quotes with \\"): {"'
    
    if search_str in content and "Escape inner quotes" not in content:
        new_content = content.replace(search_str, replace_str)
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ 提示词已增强：现在 AI 会更小心地处理双引号了。")
    else:
        print("⚠️ 提示词已包含转义要求，或无需修改。")

if __name__ == "__main__":
    patch_json_parser()