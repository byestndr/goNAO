"""Connect AI to NAO"""

from multiprocessing import Process, Queue
from naoai.ai_transcriber import Transcriber

# TODO: Get Autotalk up and working again


# This connects to the NAO
class ConnectionDetails:
    """Class with methods for connecting to the NAO."""

    def __init__(self, address, api):
        self.ip, self.port = address.ip, address.port

        try:
            # Initialize qi framework.
            self.robot_api = api

        except RuntimeError:
            print(
                "Can't connect to NAO at \"" + self.ip + '" at port ' + str(self.port) + ".\n"
                "Please check your script arguments. Run with -h option for help."
            )
            exit(1)

    def startMicrophone(self, api):
        """Method for starting the AI function"""

        Transcriber().queryingOn(api)

    def startTranscription(self, modelInfo):
        """Method for stopping the AI function"""
        # TODO: Get rid of the queue and multiprocessing process

        say = Queue()
        Transcriber().queryingOff(self.robot_api, self.ip)
        # TODO: Separate AI response and transcription
        whisperprocess = Process(
            target=Transcriber().transcribing, args=(modelname, say, apikey, sysprompt)
        )
        whisperprocess.start()
        whisperprocess.join()
        talk = str(say.get())
        Transcriber().tts(talk, self.robot_api)
