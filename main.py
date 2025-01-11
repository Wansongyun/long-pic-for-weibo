from glob import glob
import logging
from PIL.Image import open, new, Resampling
from pathlib import Path
from re import split
from os import mkdir
from os.path import exists
#from math import round

def merge_image(imgs, width, space, out_n, quality, out_path):
    color = (255, 255, 255)
    total_num = len(imgs)
    if total_num % out_n != 0:
        per_page = round(total_num / (out_n))
    else:
        per_page = int(total_num / out_n)

    if per_page < 1:
        print('图片总数小于输出图片数，不拼图。')
        return 0

    imgs_size = [list(im.size) for im in imgs]

    for i in range(len(imgs_size)):
        rate = width / imgs_size[i][0]
        imgs_size[i][0] = width
        imgs_size[i][1] = int(rate * imgs_size[i][1])

    for i in range(1, out_n):
        sum_height = sum([im[1] + space for im in imgs_size[per_page * (i-1) : per_page * i]]) - space #计算总长度
        # print(sum_height)
        if sum_height <= 0:
            print('仅能拼接', i - 1, '张')
            return 0

        result = new("RGB", (width, sum_height), color)
        #新建空白长图
        result = merge_single(result,
                          imgs[per_page * (i - 1) : per_page * i],
                          imgs_size[per_page * (i - 1) : per_page * i], space) #拼接单个长图
        if not exists(out_path):
            mkdir(out_path)
        result.save(out_path + '/'+ str(i) + '.jpg', quality=quality) #存起来

    final_sum_height = sum([im[1] + space for im in imgs_size[per_page * (out_n - 1):]]) - space
    # print(final_sum_height)
    if final_sum_height <= 0:
        print('仅能拼接', out_n - 1, '张')
        return 0
    result = new("RGB", (width, final_sum_height), color) #新建空白长图
    result = merge_single(result,
                      imgs[per_page * (out_n - 1) : ],
                      imgs_size[per_page * (out_n - 1) : ], space) #拼接单个长图
    result.save(out_path + '/'+ str(out_n) + '.jpg', quality=quality) #存起来

    print('\n图片总数: ', total_num)
    print('分割条数: ', out_n)
    print('每页张数：', per_page)

    return 0

def merge_single(result, ims, ims_size, space):
    # 拼接单个长图
    top = 0
    for i, im in enumerate(ims):
        mew_im = im.resize(ims_size[i], Resampling.LANCZOS)  # 等比缩放
        result.paste(mew_im, box=(0, top))
        top += ims_size[i][1] + space
    return (result)

# 对图片文件列表简单排序
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)

# 获取当前文件夹下图片列表
current_dir = Path(__file__).parent
origin_pic_dir = current_dir / '原图'

logging.info(origin_pic_dir)

if not exists(origin_pic_dir):
    mkdir(origin_pic_dir)

image_files = glob(str(origin_pic_dir / '*.png')) + \
              glob(str(origin_pic_dir / '*.jpg')) + \
              glob(str(origin_pic_dir / '*.jpeg')) + \
              glob(str(origin_pic_dir / '*.bmp'))


# def get_image_files(directory: Path):
#     # 定义图片格式
#     image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']
    
#     # 存储所有图片文件
#     image_files = []
    
#     # 查找所有支持的格式
#     for ext in image_extensions:
#         image_files.extend(directory.glob(ext))
        
#     return image_files



def read_pic():
    ims = [open(fn) for fn in (image_files)]
    #所有图片转换成rgb
    for i, im in enumerate(ims):
        ims[i] = ims[i].convert("RGB")
    return (ims)


# 主函数运行
def main():
    # format = input('请输入要生成的图片格式。默认png，可选jpg等：')
    width = input('输入长图宽，不输默认800：')
    space = input('输入图片间距，不输默认10：')
    pages = input('输出多少张拼接图，不输默认9：')
    quality = input('jpg压缩质量，不输默认80，越低质量越差，越高体积越大：')
    out_path = input('输出文件夹，不输默认在当前目录下新建结果文件夹:')

    # 图片输出格式选择
    # if format == "":
    #     format = "png"
    # else:
    #     format = "jpg"

    if width == "":
        width = 800
    else:
        width = eval(width)

    if space == "":
        space = 10
    else:
        space = eval(space)

    if pages == "":
        pages = 9
    else:
        pages = eval(pages)

    if quality == "":
        quality = 80
    else:
        quality = eval(quality)

    if out_path == "":
        out_path = str(current_dir / '长图')

    # print('\n连页格式: ', format)
    # print('图片宽: ', width)
    # print('图片间距: ', format)
    # print('共输出' + str(pages) + '张图')
    # print('jpg图片压缩质量', quality)

    try:
        merge_image(read_pic(), width, space, pages, quality, out_path)
        print('拼图完成\n')
    except Exception as e:
        # 处理所有异常
        print(f"发生了异常: {e}")


if __name__=='__main__':
    main()
