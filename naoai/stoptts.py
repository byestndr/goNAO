from qi import Application
from sys import exit
import argparse

class stoptts():
    def __init__(self, app):
        app.start()
        session = app.session
        # Connect to the services
        try:
            self.tts = session.service("ALTextToSpeech")
            print("Connected to ALTextToSpeech service (Kill speech)")
        except Exception as e:
            print("Could not connect to service")
            # traceback.print_exc()
            exit(1)
    def stopTalk(self):
        self.tts.stopAll()

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

    def runFromMain(ipadd, portnum):
        global ip, port, model, norobot, nomic
        ip, port = ipadd, portnum
        end()

if __name__ == "__main__":
    connection_details.runFromCurrent()

def end():
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + ip + ":" + str(port)
        app = Application(["NAOAI", "--qi-url=" + connection_url])
        stoptalk = stoptts(app)
    except RuntimeError:
        print ("Can't connect to NAO at \"" + ip + "\" at port " + str(port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        exit(1)
    
    stoptalk.stopTalk()