import os

target_file = os.path.join("app", "core", "merger.py")

def patch_merger_engine():
    if not os.path.exists(target_file):
        print(f"❌ 找不到文件: {target_file}")
        return

    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 我们要找到 merge 函数的最后一行，在它返回之前插入一段“强制大写”的代码
    target_str = "return GlobalStyleConfig(**final_config)"
    
    # 注入的修复代码：遍历所有配置，把 align 字段强制转为大写
    patch_code = """
        # --- 自动修复: 强制将对齐方式转为大写 (防止 AI 输出小写导致报错) ---
        for key, value in final_config.items():
            if isinstance(value, dict) and "align" in value and isinstance(value["align"], str):
                value["align"] = value["align"].upper()
        # -------------------------------------------------------------
        return GlobalStyleConfig(**final_config)"""

    if target_str in content:
        # 只有当文件里没有这段补丁时才添加
        if "强制将对齐方式转为大写" not in content:
            new_content = content.replace(target_str, patch_code.strip())
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("✅ 成功修复：已添加自动转换大写的逻辑。")
        else:
            print("⚠️ 补丁已存在，无需重复修复。")
    else:
        print("❌ 无法定位注入点，可能是代码版本不匹配。")

if __name__ == "__main__":
    patch_merger_engine()