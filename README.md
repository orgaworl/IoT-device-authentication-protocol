## Introdunction

This repository contains two protocal for IoT device authentication.

- Harmony Open

- Our Solution:  Kelapa

We implement the new solution Kelapa for IoT device authetication with less interaction and higher performence.

## Required dependencies

### R1: Software

**for ubuntu**
```shell
sudo apt install gcc g++ git build-essentials cmake python
```

### R2: Python packages

```shell
pip install -r requirements.txt
```

### R3: GmSSL
已测试版本: GmSSL-3.1.1

**for Linux**

```shell
git clone https://gitee.com/mirrors/GmSSL.git
cd ./GmSSL/
mkdir build
cd build
cmake ..
make
make test
sudo make install
```

**for windows**

从[github](https://github.com/guanzhi/GmSSL)上下载GmSSL[安装包](https://github.com/guanzhi/GmSSL/releases/download/v3.1.1/GmSSL-3.1.1-win64.exe)并安装.

将GmSSL动态库的路径加入环境变量,默认情况下动态库路径为:
```
C:\Program Files\GmSSL 3.1.1\bin
```

### R4: electron
```shell
cd electronSrc
npm install --save-dev electron
npm install --save @electron/remote
npm start
```




## Usage
### use python script only

```shell
python progClient.py --ip <ip> --port <port> --passwd <passwd>
```

All parameters have default values:

 - ip: 127.0.0.1
 - port: 4398
 - passwd: "passwd"


You can also specify their values using the command line.

### user gui