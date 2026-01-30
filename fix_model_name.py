import os

target_file = os.path.join("app", "engine", "llm_engine.py")

def fix_model_config():
    if not os.path.exists(target_file):
        print(f"❌ 找不到文件: {target_file}")
        return

    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 修复模型名称报错
    # 把 settings.ZHIPUAI_MODEL 替换为 "glm-4"
    if "settings.ZHIPUAI_MODEL" in content:
        content = content.replace("settings.ZHIPUAI_MODEL", '"glm-4"')
        print("✅ 已修复：模型名称硬编码为 glm-4")
    
    # 2. 预防性修复：如果 settings.OPENAI_BASE_URL 也没有定义
    # 把 settings.OPENAI_BASE_URL 替换为智谱官方地址
    if "settings.OPENAI_BASE_URL" in content:
        zhipu_url = '"https://open.bigmodel.cn/api/paas/v4/"'
        content = content.replace("settings.OPENAI_BASE_URL", zhipu_url)
        print("✅ 已修复：API 地址硬编码为官方地址")

    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("🎉 修复完成！")

if __name__ == "__main__":
    fix_model_config()