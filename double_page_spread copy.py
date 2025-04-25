# # 简单的跨页拼图处理
# from PIL.Image import open, new, Resampling


# # 自定义生成后固定路径
# out_path = 'C:\Users\Admin\Pictures'

# def double_page_spread():
    
#     is_config = input()
    
#     return




# # 主函数运行
# def main():
    
#     # 各参数默认值
#     format = 'png'
#     width = 800
#     space = 10
#     pages = 9
#     quality = 80
#     out_path = str(current_dir / '长图')
    
#     # 添加用户是否开启自定义设置功能    
#     config_open =  is_customized('是否要自定义设置相关参数？(y/n): ')
    
#     # 若开启自定义设置，将用有效输入值替换默认值
#     if config_open:
        
#         user_input = input('请输入要生成的图片格式。默认png，可选jpg等：').strip()
#         if user_input:
#             format = user_input

#         user_input = input('输入长图宽，不输默认800：').strip()
#         if user_input:
#             try: 
#                 width = int(user_input) if width else 800
#             except ValueError:
#                 print("未输入有效数字，将使用默认值800")

#         user_input = input('输入图片间距，不输默认10：').strip()
#         if user_input:
#             try: 
#                 space = int(user_input) if space else 10
#             except ValueError:
#                 print("未输入有效数字，将使用默认值10")

#         user_input = input('输出多少张拼接图，不输默认9：').strip()
#         if user_input:
#             try: 
#                 pages = int(user_input) if pages else 9
#             except ValueError:
#                 print("未输入有效数字，将使用默认值9")

#         user_input = input('压缩质量0-100，不输默认80，数字越大质量越高：').strip()
#         if user_input:
#             try: 
#                 quality = int(user_input) if quality else 80
#             except ValueError:
#                 print("未输入有效数字，将使用默认值80")

#         user_input = input('输出文件夹，不输默认在当前目录下新建结果文件夹:').strip()
#         if user_input:
#             out_path = user_input

#     print('\n结果图片格式: ', format)
#     print('图片宽: ', width)
#     print('图片间距: ', space)
#     print('共输出' + str(pages) + '张图')
#     print('压缩质量', quality)
#     print('生成结果目录', out_path)

#     try:
#         merge_image(read_pic(), format, width, space, pages, quality, out_path)
#         print('拼图完成\n')
#     except Exception as e:
#         # 处理所有异常
#         print(f"发生了异常: {e}")


# if __name__=='__main__':
#     main()

