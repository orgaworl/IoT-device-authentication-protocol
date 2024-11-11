
import socket
import random
import sys, getopt
from common import supportEC

from protocol_kelapa import Protocol_kelapa_c
from protocol_harmony import Protocol_harmony_c




def bench_mark(protocol,HOST: str, port: int,passwd:str,debug:bool=False,loopTime=3,passwdLen=100):
    import time
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    # get time

    # loop
    
    curve_names=[item["name"] for item in supportEC.curves]
    res_=np.ndarray(shape=(0,3))
    tested_curve_list=[]
    for curve_name in curve_names:
        #time_cost_matrix=[]
        time_cost_matrix=np.ndarray(shape=(0,3))
        print(f"Testing {curve_name}...")
        benchmark_init_time=10
        for testTime in range(benchmark_init_time+loopTime):
            try:
                start_time=time.time()
                phase_time_list=protocol(HOST, int(port),passwd,curve_name,debug)
                end_time=time.time()
                phase_time_list.append((end_time-start_time)*1000)
                if testTime>=benchmark_init_time:
                    time_cost_matrix=np.vstack((time_cost_matrix,phase_time_list))
                time.sleep(0.2)
            except socket.error:
                print("[ERR] socket Error")
            except Exception as e:
                print(f"[ERR] ")

        #print(time_cost_matrix)
        row_len=time_cost_matrix.shape[0]
        try:
            res_=np.vstack((res_,[sum(time_cost_matrix[:,0])/row_len, sum(time_cost_matrix[:,1])/row_len, sum(time_cost_matrix[:,2])/row_len]))
            tested_curve_list.append(curve_name)
        except Exception as e:
            print(f"[ERR] unknow")

    # show
    # plt.plot([i+1 for i in range(len(timeList))],timeList)
    # plt.show()

    # save data
    with open(f"../benchmark/{protocol.__name__}_IoT_device.csv",mode="w",encoding="utf-8") as f:
        df=pd.DataFrame()
        df.insert(loc=len(df.columns),column='curve',value=tested_curve_list)
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
    passwd="passwd"
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
        try:
            protocol(HOST, int(port),passwd,curve_name,debug)
        except socket.timeout:
            print("[ERR] socket timeout")
        except socket.error:
            print("[ERR] socket error")
        except Exception as e:
            print(f"[ERR] {e}")





