
import socket
import random
import sys, getopt


from protocol_kelapa import Protocol_kelapa_c
from protocol_harmony import Protocol_harmony_c




def bench_mark(protocol,loopTime=150,passwdLen=16):
    import time
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    HOST="127.0.0.1"
    port = 4398
    #passwd="a"*passwdLen
    passwd=random.randbytes(passwdLen)
    timeList=[]
    # get time
    for testTime in range(loopTime):
        try:
            start_time=time.time()
            protocol(HOST, int(port),passwd)
            end_time=time.time()
            timeList.append(end_time-start_time)
        except socket.error:
            print("[ERR] socket Error")
        time.sleep(0.4)
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
    
    

if __name__ == '__main__':
    try:
        argv=sys.argv[1:]
        opts, args = getopt.getopt(argv,"h",["benchmark","ip=","port=","passwd=","protocol="])
    except getopt.GetoptError:
        print('progClient.py --ip <ip> --port <port> --passwd <password>')
        sys.exit()
    HOST="127.0.0.1"
    port = 4398
    passwd="passwd"
    protocol=Protocol_kelapa_c
    flow_choice=0
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
        else:
            print("invalid argument")
            sys.exit()


    if(flow_choice==0):
        try:
            protocol(HOST, int(port),passwd)
        except socket.timeout:
            print("[ERR] socket timeout")
        except socket.error:
            print("[ERR] socket error")
        except Exception as e:
            print(f"[ERR] {e}")
    elif (flow_choice==1):
        bench_mark(protocol)




