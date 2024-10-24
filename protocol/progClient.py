
import socket
import random
import sys, getopt


from protocol_kelapa import Protocol_kelapa_c
from protocol_harmony import Protocol_harmony_c




def bench_mark(protocol,HOST: str, port: int,passwd:str,debug:bool=False,loopTime=150,passwdLen=16):
    import time
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    timeList=[]
    # get time
    for testTime in range(loopTime):
        try:
            start_time=time.time()
            protocol(HOST, int(port),passwd,debug)
            end_time=time.time()
            timeList.append(end_time-start_time)
        except socket.error:
            print("[ERR] socket Error")
        time.sleep(1)
    dataLen=len(timeList)
    timeList=timeList[dataLen//10:dataLen-dataLen//10]
    plt.plot([i+1 for i in range(len(timeList))],timeList)
    plt.show()
    with open(f"../benchmark/{protocol.__name__}.csv",mode="w",encoding="utf-8") as f:
        res=pd.DataFrame()
        res.insert(loc=len(res.columns),column='test order',value=[i+1 for i in range(len(timeList))])
        res.insert(loc=len(res.columns),column='cost time',value=timeList)
        res.to_csv(f,header=True,index=False,lineterminator='\n')
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
        opts, args = getopt.getopt(argv,"h",["benchmark","ip=","port=","passwd=","protocol=","debug"])
    except getopt.GetoptError:
        print(helpMessage)
        sys.exit()
    HOST="127.0.0.1"
    #HOST="192.168.31.222"
    port = 4398
    passwd="passwd"
    protocol=Protocol_kelapa_c
    flow_choice=0
    debug=False
    for opt, arg in opts:
        if opt == '-h':
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
        elif opt =="--benchmark":
            flow_choice=1
        elif opt =="--debug":
            debug=True
        else:
            print("invalid argument")
            sys.exit()


    if(flow_choice==0):
        try:
            protocol(HOST, int(port),passwd,debug)
        except socket.timeout:
            print("[ERR] socket timeout")
        except socket.error:
            print("[ERR] socket error")
        except Exception as e:
            print(f"[ERR] {e}")
    elif (flow_choice==1):
        bench_mark(protocol,HOST, int(port),passwd,debug)




