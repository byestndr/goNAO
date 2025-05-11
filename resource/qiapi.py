""" Module for interfacing with NAO's sensors and ordering actions """

from qi import Application

class QiService():
    """
    This class defines all of the qi services and actions.
    """
    def __init__(self, ip, port, started):
        if started.is_set() is False:
            try:
                global app, session
                connection_url = "tcp://" + ip + ":" + str(port)
                app = Application(["goNAO", "--qi-url=" + connection_url])

                app.start()
                session = app.session
                started.set()
            except RuntimeError:
                print("Could not connect to NAO, please check the ip and port.")
                exit(1)
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
            self.sonar = session.service("ALSonar")
            self.pic = session.service("ALPhotoCapture")
            self.face = session.service("ALFaceDetection")
            self.face.subscribe("Test_Face", 500, 0.0 )

        except RuntimeError:
            print("Could not connect to service")
            # traceback.print_exc()
            exit(1)

    def startRecord(self, filename, filetype, samplerate, channels):
        """
        Turns on the microphone and sets the file location and other audio info. 
        """
        self.aas.startMicrophonesRecording(filename, filetype, samplerate, channels)
    def stopRecord(self):
        """ Turn off the microphone """
        self.aas.stopMicrophonesRecording()
    def aiThinking(self, started):
        """ Turns on the ear LEDs """
        while started.is_set() is True:
            self.led.earLedsSetAngle(90, 0.5, False)
    def speechTalk(self, reply):
        """ Make the robot say whatever is passed to the reply parameter """
        print("Replying")
        self.tts.setLanguage("English")
        self.tts.say(reply)
    def stopTalk(self):
        """ Immediately make the robot stop talking"""
        self.tts.stopAll()
    def walkto(self, x, y, z):
        """ 
        Make the robot walk. X value corresponds to left and right movement, 
        Y corresponds to forwards and backwards, and Z is rotation. X, Y, and 
        Z are a value of how fast you want your robot to go along that axis.
        """
        # Slows down the movement to prevent falls
        xax, yax, zax = x * -0.7, y * -0.7, z * -0.7
        self.loco.moveToward(xax, yax, zax)
    def initMove(self, started):
        """ If it hasn't already, the robot will get ready to move. """
        if started == 0:
            self.pos.goToPosture("StandInit", 0.5)
            self.loco.wakeUp()
            self.loco.moveInit()
    def stopMove(self):
        """ Stops any current movement. """
        self.loco.stopMove()
    def wave(self):
        """ Wave if the behavior is installed. """
        self.anim.run("animation-a6d9a5/behavior_1")
    def listBehaviors(self):
        """ List all installed behaviors """
        print(self.behave.getInstalledBehaviors())
    def moveHead(self, x, y):
        """ Move the robot's head. X is left and right, Y is up and down. """
        if y == 0 and x > 0:
            joystick = x

            self.loco.setStiffnesses("Head", 1.0)
            self.loco.changeAngles("HeadYaw", -0.3, joystick)
            #print(self.loco.getTaskList())
        elif y == 0 and x < 0:
            joystick = abs(x)
            self.loco.setStiffnesses("Head", 1.0)
            self.loco.changeAngles("HeadYaw", 0.3, joystick)
        elif y > 0 and x == 0:
            joystick = y
            self.loco.setStiffnesses("Head", 1.0)
            self.loco.changeAngles("HeadPitch", 0.3, joystick)
        elif y < 0 and x == 0:
            joystick = abs(y)
            self.loco.setStiffnesses("Head", 1.0)
            self.loco.changeAngles("HeadPitch", -0.3, joystick)
    def initSonar(self):
        """ Subscribe to the sonars and turn it on """
        self.sonar.subscribe("autowalk")
    def sonarLeft(self):
        """ Returns the value of the left sonar """
        return self.mem.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    def sonarRight(self):
        """ Returns the value of the right sonar """
        return self.mem.getData("Device/SubDeviceList/US/Right/Sensor/Value")
    def takePicture(self):
        """ Take a picture and save it to the NAO """
        self.pic.setResolution(4)
        self.pic.setColorSpace(13)
        self.pic.setPictureFormat("jpg")
        self.pic.takePicture("/home/nao/recordings/camera", "frame")
    def stopSonar(self):
        """ Unsubscribes from the sonars and turns it off """
        self.sonar.unsubscribe("autowalk")
    def faceDetection(self):
        """ Returns the face detected value """
        return self.mem.getData("FaceDetected", 0)
    def fallDetection(self):
        """ Returns the status of whether the robot is supported by its feet """
        return self.mem.getData("ALMotion/RobotIsStand")
    # Attempts to recover robot
    def recover(self):
        """ Makes the robot go the stand postion """
        self.pos.goToPosture("StandInit", 0.6)
