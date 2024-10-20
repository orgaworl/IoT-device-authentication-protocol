import random
import cv2
import qrcode
from pyzbar.pyzbar import decode


def get_qr_code_image(data: str) -> str:
    """
    生成二维码
    :param data: 数据
    :return:
    """
    qr = qrcode.QRCode(
        version=2,  # 尺寸
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 容错信息当前为 30% 容错
        box_size=10,  # 每个格子的像素大小
        border=4  # 边框格子宽度
    )  # 设置二维码的大小
    try:
        qr.add_data(data)
        # 生成二维码图片，fill_color二维码颜色，back_color二维码背景颜色
        img = qr.make_image(fill_color='black', back_color="white")
        # 用时间戳命名文件
        filename = 'test_QR.png'
        img.save(filename)
        return filename
    except Exception as e:
        return ""


def get_qr(passwd: str) -> str:
    """
    生成动态二维码
    filename:二维码文件名字
    """
    filename = get_qr_code_image(passwd)
    return filename


def trans_bytes(filename) -> str:
    """
    解析二维码
    :param filename: 二维码文件名
    :return: 解析后得到的字符串
    """
    image = cv2.imread(filename)
    # 解析二维码
    data = decode(image)
    # 打印解析结果
    return data[0].data.decode()


# if __name__ == '__main__':
#     data = 'https://blog.csdn.net/powerbiubiu'
#     name = get_qr()
#     string = trans_bytes(name)


