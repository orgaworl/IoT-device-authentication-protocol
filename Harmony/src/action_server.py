import random
from common import SM4
from common import SM3HashComp
from common import sign_verfy as sv
from common import curve_ed25519 as _curve


class IoT_Control:
    # 获取曲线的阶和生成元的点
    curve = _curve.Curve()
    order = curve.order
    generator_point = curve.generator_point
    private_key = 2024
    public_key = private_key * generator_point
    private_key_iots = sv.gen_private_key(private_key)
    public_key_iots = sv.gen_public_key(public_key)

    # 生成AES加解密方案
    SysmCipher =SM4()
    HashFunc=SM3HashComp()
    def compute_x(self, QR_salt: str) -> int:
        """
        计算x
        :return:
        """
        x = self.HashFunc.Hash(QR_salt)
        return x

    def compute_B(self, x):
        """
        生成B
        :param x:
        :return:
        """
        b = random.randint(1, self.order - 2)
        u = random.randint(1, self.order - 2)
        B = self.curve.add(x * self.generator_point, b * self.generator_point)
        return B, b, u

    def compute_key(self, A, x, u, b):
        """
        计算临时密钥
        :param A:
        :param x:
        :param u:
        :param b:
        :return:
        """
        temp = self.curve.mul(x*u, self.generator_point)
        s = self.curve.add(A, temp)
        S = self.curve.mul(b, s)
        K = self.HashFunc.Hash(self.curve.to_bytes(S))
        return K

    def random_data(self):
        """
        生成随机数a和点A
        :return:
        """
        a = random.randint(1, self.order - 2)
        A = a * self.generator_point
        return A, a

    def verfy_M1(self, A, B, K, M1):
        """
        验证接收到的M1
        :param A:
        :param B:
        :param K:
        :param M1: 接收到的M1
        :return:
        """
        _M1 = self.curve.to_bytes(A) + self.curve.to_bytes(B) + str(K).encode('utf-8')
        _M1 = self.HashFunc.Hash(_M1)
        if (M1 != _M1):
            print("FAULT!!!")
            return False
        return True

    def compute_M2(self, A, M1, K):
        """
        计算M2
        :param A:
        :param M1:
        :param K:
        :return:
        """
        return self.HashFunc.Hash(self.curve.to_bytes(A) + str(M1).encode("UTF-8") + str(K).encode('utf-8'))

    def decrypt(self, K: int, cipher: bytes):
        """
        解密对方的身份标识公钥
        :param K: 临时密钥
        :param cipher: 接收到的密文
        :return:
        """
        key = self.SysmCipher.PadKey(str(K).encode())
        decryptTest = self.SysmCipher.DeCrypt(key, cipher)
        return self.curve.from_bytes(decryptTest)

    def encrypt(self, K, public_key):
        """
        加密身份标识公钥
        :param K: IoT设备生成的临时密钥
        :param public_key: IoT设备的身份标识公钥
        :return:
        """
        key = self.SysmCipher.PadKey(str(K).encode())
        cipher_iot = self.SysmCipher.EnCrypt(key, self.curve.to_bytes(public_key))
        return cipher_iot
    
    
    def compute_ssk(self, y, Z):
        """
        计算会话密钥
        :param y: IoT主控设备生成的随机数
        :param Z: IoT主控设备接收到的点
        :return:
        """
        Z = self.curve.from_bytes(Z)
        ssk = self.curve.mul(y, Z)
        return self.curve.to_bytes(ssk)

    def dec_vrfy(self, cipher, ssk, Z, Y, public_key_iot):
        """
        接收密文并验证签名
        :param cipher:
        :param ssk:
        :param Z:
        :param Y:
        :param public_key_iot:
        :return:
        """
        key = self.SysmCipher.PadKey(ssk)
        decryptTest = self.SysmCipher.DeCrypt(key, cipher)
        Z = self.curve.from_bytes(Z)
        m = self.curve.add(Z, Y)
        message = self.curve.to_bytes(m)
        public_key_iot = sv.gen_public_key(public_key_iot)
        sv.verify(message, decryptTest, public_key_iot)

    def enc_sign(self, Z, Y, ssk):
        """
        加密签名
        :param Z:
        :param Y:
        :param ssk:
        :return:
        """
        Z = self.curve.from_bytes(Z)
        m = self.curve.add(Y, Z)
        message = self.curve.to_bytes(m)
        sign = sv.sign(message, self.private_key_iots)
        key = self.SysmCipher.PadKey(ssk)
        cipher = self.SysmCipher.EnCrypt(key, sign)
        return cipher


