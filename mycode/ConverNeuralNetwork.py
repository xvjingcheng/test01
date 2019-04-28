import numpy as np
import os

import cv2

IMAGE_SIZE =128


# 按照只当图像大小调整尺寸
def resize_image(image, height=IMAGE_SIZE, width=IMAGE_SIZE):
    top, bottom, left, right = (0, 0, 0, 0)

    # 获取图像尺寸
    h, w, _ = image.shape

    # 对于长宽不相等的图片，找到最长的一边
    longest_edge = max(h, w)

    # 计算短边需要增加多上像素宽度使其与长边等长
    if h < longest_edge:
        dh = longest_edge - h
        top = dh // 2
        bottom = dh - top
    elif w < longest_edge:
        dw = longest_edge - w
        left = dw // 2
        right = dw - left
    else:
        pass

    # RGB颜色
    BLACK = [0, 0, 0]

    # 给图像增加边界，是图片长、宽等长，cv2.BORDER_CONSTANT指定边界颜色由value指定
    constant = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=BLACK)

    # 调整图片大小并返回
    return cv2.resize(constant, (height, width))


# 读取训练数据
images = []
labels = []


def read_path(path_name):
    for dir_item in os.listdir(path_name):
        # 从初始路径开始叠加，合并成可识别的操作路径
        full_path = os.path.abspath(os.path.join(path_name, dir_item))
        # 如果是文件夹，继续递归调用
        if os.path.isdir(full_path):
            read_path(full_path)
        else:
            if dir_item.endswith('.JPG'):
                image = cv2.imread(full_path)
                image = resize_image(image, IMAGE_SIZE, IMAGE_SIZE)
                images.append(image)
                labels.append(path_name)
    return images, labels


# 从指定路径读取训练数据
def load_dataset(path_name):
    images, labels = read_path(path_name)
    # 将输入的所有图片专程四维数组，尺寸为（图片数量*IMAGE_SIZE*IMAGE_SIZE*3）
    # 图片为64*64像素，一个像素3个颜色值（RGB）
    images = np.array(images)


    # 标注数据，'hight'文件夹下都是高糖图像，全部指为0.另一个是‘lower’全部指为1.
    # labels = np.array([1 if label.endswith('hight')else 0 for label in labels])
    # print(labels)

    label_num  = []
    for label in labels:
        if label.endswith('hight'):
            label_num.append(2)
        elif label.endswith('middle'):
            label_num.append(1)
        else:
            label_num.append(0)
    # #         ''''''
    return images,np.array(label_num)
