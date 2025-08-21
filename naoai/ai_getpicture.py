from os import path, remove
import paramiko
from goNAO.naoai.ai_autotalk import AutoResponse
from goNAO.naoai.ai_transcriber import Transcriber

class AutoTalk():
    """ Class for defining the methods to make the robot auto talk """
    def __init__(self, api):
        self.api = api

    def getPicture(self, ip):
        """ Method that takes a picture and transfers it to the computer """
        self.api.takePicture()
        picfile = path.dirname(path.realpath(__file__))+"/frame.jpg"
        # SCPs the file over to the host
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username='nao',password='nao')
        ssh.open_sftp().get('/home/nao/recordings/camera/frame.jpg', picfile)
        return picfile
    def analyzePic(self, picfile, apikey, model):
        """ This method sends the picture to an AI model and makes the robot say the reply """
        if model == "gemini":
            reply = AutoResponse().geminiImage(picfile, apikey)
        else:
            reply = AutoResponse().ollamaImage(picfile)

        if path.isfile(picfile) is True:
            remove(picfile)
        Transcriber().tts(reply, self.api)