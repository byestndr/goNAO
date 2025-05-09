import sys
from goNAO.naoai.qiapi import QiService
sys.path.append('../goNAO')

class ConnectionDetails():
    def runFromMain(self, ipadd, portnum, qistarted):
        """ Stop talking """
        end(ipadd, portnum, qistarted)

def end(ip, port, qistarted):
    """ Connect to the NAO and stop it from talking """
    try:
        # Initialize qi framework.
        stoptalk = QiService(ip, port, qistarted)
    except RuntimeError:
        print ("Can't connect to NAO at \"" + ip + "\" at port " + str(port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        exit(1)
    stoptalk.stopTalk()
