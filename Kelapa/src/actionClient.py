
from common import SM4
from common import oprf
from common import curve_ed25519 as _curve
from common import generate_qr as QR
import random




class Iot:
    # 获取曲线的阶和生成元的点
    curve = _curve.Curve()
    order = curve.order
    generator_point = curve.generator_point
    private_key = 2024
    public_key = private_key * generator_point

    # 生成对称加解密方案
    SysmCipher = SM4()

    def create_QR(self,passwd: str) -> str:
        """
        产生动态二维码，输出二维码的字符串解析
        :return:
        """
        QR_name = QR.get_qr(passwd)   # 二维码名字, 可以查看二维码图片
        QR_string = QR.trans_bytes(QR_name)
        return QR_string

    def compute_key(self, QR_string: str) -> (str, int):
        """
        计算临时密钥
        :param QR_string: 二维码的字符串解析
        :return: 临时密钥，kc的值
        """
        kc = random.randint(1, self.order)              # 随机生成kc
        QR_hash = oprf.Hash(QR_string)             # 计算二维码的哈希值
        key = oprf.two_hashed_OPRF(kc, QR_string, QR_hash, self.order)  # 计算临时密钥
        return key, kc

    def compute_beta(self, alpha: int, kc: int) -> int:
        """
        计算beta的值
        :param alpha: IoT设备接收到的alpha值
        :param kc:
        :param order_:
        :return:
        """
        beta = pow(alpha, kc, self.order)
        return beta

    def compute_cipher(self, message, key: bytes) -> bytes:
        """
        对称加密，计算密文
        :param message: 待加密明文,椭圆曲线上的点
        :param key: 加密密钥
        :return:
        """
        messageBytes=self.curve.to_bytes(message)
        cipher_iot = self.SysmCipher.EnCrypt(key, messageBytes)
        return cipher_iot

    def DeCrypt(self, public_key_iots, cipher: bytes, key: bytes):
        """
        对称解密
        :param public_key_iots:
        :param cipher: IoT接收到的密文
        :param key: 解密密钥
        :return:
        """
        decryptTest = self.SysmCipher.DeCrypt(key, cipher)
        return self.curve.from_bytes(decryptTest)            # 椭圆曲线上的点

    def random_data_mark(self):
        """
        生成随机数y和点Y
        :return:
        """
        y = random.randint(1, self.order - 2)
        Y = y * self.generator_point
        return Y, y

    def compute_ssk(self, X, Y,  y: int,  public_key_iots,  public_key_iot,  private_key_iot: int) -> int:
        """
        计算得到会话密钥ssk
        :param X: Iot设备接收得到的点
        :param Y: Iot产生的点
        :param y: Iot生成的随机数y
        :param public_key_iots: IoT解密得到的IoT主控设备的公钥
        :param public_key_iot: IoT的公钥
        :param private_key_iot: IoT的私钥
        :return:
        """
        X_byte = self.curve.to_bytes(X)  # 将椭圆曲线上的点转换为字节类型
        Y_byte = self.curve.to_bytes(Y)
        public_key_iots_byte = self.curve.to_bytes(public_key_iots)
        public_key_iot_byte = self.curve.to_bytes(public_key_iot)

        e = oprf.Hash(X_byte + public_key_iot_byte)
        d = oprf.Hash(Y_byte + public_key_iots_byte)
        theta_c = (e * private_key_iot + y) % self.order
        ssk_temp = theta_c * (X + d * public_key_iots)
        ssk = oprf.Hash(self.curve.to_bytes(ssk_temp))
        return ssk

