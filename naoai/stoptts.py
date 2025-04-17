import sys
sys.path.append('../goNAO')
from .qiapi import qiservice
from qi import Application
import argparse
from sys import exit

class connection_details():
    def runFromCurrent():
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", type=str, default="127.0.0.1",
                            help="IP address for the NAO robot. Cannot be a simulated robot as they are not supported")
        parser.add_argument("--port", type=int, default=9559,
                            help="NAO port")
        global ip, port
        args = parser.parse_args()
        ip, port = args.ip, args.port

    def runFromMain(ipadd, portnum, qistarted):
        end(ipadd, portnum, qistarted)

if __name__ == "__main__":
    connection_details.runFromCurrent()

def end(ip, port, qistarted):
    try:
        # Initialize qi framework.
        stoptalk = qiservice(ip, port, qistarted)
    except RuntimeError:
        print ("Can't connect to NAO at \"" + ip + "\" at port " + str(port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        exit(1)
    
    stoptalk.stopTalk()