
# coding=utf-8
import socket
from protocol_kelapa import Protocol_kelapa_s
from protocol_harmony import Protocol_harmony_s
import sys, getopt

helpMessage='''
Usage:
    python progServer.py [options]

Options:
    --ip <ip>               Specify the IP address. (default "127.0.0.1")
    --port <port>           Specify the port.       (default "4398")
    --protocol <protocol>   Specify the protocol.   (default "kelapa")
    <--debug>               Print protocol parameters.
    

'''

if __name__ == '__main__':
    # process input parameters
    try:
        argv=sys.argv[1:]
        opts, args = getopt.getopt(argv,"h",["ip=","port=","protocol=","ec=","debug","bms"])
    except getopt.GetoptError:
        print(helpMessage)
        sys.exit()

    # default config
    HOST="127.0.0.1"
    port = 4398
    protocol=Protocol_kelapa_s
    debug_flag=False
    bms_flag=False
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
        elif opt in ("--bms"):
            bms_flag=True
        elif opt in ("--ec"):
            curve_name=arg
        else:
            print("invalid argument")
            sys.exit()
    
    
    # run protocol
    count=1
    while(1):
        try:
            print(f"-------- waiting for {count}th connection --------")
            protocol(HOST, port,curve_name,debug_flag,bms_flag)
        except Exception as e:
            print(f"[ERR]{e}")
        count+=1