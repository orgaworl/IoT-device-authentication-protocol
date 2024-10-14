import socket
import actionClient
import sys, getopt
def Protocol_Iot(HOST: str, port: int,passwd:str) -> None:
    """
    IoT设备参与协议的运行
     :param HOST:IoT主控设备的IP地址
    :param port: 端口号
    :return:
    """
    # 系统初始化
    IoT = actionClient.Iot()
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect((HOST, port))

    
    # Step One Iot设备生成二维码或者PIN码
    print(f"[key] IoT设备输入口令:\n[val] {passwd}")
    QR = IoT.create_QR(passwd)
    socket_client.send(QR.encode("UTF-8"))
    print(f"[com] IoT设备生成二维码")
    
    # Step Two  Iot设备接收alpha，计算临时密钥K
    alpha = socket_client.recv(1024).decode("UTF-8")  # 接受来自Iot主控设备的alpha
    alpha = int(alpha)
    key, kc = IoT.compute_key(QR)  # 生成随机数kc和计算临时密钥key

    # Step Three Iot设备计算身份标识公钥的密文和beta，发送给Iot主控设备
    beta = IoT.compute_beta(alpha, kc)
    cipher_iot = IoT.compute_cipher(IoT.public_key, key.encode('utf-8'))
    socket_client.send(cipher_iot)
    socket_client.send(str(beta).encode("UTF-8"))
    print(f"[key] IoT设备发送的身份标识公钥密文:\n[val] 0x{cipher_iot.hex()}")
    print(f"[key] IoT设备发送参数beta:\n[val] {hex(beta)}", )

    # Step Four Iot设备接收密文并解密，验证
    cipher_iots = socket_client.recv(1024)  # 接受来自Iot主控设备的加密身份标识公钥bytes类型
    public_key_iots = IoT.DeCrypt(0, cipher_iots, key.encode('utf-8'))   # 解密，point类型

    # Step Five Iot设备计算Y并发送
    Y, y = IoT.random_data_mark()
    socket_client.send(IoT.curve.to_bytes(Y))
    print("[com] IoT设备成功验证IoT主控设备公钥")
    
    # Step Six  Iot设备接收X
    X_data = socket_client.recv(1024)
    X = IoT.curve.from_bytes(X_data)    # 接受来自Iot主控设备的X(point类型)
    print(f"[key] IOT设备发送参数Y:\n[val] {hex(Y.x)}{hex(Y.y)[2:]}")
    
    # Step Seven - Nine  Iot设备计算会话密钥ssk
    ssk = IoT.compute_ssk(X, Y, y, public_key_iots, IoT.public_key, IoT.private_key)
    print(f"[key] IoT设备最终协商的会话密钥:\n[val] {hex(ssk)}")
    # 关闭连接
    socket_client.close()
    


if __name__ == '__main__':
    try:
        argv=sys.argv[1:]
        opts, args = getopt.getopt(argv,"h",["ip=","port=","passwd="])
    except getopt.GetoptError:
        print('progClient.py --ip <ip> --port <port> --passwd <password>')
    HOST="127.0.0.1"
    port = 4398
    passwd="passwd"
    for opt, arg in opts:
        if opt == '-h':
            print("progClient.py --ip <ip> --port <port> --passwd <password>")
            sys.exit()
        elif opt in ("--ip"):
            HOST=arg
        elif opt in ("--port"):
            port=arg
        elif opt in ("--passwd"):
            passwd=arg
    try:
        Protocol_Iot(HOST, int(port),passwd)
    except socket.error:
        print("[ERR] socket Error")




