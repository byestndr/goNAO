from os import path, remove
from time import sleep
import paramiko
from naoai.ai_autotalk import AutoResponse
from naoai.ai_transcriber import Transcriber

class AutoTalk():
    """ Class for defining the methods to make the robot auto talk """
    def __init__(self, address, api, model):
        self.ip = address.ip
        self.api = api
        self.model = model

    def talkLoop(self):
        while True:
            sleep(60)
            picturePath = self.getPicture()
            self.analyzePic(picturePath)

    def getPicture(self):
        """ Method that takes a picture and transfers it to the computer """
        self.api.takePicture()
        picfile = path.dirname(path.realpath(__file__))+"/frame.jpg"
        # SCPs the file over to the host
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip,22,username='nao',password='nao')
        ssh.open_sftp().get('/home/nao/recordings/camera/frame.jpg', picfile)
        return picfile
    def analyzePic(self, picfile):
        """ This method sends the picture to an AI model and makes the robot say the reply """
        if self.model.usingGemini:
            reply = AutoResponse().geminiImage(picfile, self.model.apiKey)
        else:
            reply = AutoResponse().ollamaImage(picfile, self.model.ollamaModel)

        if path.isfile(picfile) is True:
            remove(picfile)
        Transcriber().tts(reply, self.api)