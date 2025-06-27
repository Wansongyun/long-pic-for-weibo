from glob import glob
from PIL.Image import open, new, Resampling
from pathlib import Path
from re import split
import os


folder_path = input('输入图片文件夹路径：').strip()
file_list = sorted(os.listdir(folder_path))
# 过滤出图片文件（按实际需求筛选图片扩展名）
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
image_files = [f for f in file_list if os.path.splitext(f)[1].lower() in image_extensions]

# 开始重命名
for idx, filename in enumerate(image_files, start=1):
    ext = os.path.splitext(filename)[1]  # 保留原始扩展名
    new_name = f"{idx:02d}{ext}"
    src = os.path.join(folder_path, filename)
    dst = os.path.join(folder_path, new_name)
    os.rename(src, dst)

print("重命名完成！")
