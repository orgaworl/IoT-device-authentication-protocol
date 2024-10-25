
## 组成
### common

1. curve_ed25519.py 椭圆曲线Ed25519类

2. generate_qr.py   生成动态二维码及解析二维码

3. get_random_num.py 生成与群的阶的欧拉函数值互素的随机数

4. oprf.py    OPRF函数和SM3哈希函数

5. sign_verify.py 数字签名与验证

6. SM4.py SM4加解密程序

### protocol_*.py

1. protocol_kelapa.py  实现了kelapa认证协议

2. protocol_harmony.py  实现了HarmonyOpen认证协议

### prog*.py

1. progClient.py  认证协议的物联网设备端

2. progServer.py  认证协议的主控设备端

## 项目代码执行

```
[ERR]socket error
```

说明端口被占用，请打开iot_client.py和iot_server.py，更换端口号port(使用相同的端口号)，范围在1到65535
