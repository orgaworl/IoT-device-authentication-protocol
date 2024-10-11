import socket
import iot


def Protocol_Iot(HOST: str, port: int) -> None:
    """
    IoT设备参与协议的运行
     :param HOST:IoT主控设备的IP地址
    :param port: 端口号
    :return:
    """
    # 系统初始化
    IoT = iot.Iot()
    # 创建socket对象
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 连接到服务器
    socket_client.connect((HOST, port))
    # 协议开始
    # Step One Iot设备生成二维码或者PIN码
    QR = IoT.create_QR()
    socket_client.send(QR.encode("UTF-8"))
    print("IoT设备成功发送二维码\n")
    # Step Two  Iot设备接收alpha，计算临时密钥K
    alpha = socket_client.recv(1024).decode("UTF-8")  # 接受来自Iot主控设备的alpha
    alpha = int(alpha)
    key, kc = IoT.compute_key(QR)  # 生成随机数kc和计算临时密钥key

    # Step Three Iot设备计算身份标识公钥的密文和beta，发送给Iot主控设备
    beta = IoT.compute_beta(alpha, kc)
    cipher_iot = IoT.compute_cipher(IoT.public_key, key.encode('utf-8'))
    socket_client.send(cipher_iot)
    socket_client.send(str(beta).encode("UTF-8"))

    print("IoT设备发送的身份标识公钥密文: ", cipher_iot, '\n')
    print("IoT设备发送的beta: ", beta, '\n')

    # Step Four Iot设备接收密文并解密，验证
    cipher_iots = socket_client.recv(1024)  # 接受来自Iot主控设备的加密身份标识公钥bytes类型
    public_key_iots = IoT.DeCrypt(0, cipher_iots, key.encode('utf-8'))   # 解密，point类型

    # Step Five Iot设备计算Y并发送
    Y, y = IoT.random_data_mark()
    socket_client.send(IoT.curve.to_bytes(Y))
    print("IoT设备成功验证IoT主控设备公钥\n")
    # Step Six  Iot设备接收X
    X_data = socket_client.recv(1024)
    X = IoT.curve.from_bytes(X_data)    # 接受来自Iot主控设备的X(point类型)
    print("IOT设备发送的Y：", Y, '\n')

    # Step Seven - Nine  Iot设备计算会话密钥ssk
    ssk = IoT.compute_ssk(X, Y, y, public_key_iots, IoT.public_key, IoT.private_key)
    print("IoT设备最终协商的会话密钥", ssk)
    # 关闭连接
    socket_client.close()


if __name__ == '__main__':
    # 如有问题，可以修改端口号
    HOST = input("请输入移动设备的IP地址:")
    port = 4398
    Protocol_Iot(HOST, port)




