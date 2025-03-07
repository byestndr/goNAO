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
        else:
            print("Service already started")
        # Connect to the services
        try:
            self.aas = session.service("ALAudioRecorder")
            self.tts = session.service("ALTextToSpeech")
            print("Connected to ALAudioRecorder and ALTextToSpeech service")
            self.loco = session.service("ALMotion")
            self.pos = session.service("ALRobotPosture")
            self.mem = session.service("ALMemory")
            self.led = session.service("ALLeds")
            print("Connected to the Motion and Posture services")
            self.behave = session.service("ALBehaviorManager")
            self.anim = session.service("ALAnimationPlayer")

        except Exception as e:
            print("Could not connect to service")
            # traceback.print_exc()
            exit(1)
    def startRecord(self, filename, filetype, samplerate, channels):
        self.aas.startMicrophonesRecording(filename, filetype, samplerate, channels)
    def stopRecord(self):
        self.aas.stopMicrophonesRecording()
    def aiThinking(self, started):
        while started.is_set() == True:
            self.led.earLedsSetAngle(90, 0.5, False)
    def speechTalk(self, reply):
        print("Replying")
        self.tts.setLanguage("English")
        self.tts.say(reply)
    def stopTalk(self):
        self.tts.stopAll()
    def walkto(self, x, y, z):
        # Slows down the movement to prevent falls
        xax, yax, zax = x * -0.7, y * -0.7, z * -0.7
        self.loco.moveToward(xax, yax, zax)
    def initMove(self, started):
        if started == 0:
            self.pos.goToPosture("StandInit", 0.5)
            self.loco.wakeUp()
            self.loco.moveInit()
    def stopMove(self):
        self.loco.stopMove()
    def wave(self):
        self.anim.run("animation-a6d9a5/behavior_1")
    def listBehaviors(self):
        print(self.behave.getInstalledBehaviors())


    # Subscribes to robot fallen event and sees if robot falls
    # def ifFallen(fallen):
    #     return True
    # def hasFallen(self):
    #     fall = self.mem.subscriber("robotHasFallen")
    #     fall.signal.connect(self.ifFallen)
    # Attempts to recover robot
    def recover(self):
        self.pos.goToPosture("LyingBack", 0.6)
        self.pos.goToPosture("Sit", 0.6)
        self.pos.goToPosture("StandInit", 0.6)

