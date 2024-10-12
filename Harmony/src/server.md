# Harmony Open设备互联认证协议代码

## 项目文件说明

1. aes.py AES加解密程序

2. curve_ed25519.py 椭圆曲线Ed25519类

3. generate_qr.py 生成动态二维码及解析二维码

4. SHA256.py SHA256哈希函数

5. iot.py IoT设备的类，包含IoT设备的初始化，以及IoT设备相关函数

6. iot_client.py IoT设备运行协议的代码

7. IoT_main.py IoT主控设备的类

8. iot_server.py IoT主控设备运行协议的代码

9. test_QR.png IoT设备生成的二维码图片

## 项目代码执行

### 运行的环境

安卓手机，提前安装termux。

python3.9及以上

### 运行的注意事项

本文件运行在手机中，模拟协议的执行过程。请确保移动设备和PC设备属于同一个局域网。如果运行后提示

```
    OSError: [WinError 10048] 通常每个套接字地址(协议/网络地址/端口)只允许使用一次
```

<u>**说明端口被占用，请打开iot_client.py和iot_server.py，更换端口号port(使用相同的端口号)，范围在1到65535**.</u>

## 运行说明

### 第一步

打开Harmony_server项目文件位置所在的命令行，安装代码调用的包  

```
 pip install -r requirements.txt
```

### 第二步

打开Harmony_server项目文件位置所在的命令行，运行iot_server.py程序(Harmony_server下载到移动设备中)

```
python iot_server.py
```

### 第三步

打开Harmony_client项目文件位置所在的命令行，运行iot_client.py程序

```
python iot_client.py
```

### 第四步

在PC端输入移动设备的IP地址
