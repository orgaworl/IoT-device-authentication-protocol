
import socket
import time
import random
import sys, getopt
from common import supportEC

from protocol_kelapa import Protocol_kelapa_c
from protocol_harmony import Protocol_harmony_c




def bench_mark(protocol,HOST: str, port: int,passwd:str,debug:bool=False,loopTime=100,passwdLen=100):
    import time
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt


    res_=np.ndarray(shape=(0,3))
    tested_curve_list=[]
    for curve in supportEC.curves:
        time_cost_matrix=np.ndarray(shape=(0,3))
        print(f'Testing {curve["name"]}...')
        benchmark_init_time=10
        for testTime in range(benchmark_init_time+loopTime):
            try:
                phase_time_list=protocol(HOST, int(port),passwd,curve["name"],debug)
                if testTime>=benchmark_init_time:
                    time_cost_matrix=np.vstack((time_cost_matrix,phase_time_list))
                time.sleep(0.15)
            except socket.error:
                print("[ERR] socket Error")
            except Exception as e:
                print(f"[ERR] {e}")

        #print(time_cost_matrix)
        row_len=time_cost_matrix.shape[0]
        try:
            res_=np.vstack((res_,[sum(time_cost_matrix[:,0])/row_len, sum(time_cost_matrix[:,1])/row_len, sum(time_cost_matrix[:,2])/row_len]))
            tested_curve_list.append(curve)
        except Exception as e:
            print(f"[ERR] unknow")


    # save data
    with open(f"../benchmark/{protocol.__name__}_controlled_device.csv",mode="w",encoding="utf-8") as f:
        df=pd.DataFrame()
        df.insert(loc=len(df.columns),column='curve',value=[curve["name"] for curve in tested_curve_list])
        df.insert(loc=len(df.columns),column='size',value=[curve["size"] for curve in tested_curve_list])
        df.insert(loc=len(df.columns),column='phase1 cost',value=res_[:,0])
        df.insert(loc=len(df.columns),column='phase2 cost',value=res_[:,1])
        df.insert(loc=len(df.columns),column='total cost',value=res_[:,2])
        df.to_csv(f,header=True,index=False,lineterminator='\n')
        f.close()
    
helpMessage='''
Usage:
    python progClient.py [options]

Options:
    --ip <ip>               Specify the IP address. (default "127.0.0.1")
    --port <port>           Specify the port.       (default "4398")
    --passwd <password>     Specify the password.   (defalut "passwd")
    --protocol <protocol>   Specify the protocol.   (default "kelapa")
    <--benchmark>           Record time cost.
    <--debug>               Print running details.
    
Examples:
    # run protocol for local test.
    python progClient.py  
    
    # run protocol with another device in the same LAN whose IP address is 192.168.31.100 .
    python progClient.py --ip 192.168.31.100
'''

if __name__ == '__main__':
    try:
        argv=sys.argv[1:]
        opts, args = getopt.getopt(argv,"h",["ip=","port=","passwd=","protocol=","ec=","help","debug","benchmark"])
    except getopt.GetoptError:
        sys.exit()
    HOST="127.0.0.1"
    #HOST="192.168.31.222"
    port = 4398
    passwd=random.randbytes(16).hex()
    protocol=Protocol_kelapa_c
    benchmark_flag=0
    debug=False
    benchmark_steps=False;
    curve_name="Ed25519"

    for opt, arg in opts:
        if opt in ('-h' ,"--help"):
            print(helpMessage)
            sys.exit()
        elif opt in ("--ip"):
            HOST=arg
        elif opt in ("--port"):
            port=arg
        elif opt in ("--passwd"):
            passwd=arg
        elif opt in ("--protocol"):
            if(arg=="harmony"):
                protocol=Protocol_harmony_c
            elif(arg=="kelapa"):
                protocol=Protocol_kelapa_c
            else:
                print("unknow protocol")
                sys.exit()
        elif opt in("--ec"):
            curve_name=arg
        elif opt in ("--benchmark"):
            benchmark_flag=1


        elif opt =="--debug":
            debug=True
        else:
            print("invalid argument")
            sys.exit()

    if(benchmark_flag==1):
        bench_mark(protocol,HOST, int(port),passwd,debug)
    elif(benchmark_flag==0):
        # 不断等待连接, 直到协议运行并成功协商出密钥
        while(True):
            try:
                print("waiting for connection...")
                protocol(HOST, int(port),passwd,curve_name,debug)
                time.sleep(1)
                break
            except socket.timeout:
                print("[ERR] socket timeout")
            except socket.error:
                print("[ERR] socket error")
            except Exception as e:
                print(f"[ERR] {e}")
                





