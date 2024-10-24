
# coding=utf-8
import socket
from protocol_kelapa import Protocol_kelapa_s
from protocol_harmony import Protocol_harmony_s
import sys, getopt

helpMessage='''
Usage:
    python progServer.py --ip <ip> --port <port> --protocol <protocol>  <--debug>

Options:
    --ip <ip>               Specify the IP address. (default "127.0.0.1")
    --port <port>           Specify the port.       (default "4398")
    --protocol <protocol>   Specify the protocol.   (default "kelapa")
    <--debug>               Print protocol parameters.
    

'''

if __name__ == '__main__':
    try:
        argv=sys.argv[1:]
        opts, args = getopt.getopt(argv,"h",["ip=","port=","protocol=","debug"])
    except getopt.GetoptError:
        print(helpMessage)
        sys.exit()
    HOST="127.0.0.1"
    port = 4398
    protocol=Protocol_kelapa_s
    debug=False
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
            debug=True
        else:
            print("invalid argument")
            sys.exit()
    #protocol(HOST, port)
    count=1
    while(1):
        try:
            print(f"-------- waiting for {count}th connection --------")
            protocol(HOST, port,debug)
        except Exception as e:
            print(f"[ERR]{e}")
        count+=1