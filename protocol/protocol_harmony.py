import random
import socket
import time
from common import SM4
from common import SM3HashComp
from common import sign_verify as sv
from common import curve_ed25519 as _curve
from common import generate_qr as QR


class Protocol_harmony_c_action:
    # 获取曲线的阶和生成元的点
    curve = _curve.Curve()
    order = curve.order
    generator_point = curve.generator_point
    private_key = 2024
    public_key = private_key * generator_point
    private_key_iot = sv.gen_private_key(private_key)
    public_key_iot = sv.gen_public_key(public_key)

    # 生成AES加解密方案
    SysmCipher = SM4()
    HashFunc=SM3HashComp()
    def create_QR(self,passwd:str) -> str:
        """
        产生动态二维码，输出二维码的字符串解析
        :return:
        """
        QR_name = QR.get_qr(passwd)   # 二维码名字, 可以查看二维码图片
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
        x = self.HashFunc.Hash(QR + salt)
        S = self.curve.sub(B, x * self.generator_point)
        S = self.curve.mul(a + u * x, S)
        K = self.HashFunc.Hash(self.curve.to_bytes(S))
        return K

    def compute_M1(self, A, B, K):
        """
        计算M1
        :param A:
        :param B:
        :param K:
        :return:
        """
        return self.HashFunc.Hash(self.curve.to_bytes(A) + self.curve.to_bytes(B) + str(K).encode('utf-8'))

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
        _M2 = self.HashFunc.Hash(_M2)
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
        key = self.SysmCipher.PadKey(str(K).encode())
        cipher_iot = self.SysmCipher.EnCrypt(key, self.curve.to_bytes(public_key))
        return cipher_iot

    def decrypt(self, K: int, cipher: bytes):
        """
        解密对方的身份标识公钥
        :param K: 临时密钥
        :param cipher: 接收到的密文
        :return:
        """
        key = self.SysmCipher.PadKey(str(K).encode())
        decryptTest =self.SysmCipher.DeCrypt(key, cipher)
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
        key = self.SysmCipher.PadKey(ssk)
        cipher = self.SysmCipher.EnCrypt(key, sign)
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
        key = self.SysmCipher.PadKey(ssk)
        decryptTest = self.SysmCipher.DeCrypt(key, cipher)
        Y = self.curve.from_bytes(Y)
        m = self.curve.add(Y, Z)
        message = self.curve.to_bytes(m)
        public_key_iots = sv.gen_public_key(public_key_iots)
        sv.verify(message, decryptTest, public_key_iots)


def Protocol_harmony_c(HOST: str, port: int, passwd:str,debug:bool=False) -> bool:
    """
    IoT设备参与协议的运行
    :param HOST:IoT主控设备IP地址
    :param port:端口号
    :return:
    """
    # 系统初始化
    IoT = Protocol_harmony_c_action()
    # 创建socket对象
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 连接到服务器
    socket_client.connect((HOST, port))

    # 协议开始
    # Step One Iot设备生成二维码或者PIN码以及盐
    QR = IoT.create_QR(passwd)
    salt = IoT.create_salt()
    socket_client.send((QR+salt).encode("UTF-8"))

    # Step Two IoT设备计算A
    A, a = IoT.random_data()
    socket_client.send(IoT.curve.to_bytes(A))

    # Step Three Iot设备接收B和u
    B = socket_client.recv(1024)
    if debug: print(f"[key] send parameter <B>\n[val] 0x{B.hex()}")
    u = socket_client.recv(1024)
    if debug: print(f"[key] send parameter <u>:\n[val] {u}")
    B = IoT.curve.from_bytes(B)
    u = int(u)

    # Step Four_FIVE Iot设备计算S和K
    K = IoT.comupte_key(B, salt, a, u, QR)

    # Step Six IoT设备计算M1发送M1
    M1 = IoT.compute_M1(A, B, K)
    socket_client.send(str(M1).encode('utf-8'))
    if debug: print(f"[key] send parameter <M1>:\n[val] {M1}")
    # Step Seven IoT设备验证M2
    M2 = socket_client.recv(1024).decode('utf-8')
    M2 = int(M2)
    if IoT.verfy_M2(A, M1, K, M2) == 0:
        return False
    if debug: print(f"[sta] verify parameter <M2> successful")
    # Step Eight IoT设备加密传输身份标识公钥c1
    c1 = IoT.encrypt(K, IoT.public_key)
    socket_client.send(c1)
    if debug: print(f"[key] send parameter <c1>:\n[val] 0x{c1.hex()}")
    # Step Nine IoT设备解密接收到的签名公钥
    cipher = socket_client.recv(1024)
    public_key_iots = IoT.decrypt(K, cipher)

    # Step Ten IoT设备接收Y，生成Z和z
    Y = socket_client.recv(1024)
    Z, z = IoT.random_data()

    # Step 11 IoT设备生成ssk
    ssk = IoT.compute_ssk(z, Y)

    # Step 12-13 IoT设备生成签名和加密
    cipher_iot = IoT.enc_sign(Z, Y, ssk)

    # Step 14 IoT设备发送Z和密文，接收Y
    socket_client.send(cipher_iot)
    socket_client.send(IoT.curve.to_bytes(Z))
    cipher_iots = socket_client.recv(1024)

    # Step 15 IoT设备解密并验证签名
    IoT.dec_vrfy(cipher_iots, ssk, Z, Y, public_key_iots)

    print(f"[SUC] 0x{ssk.hex()}")



class Protocol_harmony_s_action:
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




def Protocol_harmony_s(HOST: str, port: int,debug:bool=False) -> bool:
    """
    IoT主控设备参与协议的运行
    :param HOST: IoT设备IP地址
    :param port: 端口号
    :return:
    """

    IoTs = Protocol_harmony_s_action()
    # 建立socket连接
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 端口号复用
    
    socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_server.bind((HOST, port))
    # 监听端口
    socket_server.listen(1)
    conn, address = socket_server.accept()
    
    # Step One  IoT主控设备扫码计算x
    QR_salt = conn.recv(1024).decode("UTF-8")    # 接收pwd，str类型
    x = IoTs.compute_x(QR_salt)
    if debug: print("[sta] scan qr-code\n")
    # Step Two  IoT主控设备接收A
    A = conn.recv(1024)
    A = IoTs.curve.from_bytes(A)

    # Step Three  IoT主控设备计算B，发送B和u
    B, b, u = IoTs.compute_B(x)
    B_bytes= IoTs.curve.to_bytes(B)
    conn.send(B_bytes)
    time.sleep(0.01)  # in case send two package together
    if debug: print(f"[key] send parameter <B>\n[val] {B_bytes}")
    if debug: print(f"[key] send parameter <u>\n[val] {hex(u)}")
    conn.send(str(u).encode('utf-8'))

    # Step Four-Five   IoT主控设备计算S和临时密钥K
    K = IoTs.compute_key(A, x, u, b)

    # Step Six IoT主控设备接收M1，验证M1
    M1 = conn.recv(1024).decode('utf-8')
    #if debug: print(f"M1:{M1}")
    M1 = int(M1)
    if IoTs.verfy_M1(A, B, K, M1) == 0:
        return False

    # Step Seven IoT主控设备计算M2
    M2 = IoTs.compute_M2(A, M1, K)
    if debug: print(f"[key] send parameter <M2>:\n[val] {M2}")
    conn.send(str(M2).encode('utf-8'))

    # Step Eight IoT设备解密密文
    cipher = conn.recv(1024)
    public_key_iot = IoTs.decrypt(K, cipher)

    # Step Nine IoT主控设备加密传输身份标识公钥c2
    c2 = IoTs.encrypt(K, IoTs.public_key)
    conn.send(c2)
    if debug: print(f"[key] send parameter <encrypted identity public key>\n[val] {c2}")

    # Step ten IoT主控设备生成随机数y和点Y
    Y, y = IoTs.random_data()
    if debug: print(f"[key] send parameter <Y>\n[val]{Y}")
    conn.send(IoTs.curve.to_bytes(Y))

    # Step 11 IoT主控设备接收密文和Z
    cipher_iot = conn.recv(1024)
    Z = conn.recv(1024)

    # Step 12-13 IoT主控设备计算会话密钥，解密密文, 验证签名
    ssk = IoTs.compute_ssk(y, Z)
    IoTs.dec_vrfy(cipher_iot, ssk, Z, Y, public_key_iot)

    # Step 14 IoT主控设备签名，加密
    cipher_iots = IoTs.enc_sign(Z, Y, ssk)
    if debug: print(f"[key] send parameter <encrypted signature>\n[val] 0x{cipher_iots.hex()}")
    conn.send(cipher_iots)

    print(f"[SUC] {ssk.hex()}")
    # 关闭连接
    conn.close()
    socket_server.close()