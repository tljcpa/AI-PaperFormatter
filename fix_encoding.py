import os

def convert_to_utf8(filename):
    try:
        # 尝试以 GBK 格式（Windows默认）读取
        with open(filename, 'r', encoding='gbk') as f:
            content = f.read()
        
        # 如果能读出来，就以 UTF-8 格式写回去
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 已修复: {filename}")
    except UnicodeDecodeError:
        # 如果本来就是 UTF-8 或者不是 GBK，就跳过
        print(f"⏩ 跳过 (无需修复): {filename}")
    except Exception as e:
        print(f"❌ 出错: {filename} - {e}")

print("正在扫描并修复所有 .py 文件的编码...")

# 遍历 app 目录下的所有文件
for root, dirs, files in os.walk("app"):
    for file in files:
        if file.endswith(".py"):
            convert_to_utf8(os.path.join(root, file))

print("完成！") 
