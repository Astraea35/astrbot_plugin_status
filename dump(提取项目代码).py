import os

# 1. 自动获取当前所在的文件夹名字
current_folder = os.path.basename(os.getcwd())
output_filename = f"【代码打包】{current_folder}.txt"

# 2. 定义需要排除的垃圾文件或缓存
EXCLUDE_DIRS = {'__pycache__', '.git', '.idea', 'data', 'ocr_cache'}
# ✨ 核心修正：这里把名字同步改掉，防止脚本傻乎乎地把自己也打包进去
EXCLUDE_FILES = {output_filename, 'dump(提取项目代码).py', '.DS_Store'}

def dump_project():
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(f"=========================================\n")
        f.write(f"🌟 项目根文件夹名称: {current_folder}\n")
        f.write(f"=========================================\n\n")
        
        # 先打印一份标准的目录树结构
        f.write("📂 目录树结构:\n")
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            level = root.replace(".", "").count(os.sep)
            indent = " " * 4 * level
            f.write(f"{indent}├── {os.path.basename(root)}/\n")
            sub_indent = " " * 4 * (level + 1)
            for file in files:
                if file not in EXCLUDE_FILES and not file.endswith(('.zip', '.pyc')):
                    f.write(f"{sub_indent}├── {file}\n")
        
        f.write("\n" + "="*50 + "\n\n")
        
        # 逐个读取并写入文件内容
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                if file in EXCLUDE_FILES or file.endswith(('.zip', '.pyc')):
                    continue
                    
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, ".")
                
                f.write(f"📝 [FILE_NAME]: rel_path -> {rel_path}\n")
                f.write(f"-----------------------------------------\n")
                
                try:
                    with open(file_path, "r", encoding="utf-8") as source_f:
                        f.write(source_f.read())
                except Exception as e:
                    f.write(f"❌ [无法读取文本内容: {str(e)}]\n")
                    
                f.write(f"\n\n=========================================\n\n")

    print(f"🎉 提取成功！文件已保存在: {output_filename}")

if __name__ == "__main__":
    dump_project()