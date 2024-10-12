import random
from Crypto.Util.number import *

from common import SM4
from common import get_random_num
from common import oprf
from common import curve_ed25519 as _curve


class IoT_Control:
    # 获取曲线的阶和生成元的点
    curve = _curve.Curve()
    order = curve.order
    generator_point = curve.generator_point

    # 生成IoT设备身份标识私钥和公钥
    private_key = 4046
    public_key = private_key * generator_point

    # 生成SysmCipher加解密方案
    SysmCipher = SM4()

    def generate_alpha(self, QR_string: str) -> (str, int):
        """
        IoT主控设备生成随机数r, 计算alpha
        :param QR_string: 得到的二维码
        :return:
        """
        r = get_random_num.generate_prime(self.order)
        QR_string_hash = oprf.Hash(QR_string)
        temp = pow(QR_string_hash, r, self.order)
        alpha = str(temp)
        return alpha, r

    def compute_key_cipher(self, QR_string: str, r: int, beta: int, cipher_iot: bytes, public_key_iots):
        """
        计算临时密钥、解密接收到的密文，计算身份标识公钥的密文
        :param QR_string: IoT主控设备接收到的二维码
        :param r: 计算的随机数r
        :param beta: 接收到的数beta
        :param cipher_iot: 接收到的密文
        :param public_key_iots: 身份标识公钥
        :return: 密文，IoT主控设备接收到的密文解密结果，临时密钥
        """
        r_inverse = inverse(r, self.order - 1)
        key = oprf.two_hashed_OPRF(r_inverse, QR_string, beta, self.order)
        decryptTest = self.SysmCipher.DeCrypt(key.encode(), cipher_iot)
        cipher_iots = self.SysmCipher.EnCrypt(key.encode(), self.curve.to_bytes(public_key_iots))
        return cipher_iots, self.curve.from_bytes(decryptTest), key

    def random_data_mark(self):
        """
        输出随机数x和点X
        :return:
        """
        x = random.randint(1, self.order - 2)
        X = x * self.generator_point
        return X, x

    def compute_ssk(self, X, Y, x, public_key_iots, public_key_iot, private_key_iots) -> int:
        X_byte = self.curve.to_bytes(X)  # 将点转换为bytes类型
        Y_byte = self.curve.to_bytes(Y)
        public_key_iots_byte = self.curve.to_bytes(public_key_iots)
        public_key_iot_byte = self.curve.to_bytes(public_key_iot)

        e = oprf.Hash(X_byte + public_key_iot_byte)
        d = oprf.Hash(Y_byte + public_key_iots_byte)

        theta_s = (d * private_key_iots + x) % self.order
        ssk_temp = theta_s * (Y + e * public_key_iot)
        ssk = oprf.Hash(self.curve.to_bytes(ssk_temp))
        return ssk

