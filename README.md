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

### R4: electron front end gui
```shell
cd electronSrc
npm install --save-dev electron
npm install --save @electron/remote
npm start #for test
npm 
```




## Usage
```shell
python progClient.py --ip <ip> --port <port> --passwd <passwd>
```

All parameters have default values:

 - ip: 127.0.0.1
 - port: 4398
 - passwd: "passwd"


You can also specify their values using the command line.

