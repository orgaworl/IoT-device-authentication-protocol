import socket
import iot


def Protocol_Iot(HOST: str, port: int) -> bool:
    """
    IoT设备参与协议的运行
    :param HOST:IoT主控设备IP地址
    :param port:端口号
    :return:
    """
    # 系统初始化
    IoT = iot.Iot()
    # 创建socket对象
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 连接到服务器
    socket_client.connect((HOST, port))

    # 协议开始
    # Step One Iot设备生成二维码或者PIN码以及盐
    QR = IoT.create_QR()
    salt = IoT.create_salt()
    socket_client.send((QR+salt).encode("UTF-8"))
    print("IoT设备发送二维码\n")
    # Step Two IoT设备计算A
    A, a = IoT.random_data()
    print("IoT设备传输A: ", A, '\n')
    socket_client.send(IoT.curve.to_bytes(A))

    # Step Three Iot设备接收B和u
    B = socket_client.recv(1024)
    u = socket_client.recv(1024)
    B = IoT.curve.from_bytes(B)
    u = int(u)

    # Step Four_FIVE Iot设备计算S和K
    K = IoT.comupte_key(B, salt, a, u, QR)

    # Step Six IoT设备计算M1发送M1
    M1 = IoT.compute_M1(A, B, K)
    print("IoT设备传输M1: ", M1, '\n')
    socket_client.send(str(M1).encode('utf-8'))

    # Step Seven IoT设备验证M2
    M2 = socket_client.recv(1024).decode('utf-8')
    M2 = int(M2)
    if IoT.verfy_M2(A, M1, K, M2) == 0:
        return False

    # Step Eight IoT设备加密传输身份标识公钥c1
    c1 = IoT.encrypt(K, IoT.public_key)
    socket_client.send(c1)
    print("IoT设备传输加密后的身份标识公钥: ", c1, '\n')
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
    print("IoT设备传输加密后的签名： ", cipher_iot, '\n')
    print("IoT设备传输Z： ", Z, '\n')
    # Step 14 IoT设备发送Z和密文，接收Y
    socket_client.send(cipher_iot)
    socket_client.send(IoT.curve.to_bytes(Z))
    cipher_iots = socket_client.recv(1024)

    # Step 15 IoT设备解密并验证签名
    IoT.dec_vrfy(cipher_iots, ssk, Z, Y, public_key_iots)

    print("IoT设备协商的会话密钥是: ", ssk)


if __name__ == '__main__':
    # 如有问题，可以修改端口号
    HOST = input("请输入移动设备的IP地址：")
    port = 4390
    Protocol_Iot(HOST, port)




