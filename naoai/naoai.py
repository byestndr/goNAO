"""Connect AI to NAO"""

from multiprocessing import Process, Queue
from goNAO.resource.qiapi import QiService

# TODO: Get Autotalk up and working again

# This connects to the NAO
class ConnectionDetails:
    """Class with methods for connecting to the NAO."""

    def runFromMainStart(ipadd, portnum, modelname, qistarted):
        """Method for starting the AI function"""
        global ip, port, model, qistart
        ip, port, model, qistart = ipadd, portnum, modelname, qistarted
        try:
            # Initialize qi framework.
            global ipaddr, robot_api
            ipaddr = ip
            robot_api = QiService(ip, port, qistarted)

        except RuntimeError:
            print(
                "Can't connect to NAO at \"" + ip + '" at port ' + str(port) + ".\n"
                "Please check your script arguments. Run with -h option for help."
            )
            exit(1)
        Transcriber().queryingOn()

    def startTranscription(ipadd, portnum, modelname, apikey, sysprompt):
        """Method for stopping the AI function"""
        global ip, port, model
        ip, port, model = ipadd, portnum, modelname
        say = Queue()
        Transcriber().queryingOff()
        whisperprocess = Process(
            target=Transcriber().transcribing, args=(modelname, say, apikey, sysprompt)
        )
        whisperprocess.start()
        whisperprocess.join()
        talk = str(say.get())
        Transcriber.tts(talk)


