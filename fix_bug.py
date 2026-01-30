import os

# 目标文件路径
target_file = os.path.join("app", "engine", "llm_engine.py")

def repair_file():
    if not os.path.exists(target_file):
        print(f"❌ 找不到文件: {target_file}")
        return

    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 关键修复逻辑：找到导致报错的 JSON 示例格式
    # 原理：LangChain 中 PromptTemplate 里的 JSON 花括号必须转义，即 { 变成 {{
    
    # 修复 1: 针对 "type" 字段的报错
    old_str_1 = '{"type": "..."}'
    new_str_1 = '{{"type": "..."}}'
    
    # 修复 2: 预防性修复其他可能的 JSON 示例
    old_str_2 = 'Output JSON format: {'
    new_str_2 = 'Output JSON format: {{'
    
    # 执行替换
    new_content = content
    if old_str_1 in new_content:
        new_content = new_content.replace(old_str_1, new_str_1)
        print("✅ 修复了 JSON 字段 'type' 的转义问题")
        
    # 如果上面的精确匹配没找到，尝试模糊修复（针对常见的 Prompt 写法）
    # 查找包含 {"type" 的行并进行转义处理（这是一个更通用的补救措施）
    if '{"type"' in new_content and '{{"type"' not in new_content:
         new_content = new_content.replace('{"type"', '{{"type"')
         new_content = new_content.replace('"}', '"}}')
         print("✅ 强制修复了 JSON 格式的花括号")

    # 写回文件
    if new_content != content:
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"🎉 文件已修复保存: {target_file}")
    else:
        print("⚠️ 未发现需要修复的内容，或者代码已经是正确的了。")

if __name__ == "__main__":
    repair_file()