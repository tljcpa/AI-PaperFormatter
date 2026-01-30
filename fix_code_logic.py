import os

# 目标文件
target_file = os.path.join("app", "engine", "llm_engine.py")

def undo_aggressive_fix():
    if not os.path.exists(target_file):
        print(f"❌ 找不到文件: {target_file}")
        return

    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 修复目标：代码里的 model_kwargs 不应该用双花括号 {{ }}
    # 错误的代码: model_kwargs={"response_format": {{"type": "json_object"}}}
    # 正确的代码: model_kwargs={"response_format": {"type": "json_object"}}
    
    wrong_code = 'model_kwargs={"response_format": {{"type": "json_object"}}}'
    correct_code = 'model_kwargs={"response_format": {"type": "json_object"}}'
    
    if wrong_code in content:
        new_content = content.replace(wrong_code, correct_code)
        
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ 成功修复：已将 model_kwargs 里的双花括号还原为单花括号。")
    else:
        # 尝试更模糊的匹配，以防空格不同
        if '{{"type": "json_object"}}' in content:
            new_content = content.replace('{{"type": "json_object"}}', '{"type": "json_object"}')
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("✅ 成功修复：已还原 JSON 配置格式。")
        else:
            print("⚠️ 未发现错误代码，或者文件已经被手动修复了。")

if __name__ == "__main__":
    undo_aggressive_fix()