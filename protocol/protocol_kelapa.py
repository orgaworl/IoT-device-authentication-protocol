import random
import socket
from Crypto.Util.number import *
from common import SM4
from common import SM3HashComp
from common import curve_ed25519 as _curve
from common import generate_qr as QR
from common import get_random_num




class Protocol_kelapa_c_action:
    # 获取曲线的阶和生成元的点
    curve = _curve.Curve()
    order = curve.order
    generator_point = curve.generator_point
    private_key = 2024
    public_key = private_key * generator_point

    # 生成对称加解密方案
    SysmCipher = SM4()
    HashFunc=SM3HashComp()
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
        QR_hash = self.HashFunc.Hash(QR_string)             # 计算二维码的哈希值
        key = self.HashFunc.two_hashed_OPRF(kc, QR_string, QR_hash, self.order)  # 计算临时密钥
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

        e = self.HashFunc.Hash(X_byte + public_key_iot_byte)
        d = self.HashFunc.Hash(Y_byte + public_key_iots_byte)
        theta_c = (e * private_key_iot + y) % self.order
        ssk_temp = theta_c * (X + d * public_key_iots)
        ssk = self.HashFunc.Hash(self.curve.to_bytes(ssk_temp))
        return ssk



def Protocol_kelapa_c(HOST: str, port: int,passwd:str,debug:bool=False) -> None:
    """
    IoT设备参与协议的运行
     :param HOST:IoT主控设备的IP地址
    :param port: 端口号
    :return:
    """
    # 系统初始化
    IoT = Protocol_kelapa_c_action()
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect((HOST, port))

    
    # Step One Iot设备生成二维码或者PIN码
    if debug:print(f"[key] passwd:\n[val] {passwd}")
    QR = IoT.create_QR(passwd)
    socket_client.send(QR.encode("UTF-8"))
    if debug:print(f"[com] gen qrcode")
    
    # Step Two  Iot设备接收alpha，计算临时密钥K
    alpha = socket_client.recv(1024).decode("UTF-8")  # 接受来自Iot主控设备的alpha
    
    alpha = int(alpha)
    if debug:print(f"[key] recv alpha:\n[val] {hex(alpha)}")
    key, kc = IoT.compute_key(QR)  # 生成随机数kc和计算临时密钥key

    # Step Three Iot设备计算身份标识公钥的密文和beta，发送给Iot主控设备
    beta = IoT.compute_beta(alpha, kc)
    cipher_iot = IoT.compute_cipher(IoT.public_key, key.encode('utf-8'))
    socket_client.send(cipher_iot)
    socket_client.send(str(beta).encode("UTF-8"))
    if debug:print(f"[key] send pk cipher:\n[val] 0x{cipher_iot.hex()}")
    if debug:print(f"[key] send beta:\n[val] {hex(beta)}", )

    # Step Four Iot设备接收密文并解密，验证
    cipher_iots = socket_client.recv(1024)  # 接受来自Iot主控设备的加密身份标识公钥bytes类型
    public_key_iots = IoT.DeCrypt(0, cipher_iots, key.encode('utf-8'))   # 解密，point类型

    # Step Five Iot设备计算Y并发送
    Y, y = IoT.random_data_mark()
    socket_client.send(IoT.curve.to_bytes(Y))
    if debug:print("[com] verify pk")
    
    # Step Six  Iot设备接收X
    X_data = socket_client.recv(1024)
    X = IoT.curve.from_bytes(X_data)    # 接受来自Iot主控设备的X(point类型)
    if debug:print(f"[key] send Y:\n[val] {hex(Y.x)}{hex(Y.y)[2:]}")
    
    # Step Seven - Nine  Iot设备计算会话密钥ssk
    ssk = IoT.compute_ssk(X, Y, y, public_key_iots, IoT.public_key, IoT.private_key)
    if debug:print(f"[key] gen session key:\n[val] {hex(ssk)}")
    print(f"[SUC] {hex(ssk)}")
    # 关闭连接
    socket_client.close()
    




class Protocol_kelapa_s_action:
    # 获取曲线的阶和生成元的点
    curve = _curve.Curve()
    order = curve.order
    generator_point = curve.generator_point

    # 生成IoT设备身份标识私钥和公钥
    private_key = 4046
    public_key = private_key * generator_point

    # 生成SysmCipher加解密方案
    SysmCipher = SM4()
    HashFunc=SM3HashComp()
    def generate_alpha(self, QR_string: str) -> (str, int):
        """
        IoT主控设备生成随机数r, 计算alpha
        :param QR_string: 得到的二维码
        :return:
        """
        r = get_random_num.generate_prime(self.order)
        QR_string_hash = self.HashFunc.Hash(QR_string)
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
        key = self.HashFunc.two_hashed_OPRF(r_inverse, QR_string, beta, self.order)
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

        e = self.HashFunc.Hash(X_byte + public_key_iot_byte)
        d = self.HashFunc.Hash(Y_byte + public_key_iots_byte)

        theta_s = (d * private_key_iots + x) % self.order
        ssk_temp = theta_s * (Y + e * public_key_iot)
        ssk = self.HashFunc.Hash(self.curve.to_bytes(ssk_temp))
        return ssk
    

def Protocol_kelapa_s(HOST: str, port: int) -> None:
    """
    IoT主控设备参与协议的运行
    :param HOST: IoT设备的IP
    :param port: 端口号
    :return:
    """
    IoTs = Protocol_kelapa_s_action()
    # 建立socket连接
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 端口号复用
    socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_server.bind((HOST, port))
    # 监听端口
    socket_server.listen(1)
    conn, address = socket_server.accept()

    # Step One  IoT主控设备扫码
    QR = conn.recv(1024).decode("UTF-8")    # 接收pwd，str类型
    print(f"[key] scan qrcode:\n[val] {QR} ")
    # Step Two  IoT主控设备发送alpha
    alpha, r = IoTs.generate_alpha(QR)      # alpha是字符串类型
    print(f"[key] gen and send alpha:\n[val] {alpha} ")
    conn.send(alpha.encode("UTF-8"))        # 发送bytes类型
    

    # Step Three  IoT主控接收beta与密文
    cipher_iot = conn.recv(1024)
    beta = conn.recv(1024).decode("UTF-8")    # 接收到的beta转str类型
    beta = int(beta)

    # Step Four   IoT主控计算临时密钥K，解密密文，验证密文，发送加密后的自己的身份标识公钥
    cipher_iots, public_key_iot, key = IoTs.compute_key_cipher(QR, r, beta, cipher_iot, IoTs.public_key)
    conn.send(cipher_iots)  # 发送加密后的身份标识公钥
    #print(f"[key] IoT主控设备发送的身份标识公钥密文:\n[val] 0x{cipher_iots.hex()} ")
    print(f"[key] recv pk cipher:\n[val] 0x{cipher_iots.hex()} ")
    print(f"[com] verify pk cipher success")
    # Step Five   IoT主控设备接收Y,转为点类型
    Y_data = conn.recv(1024)
    Y = IoTs.curve.from_bytes(Y_data)

    # Step Six IoT主控设备计算X，发送X
    X, x = IoTs.random_data_mark()
    conn.send(IoTs.curve.to_bytes(X))  # 发送X
    print(f"[key] recv X:\n[val] {hex(X.x)}{hex(X.y)[2:]} ")

    # Step Seven - Nine  协商会话密钥ssk
    ssk = IoTs.compute_ssk(X, Y, x, IoTs.public_key, public_key_iot, IoTs.private_key)
    print(f"[SUC] {hex(ssk)}")
    # 关闭连接
    conn.close()
    socket_server.close()

