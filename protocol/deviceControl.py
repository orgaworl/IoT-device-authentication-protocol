
# coding=utf-8
import socket
from protocol_kelapa import Protocol_kelapa_s
from protocol_harmony import Protocol_harmony_s
import sys, getopt
from common import supportEC


helpMessage='''
Usage:
    python progServer.py [options]

Options:
    --ip <ip>               Specify the IP address. (default "127.0.0.1")
    --port <port>           Specify the port.       (default "4398")
    --protocol <protocol>   Specify the protocol.   (default "kelapa")
    <--debug>               Print protocol parameters.
'''

def bench_mark(protocol,HOST: str, port: int,passwd:str,debug:bool=False,loopTime=100,passwdLen=100):
    import time
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    # get time

    # loop
    
    
    res_=np.ndarray(shape=(0,3))
    tested_curve_list=[]
    for curve in supportEC.curves:
        time_cost_matrix=np.ndarray(shape=(0,3))
        print(f"Testing {curve["name"]}...")
        benchmark_init_time=10
        for testTime in range(benchmark_init_time+loopTime):
            try:
                phase_time_list=protocol(HOST, int(port),curve["name"],debug)
                if testTime>=benchmark_init_time:
                    time_cost_matrix=np.vstack((time_cost_matrix,phase_time_list))
                time.sleep(0.8)
            except socket.error:
                print("[ERR] socket Error")
            except Exception as e:
                print(f"[ERR] {e}")

        #print(time_cost_matrix)
        row_len=time_cost_matrix.shape[0]
        try:
            print(res_)
            res_=np.vstack((res_,[sum(time_cost_matrix[:,0])/row_len, sum(time_cost_matrix[:,1])/row_len, sum(time_cost_matrix[:,2])/row_len]))
            tested_curve_list.append(curve)
        except Exception as e:
            print(f"[ERR] unknow")

    # show
    # plt.plot([i+1 for i in range(len(timeList))],timeList)
    # plt.show()

    # save data
    with open(f"../benchmark/{protocol.__name__}_control_device.csv",mode="w",encoding="utf-8") as f:
        df=pd.DataFrame()
        df.insert(loc=len(df.columns),column='curve',value=[curve["name"] for curve in tested_curve_list])
        df.insert(loc=len(df.columns),column='size',value=[curve["size"] for curve in tested_curve_list])
        df.insert(loc=len(df.columns),column='phase1 cost',value=res_[:,0])
        df.insert(loc=len(df.columns),column='phase2 cost',value=res_[:,1])
        df.insert(loc=len(df.columns),column='total cost',value=res_[:,2])
        df.to_csv(f,header=True,index=False,lineterminator='\n')
        f.close()

if __name__ == '__main__':
    # process input parameters
    try:
        argv=sys.argv[1:]
        opts, args = getopt.getopt(argv,"h",["ip=","port=","protocol=","ec=","debug","benchmark"])
    except getopt.GetoptError:
        print(helpMessage)
        sys.exit()

    # default config
    HOST="127.0.0.1"
    port = 4398
    protocol=Protocol_kelapa_s
    debug_flag=False
    benchmark_flag=False
    curve_name="Ed25519"

    # process parameters
    for opt, arg in opts:
        if opt == '-h':
            print(helpMessage)
            sys.exit()
        elif opt in ("--ip"):
            HOST=arg
        elif opt in ("--port"):
            port=int(arg)
        elif opt in ("--protocol"):
            if arg=="harmony":
                protocol=Protocol_harmony_s
            elif arg=="kelapa":
                protocol=Protocol_kelapa_s
            else:
                print("protocol error")
                sys.exit()

        elif opt in ("--debug"):
            debug_flag=True
        elif opt in ("--benchmark"):
            benchmark_flag=True
        elif opt in ("--ec"):
            curve_name=arg
        else:
            print("invalid argument")
            sys.exit()
    
    
    # run protocol
    if (benchmark_flag==True):
        bench_mark(protocol,HOST,port,debug_flag)
    else:
        count=1
        while(1):
            try:
                print(f"-------- waiting for {count}th connection --------")
                protocol(HOST, port,curve_name,debug_flag)
            except Exception as e:
                print(f"[ERR] *")
            count+=1
            break