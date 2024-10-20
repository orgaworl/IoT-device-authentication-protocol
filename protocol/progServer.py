
# coding=utf-8
import socket
from protocol_kelapa import Protocol_kelapa_s
from protocol_harmony import Protocol_harmony_s
import sys, getopt



if __name__ == '__main__':
    try:
        argv=sys.argv[1:]
        opts, args = getopt.getopt(argv,"h",["ip=","port=","protocol="])
    except getopt.GetoptError:
        print('progServer.py --ip <ip> --port <port>')
    HOST="127.0.0.1"
    port = 4398
    protocol=Protocol_kelapa_s
    for opt, arg in opts:
        if opt == '-h':
            print("progServer.py --ip <ip> --port <port>")
            sys.exit()
        elif opt in ("--ip"):
            HOST=arg
        elif opt in ("--port"):
            port=arg
        elif opt in ("--protocol"):
            if arg=="harmony":
                protocol=Protocol_harmony_s
            elif arg=="kelapa":
                protocol=Protocol_kelapa_s
            else:
                print("protocol error")
                sys.exit()
        else:
            print("invalid argument")
            sys.exit()
    #protocol(HOST, port)
    count=1
    while(1):
        try:
            print(f"-------- {count} --------")
            print(protocol)
            protocol(HOST, port)
        except Exception as e:
            print(f"[ERR]{e}")
        count+=1