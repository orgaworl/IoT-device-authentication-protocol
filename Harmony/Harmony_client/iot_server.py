import socket
import IoT_main


def Protocol_Iots(HOST: str, port: int) -> bool:
    """
    IoT主控设备参与协议的运行
    :param HOST: IoT设备IP地址
    :param port: 端口号
    :return:
    """

    IoTs = IoT_main.IoT_Control()
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

    # Step Two  IoT主控设备接收A
    A = conn.recv(1024)
    A = IoTs.curve.from_bytes(A)

    # Step Three  IoT主控设备计算B，发送B和u
    B, b, u = IoTs.compute_B(x)
    conn.send(IoTs.curve.to_bytes(B))
    conn.send(str(u).encode('utf-8'))

    # Step Four-Five   IoT主控设备计算S和临时密钥K
    K = IoTs.compute_key(A, x, u, b)

    # Step Six IoT主控设备接收M1，验证M1
    M1 = conn.recv(1024).decode('utf-8')
    M1 = int(M1)
    if IoTs.verfy_M1(A, B, K, M1) == 0:
        return False

    # Step Seven IoT主控设备计算M2
    M2 = IoTs.compute_M2(A, M1, K)
    conn.send(str(M2).encode('utf-8'))

    # Step Eight IoT设备解密密文
    cipher = conn.recv(1024)
    public_key_iot = IoTs.decrypt(K, cipher)

    # Step Nine IoT主控设备加密传输身份标识公钥c2
    c2 = IoTs.encrypt(K, IoTs.public_key)
    conn.send(c2)

    # Step ten IoT主控设备生成随机数y和点Y
    Y, y = IoTs.random_data()
    conn.send(IoTs.curve.to_bytes(Y))

    # Step 11 IoT主控设备接收密文和Z
    cipher_iot = conn.recv(1024)
    Z = conn.recv(1024)

    # Step 12-13 IoT主控设备计算会话密钥，解密密文, 验证签名
    ssk = IoTs.compute_ssk(y, Z)
    IoTs.dec_vrfy(cipher_iot, ssk, Z, Y, public_key_iot)

    # Step 14 IoT主控设备签名，加密
    cipher_iots = IoTs.enc_sign(Z, Y, ssk)
    conn.send(cipher_iots)

    print("协商会话密钥: ", ssk)
    # 关闭连接
    conn.close()
    socket_server.close()


if __name__ == '__main__':
    # 如有问题，修改端口号
    HOST = '0.0.0.0'
    Port = 439
    Protocol_Iots(HOST, Port)
