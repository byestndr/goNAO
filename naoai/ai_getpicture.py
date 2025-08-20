from os import path, remove
import paramiko
from faster_whisper import WhisperModel
from goNAO.resource.qiapi import QiService

class AutoTalk():
    """ Class for defining the methods to make the robot auto talk """
    def getPicture(self):
        """ Method that takes a picture and transfers it to the computer """
        robot_api.takePicture()
        picfile = path.dirname(path.realpath(__file__))+"/frame.jpg"
        # SCPs the file over to the host
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ipaddr,22,username='nao',password='nao')
        ssh.open_sftp().get('/home/nao/recordings/camera/frame.jpg', picfile)
        return picfile
    def analyzePic(picfile, apikey):
        """ This method sends the picture to an AI model and makes the robot say the reply """
        if model == "gemini":
            reply = AiResponse.geminiImage(picfile, apikey)
        else:
            reply = AiResponse().ollamaImage(picfile)

        if path.isfile(picfile) is True:
            remove(picfile)
        Transcriber.tts(reply)