#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
图片矩阵拼接程序
功能：将多张图片按照N行M列的矩阵形式合并为一张图片
"""

import os
import math
from pathlib import Path
from PIL import Image

# 计算最优的行列数
def calculate_grid(number, n=None, m=None): 
    if not n is None and not m is None:
        return n, m
    elif not n is None:
        m = math.ceil(number / n)
        return n, m
    else:
        n = 2
        while True:
            m = math.ceil(number / n)
            if m > 3 * n:
                n += 1
                continue
            else:
                return n, m
            

def merge_images(image_paths, output_path, rows=None, cols=None, gap=10, width=None, height=None):
    """
    将多张图片按矩阵形式合并
    
    参数:
        image_paths: 图片路径列表
        output_path: 输出路径
        rows: 行数，如不指定则自动计算
        cols: 列数，如不指定则自动计算
        gap: 图片间的间隔像素
        width: 每张图片调整后的宽度，不指定则使用原图宽度
        height: 每张图片调整后的高度，不指定则使用原图高度
    """
    number = len(image_paths)
    if number == 0:
        print("请检查原始图片路径")
        return
    
    # 自动计算行列数
    rows, cols = calculate_grid(number, rows, cols)
    
    # 打开第一张图片来获取相关尺寸信息
    with open(image_paths[0], 'rb') as f:
        img_width, img_height = Image.open(f).size
        if width is None:
            width = img_width
        if height is None:
            height = img_height
        aspect_ratio = img_height / img_width
        # 如果只指定了宽度，按比例计算高度
        if width and not height:
            height = int(width * aspect_ratio)
        # 如果只指定了高度，按比例计算宽度
        if height and not width:
            width = int(height / aspect_ratio)
    
    # 让首行图片为较小的数量（余数）
    first_row_imgs = number - (rows - 1) * cols
    # 分别计算整体宽度和首行宽度 让首行居中显示
    merged_width = (cols * width) + ((cols - 1) * gap)
    first_merged_width = (first_row_imgs * width) + ((first_row_imgs - 1) * gap)
    # 计算首行居中显示需要偏移的距离
    offset = math.floor((merged_width - first_merged_width) / 2)
    # 计算整体高度
    merged_height = (rows * height) + ((rows - 1) * gap)
    
    # 创建新图像 
    merged_image = Image.new('RGB', (merged_width, merged_height), (255, 255, 255))
    
    # 将图片粘贴到新图像上
    current_img = 0
    for row in range(rows):
        if row == 0:
            col_range = first_row_imgs
        else:
            col_range = cols
        for col in range(col_range):
            if current_img < number:
                try:
                    img = Image.open(image_paths[current_img])
                    # 调整图片大小
                    img = img.resize((width, height), Image.LANCZOS)
                    
                    # 计算粘贴位置
                    x = col * (width + gap)
                    y = row * (height + gap)
                    
                    # 计算首行偏移
                    if row == 0 and offset > 0:
                        x += offset

                    # 粘贴图片
                    merged_image.paste(img, (x, y))
                    current_img += 1
                except Exception as e:
                    print(f"处理图片 {image_paths[current_img]} 时出错: {e}")
                    current_img += 1
            else:
                break
    
    # 保存结果
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    merged_image.save(output_path)
    print(f"已将 {number} 张图片合并为 {rows}×{cols} 的矩阵图片，保存至 {output_path}")

def main():
    # 获取当前目录
    current_dir = Path(__file__).parent
    image_dir = current_dir / 'origin_pic'
    output_dir = current_dir / 'result_pic'
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取图片列表
    image_types = ('.jpg', '.jpeg', '.png', '.bmp', '.jfif')
    image_paths = []
    
    if image_dir.exists():
        for file in os.listdir(image_dir):
            if file.lower().endswith(image_types):
                image_paths.append(str(image_dir / file))
    else:
        print(f"图片目录 {image_dir} 不存在，将搜索当前目录")
        for file in os.listdir(current_dir):
            if file.lower().endswith(image_types):
                image_paths.append(str(current_dir / file))
    
    # 按文件名排序
    image_paths.sort(key=lambda x: int(Path(x).stem))
    
    if not image_paths:
        print("未找到图片文件")
        return
    print(f"找到 {len(image_paths)} 张图片")
    
    # 用户输入
    # 询问是否自定义参数
    is_custom = input("是否要自定义参数？(y/n，默认n): ").lower().strip() == 'y'
    
    if is_custom:
        rows = None
        cols = None
        row_input = input("请输入行数和列数(不输入则自动计算): ").strip()
        if row_input:
            try:
                rows = int(row_input)
                if rows <= 0:
                    print("行数必须为正整数，将自动计算")
                    rows = None
            except ValueError:
                print("输入无效，将自动计算行数")
        
        if rows is not None:
            col_input = input(f"请输入列数(不输入则自动计算，保证行*列>={len(image_paths)}): ").strip()
            if col_input:
                try:
                    cols = int(col_input)
                    if cols <= 0:
                        print("列数必须为正整数，将自动计算")
                        cols = None
                    elif rows * cols < len(image_paths):
                        print(f"行*列={rows*cols}，小于图片数量{len(image_paths)}，将自动增加列数")
                        cols = math.ceil(len(image_paths) / rows)
                        print(f"调整后的列数为: {cols}")
                except ValueError:
                    print("输入无效，将自动计算列数")
            else:
                cols = math.ceil(len(image_paths) / rows)
                print(f"自动计算的列数为: {cols}")
        else:
            rows, cols = calculate_grid(len(image_paths))
            print(f"自动计算的行数为: {rows}, 列数为: {cols}")
        
        gap_input = input("请输入图片间隔(默认10像素): ").strip()
        gap = 10
        if gap_input:
            try:
                gap = int(gap_input)
                if gap < 0:
                    print("间隔不能为负数，将使用默认值10")
                    gap = 10
            except ValueError:
                print("输入无效，将使用默认值10")
        
        width_input = input("请输入图片宽度(不输入则使用原图宽度): ").strip()
        width = None
        if width_input:
            try:
                width = int(width_input)
                if width <= 0:
                    print("宽度必须为正整数，将使用原图宽度")
                    width = None
            except ValueError:
                print("输入无效，将使用原图宽度")
        
        height_input = input("请输入图片高度(不输入则按原比例自动计算): ").strip()
        height = None
        if height_input:
            try:
                height = int(height_input)
                if height <= 0:
                    print("高度必须为正整数，将按原比例自动计算")
                    height = None
            except ValueError:
                print("输入无效，将按原比例自动计算")
        
        output_name = input("请输入输出文件名(默认'merged.png'): ").strip()
        if not output_name:
            output_name = 'merged.png'
        if not output_name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            output_name += '.png'
        
        output_path = str(output_dir / output_name)
    else:
        # 使用默认参数
        rows, cols = calculate_grid(len(image_paths))
        gap = 10
        width = None
        height = None
        output_path = str(output_dir / 'merged.png')
    
    print("\n使用的参数:")
    print(f"行数: {rows}")
    print(f"列数: {cols}")
    print(f"间隔: {gap}像素")
    print(f"图片宽度: {'原图宽度' if width is None else width}")
    print(f"图片高度: {'按比例计算' if height is None else height}")
    print(f"输出路径: {output_path}")
    
    # 执行合并
    merge_images(image_paths, output_path, rows, cols, gap, width, height)

if __name__ == '__main__':
    try:
        main()
        input("\n按回车键退出...")
    except Exception as e:
        print(f"程序运行出错: {e}")
        input("\n按回车键退出...") 