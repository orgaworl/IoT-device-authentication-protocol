
# coding=utf-8
import socket
import actionServer
import sys, getopt
def Protocol_Iots(HOST: str, port: int) -> None:
    """
    IoT主控设备参与协议的运行
    :param HOST: IoT设备的IP
    :param port: 端口号
    :return:
    """
    IoTs = actionServer.IoT_Control()
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
    conn.send(alpha.encode("UTF-8"))        # 发送bytes类型
    print(f"[key] recv alpha:\n[val] {alpha} ")

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
    print(f"[key] gen session key:\n[val] {hex(ssk)}")
    # 关闭连接
    conn.close()
    socket_server.close()


if __name__ == '__main__':
    try:
        argv=sys.argv[1:]
        opts, args = getopt.getopt(argv,"h",["ip=","port="])
    except getopt.GetoptError:
        print('progServer.py --ip <ip> --port <port>')
    HOST="127.0.0.1"
    port = 4398

    for opt, arg in opts:
        if opt == '-h':
            print("progServer.py --ip <ip> --port <port>")
            sys.exit()
        elif opt in ("--ip"):
            HOST=arg
        elif opt in ("--port"):
            port=arg
    while(1):
        try:
            Protocol_Iots(HOST, port)
        except Exception as e:
            print("[err]")
