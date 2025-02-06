import qi
from sys import exit

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