import random
import SHA256
import aes
import sign_verfy as sv
import generate_qr as QR
import curve_ed25519 as _curve


class Iot:
    # 获取曲线的阶和生成元的点
    curve = _curve.Curve()
    order = curve.order
    generator_point = curve.generator_point
    private_key = 2024
    public_key = private_key * generator_point
    private_key_iot = sv.gen_private_key(private_key)
    public_key_iot = sv.gen_public_key(public_key)

    # 生成AES加解密方案
    AES = aes.Aes(16)

    def create_QR(self) -> str:
        """
        产生动态二维码，输出二维码的字符串解析
        :return:
        """
        QR_name = QR.get_qr()   # 二维码名字, 可以查看二维码图片
        QR_string = QR.trans_bytes(QR_name)
        return QR_string

    def create_salt(self) -> str:
        """
        产生盐值
        :return:
        """
        alphabet = 'abcdefghijklmnopqrstuvwxyz!@#$%^&*()'
        characters_salt = random.sample(alphabet, 9)
        return str(characters_salt)

    def random_data(self):
        """
        生成随机数a和点A
        :return:
        """
        a = random.randint(1, self.order - 2)
        A = a * self.generator_point
        return A, a

    def comupte_key(self, B, salt, a, u, QR):
        """
        生成临时密钥key
        :param B: IoT主控设备发送的点B
        :param salt: 盐值
        :param a: 随机数a
        :param u: IoT主控设备发送的随机数u
        :param QR: 二维码
        :return:
        """
        x = SHA256.Hash(QR + salt)
        S = self.curve.sub(B, x * self.generator_point)
        S = self.curve.mul(a + u * x, S)
        K = SHA256.Hash(self.curve.to_bytes(S))
        return K

    def compute_M1(self, A, B, K):
        """
        计算M1
        :param A:
        :param B:
        :param K:
        :return:
        """
        return SHA256.Hash(self.curve.to_bytes(A) + self.curve.to_bytes(B) + str(K).encode('utf-8'))

    def verfy_M2(self, A, M1, K, M2):
        """
        验证接收到的M2
        :param A:
        :param M1:
        :param K:
        :param M2: 接收到的M2
        :return:
        """
        _M2 = self.curve.to_bytes(A) + str(M1).encode("UTF-8") + str(K).encode('utf-8')
        _M2 = SHA256.Hash(_M2)
        if (M2 != _M2):
            print("FAULT!!!")
            return False
        return True

    def encrypt(self, K, public_key):
        """
        加密身份标识公钥
        :param K: IoT设备生成的临时密钥
        :param public_key: IoT设备的身份标识公钥
        :return:
        """
        key = self.AES.PadKey(str(K).encode())
        cipher_iot = self.AES.EnCrypt(key, self.curve.to_bytes(public_key))
        return cipher_iot

    def decrypt(self, K: int, cipher: bytes):
        """
        解密对方的身份标识公钥
        :param K: 临时密钥
        :param cipher: 接收到的密文
        :return:
        """
        key = self.AES.PadKey(str(K).encode())
        decryptTest =self.AES.DeCrypt(key, cipher)
        return self.curve.from_bytes(decryptTest)

    def compute_ssk(self, z, Y):
        """
        计算会话密钥
        :param z: IoT设备生成的随机数
        :param Y: IoT设备接收到的点
        :return:
        """
        Y = self.curve.from_bytes(Y)
        ssk = self.curve.mul(z, Y)
        return self.curve.to_bytes(ssk)

    def enc_sign(self, Z, Y, ssk):
        """
        加密签名
        :param Z:
        :param Y:
        :param ssk:
        :return:
        """
        Y = self.curve.from_bytes(Y)
        m = self.curve.add(Z, Y)
        message = self.curve.to_bytes(m)
        sign = sv.sign(message, self.private_key_iot)
        key = self.AES.PadKey(ssk)
        cipher = self.AES.EnCrypt(key, sign)
        return cipher

    def dec_vrfy(self, cipher, ssk, Z, Y, public_key_iots):
        """
        接收密文并验证签名
        :param cipher:
        :param ssk:
        :param Z:
        :param Y:
        :param public_key_iots:
        :return:
        """
        key = self.AES.PadKey(ssk)
        decryptTest = self.AES.DeCrypt(key, cipher)
        Y = self.curve.from_bytes(Y)
        m = self.curve.add(Y, Z)
        message = self.curve.to_bytes(m)
        public_key_iots = sv.gen_public_key(public_key_iots)
        sv.verify(message, decryptTest, public_key_iots)





