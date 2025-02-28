from qi import Application
import threading

class qiservice():
    def __init__(self, ip, port, started):
        if started.is_set() == False:
            global app, session
            connection_url = "tcp://" + ip + ":" + str(port)
            app = Application(["goNAO", "--qi-url=" + connection_url])

            app.start()
            session = app.session
            started.set()
        # Connect to the services
        try:
            self.aas = session.service("ALAudioRecorder")
            self.tts = session.service("ALTextToSpeech")
            print("Connected to ALAudioRecorder and ALTextToSpeech service")
            self.loco = session.service("ALMotion")
            self.pos = session.service("ALRobotPosture")
            self.mem = session.service("ALMemory")
            print("Connected to the Motion and Posture services")
        except Exception as e:
            print("Could not connect to service")
            # traceback.print_exc()
            exit(1)
    def startRecord(self, filename, filetype, samplerate, channels):
        self.aas.startMicrophonesRecording(filename, filetype, samplerate, channels)
    def stopRecord(self):
        self.aas.stopMicrophonesRecording()
    def speechTalk(self, reply):
        self.tts.setLanguage("English")
        self.tts.say(reply)
    def stopTalk(self):
        self.tts.stopAll()
    def walkto(self, x, y, z):
        # Slows down the movement to prevent falls
        xax, yax, zax = x * -0.9, y * -0.9, z * -0.9
        self.loco.moveToward(xax, yax, zax)
    def initMove(self, started):
        if started == 0:
            self.pos.goToPosture("StandInit", 0.5)
            self.loco.wakeUp()
            self.loco.moveInit()
    def stopMove(self):
        self.loco.stopMove()
    # Subscribes to robot fallen event and sees if robot falls
    def hasFallen(self):
        if self.mem.subscriber("robotHasFallen") == True:
            return True
    # Attempts to recover robot
    def recover(self):
        self.pos.goToPosture("LyingBack", 0.6)
        self.pos.goToPosture("Sit", 0.6)
        self.pos.goToPosture("StandInit", 0.6)

