""" Connect AI to NAO """
from time import sleep
from sys import exit
from os import path, remove
from multiprocessing import Process, Queue
from re import sub
from base64 import b64encode
from requests import post
import paramiko
from faster_whisper import WhisperModel
from ollama import chat, ChatResponse
from goNAO.naoai.qiapi import QiService
# import traceback

# This connects to the NAO
class ConnectionDetails():
    """ Class with methods for connecting to the NAO. """
    def runFromMainStart(ipadd, portnum, modelname, qistarted, auto, apikey):
        """ Method for starting the AI function """
        global ip, port, model, qistart
        ip, port, model, qistart = ipadd, portnum, modelname, qistarted
        try:
            # Initialize qi framework.
            global ipaddr, app, start_record
            ipaddr = ip
            start_record = QiService(ip, port, qistarted)

        except RuntimeError:
            print ("Can't connect to NAO at \"" + ip + "\" at port " + str(port) +".\n"
                   "Please check your script arguments. Run with -h option for help.")
            exit(1)
        if auto is False:
            Transcriber().queryingOn()
        elif auto is True:
            while True:
                sleep(60)
                path = AutoTalk().getPicture()
                AutoTalk.analyzePic(path, apikey)

    def runFromMainStop(ipadd, portnum, modelname, qistarted, apikey, sysprompt):
        """ Method for stopping the AI function"""
        global ip, port, model
        ip, port, model = ipadd, portnum, modelname
        say = Queue()
        Transcriber().queryingOff()
        whisperprocess = Process(target=Transcriber().transcribing, args=(modelname, say, apikey, sysprompt))
        whisperprocess.start()
        whisperprocess.join()
        talk = str(say.get())
        Transcriber.tts(talk)

# AI response class
class AiResponse():
    """ Class defining methods for different AI model responses """
    def gemini(self, prompt, api_key, sysprompt):
        """ Module for communicating with Gemini and getting responses. Needs an API key. """
        # Sends the data to Gemini
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={api_key}"

        data = {
            "system_instruction": {
                "parts": 
                    {"text": sysprompt}
            },
            "contents": [{
            "parts":[{"text": prompt}]
            }],
            "safetySettings": [
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
            ],
           }

        response = post(url, headers={'Content-Type': 'application/json'}, json=data)
        # This is a debugging thingy
        # print(response)
        # This prints the result from Gemini
        # It converts the json into actual text and then regex's all the * out
        x = response.json()
        content = (x["candidates"][0]["content"]["parts"][0]["text"]) 
        print(sub('[*]', " ", content))
        return content
    def ollama(self, prompt, model, sysprompt):
        """ Module for interfacing with local Ollama and getting responses. """
        response: ChatResponse = chat(model=model, messages=[
          {
            'role': 'system',
            'content': sysprompt,  
          },
          {
            'role': 'user',
            'content': prompt,
          },
        ])

        response = response['message']['content']
        print(sub('[*]', " ", response))
        return sub('[*]', " ", response)
    def ollamaImage(self, path):
        """ Module for sending images to Ollama and getting responses. """
        with open(path, "rb") as image_file:
            image = b64encode(image_file.read()).decode('utf-8')

        response = chat(
          model=model,
          messages=[
            {
              'role': 'user',
              'content': 'Your role is a robotic assistant whose job is to sarcastically in a hilarious matter describe what is happening in this image in one sentence.',
              'images': [image],
            }
          ],
        )

        reply = response['message']['content']
        return reply

    def geminiImage(path, api_key):
        """ Module for sending images to Gemini and getting a response. An API key is needed. """
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={api_key}"
        with open(path, "rb") as image_file:
            image = b64encode(image_file.read()).decode('utf-8')


        data = {
            "contents": [{
            "parts":[
                {
                  "inline_data": {
                    "mime_type":"image/jpeg",
                    "data": image
                  }
                },
                {"text": "Your role is a robotic assistant whose job is to sarcastically in a hilarious matter describe what is happening in this image in one sentence."}
                ]
            }],
            "safetySettings": [
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
            ],
           }

        response = post(url, headers={'Content-Type': 'application/json'}, json=data)
        # This prints the result from Gemini
        # It converts the json into actual text and then regex's all the * out
        x = response.json()
        content = (x["candidates"][0]["content"]["parts"][0]["text"]) 
        print(sub('[*]', " ", content))
        return content

class Transcriber():
    """ Transcribes audio and turns it into text. Also carries the text-to-speech method. """
    def queryingOn(self):
        """ Turns on the microphones and defines where to save the audio file. """
        channels = [0, 0, 1, 0]
        start_record.stopRecord()
        start_record.startRecord("/home/nao/recordings/microphones/request.wav", "wav", 48000, channels)
        print("SPEAK NOW")            
    def queryingOff(self):
        """ Turns off the microphone and transfers the file over to the computer """
        start_record.stopRecord()
        global audfile
        audfile = path.dirname(path.realpath(__file__))+"/request.wav"
        print(audfile)
        # SCPs the file over to the host
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ipaddr,22,username='nao',password='nao')
        ssh.open_sftp().get('/home/nao/recordings/microphones/request.wav', audfile)

    def transcribing(self, model, say, apikey, sysprompt):
        """ 
        Transcribes the audio file to text and plugs the 
        transcript into the AI model. Then it puts the reply in the queue
        """
        # Sets model size
        model_size = "tiny.en"

        # Transcribes using faster whisper
        whispmodel = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
        segments, info = whispmodel.transcribe(str(audfile))

        segments = list(segments)
        for segment in segments:
            print(segment.text)
            cleanedQuery = segment.text

        # Deletes audio request
        if path.isfile(audfile) is True:
            remove(audfile)

        # Make NAO say the response by calling the method corresponding to each model
        if model == "gemini":
            reply = AiResponse().gemini(cleanedQuery, apikey, sysprompt)
        else:
            reply = AiResponse().ollama(cleanedQuery, model, sysprompt)

        # Puts the reply into the speech queue
        say.put(reply)

    def tts(reply):
        """ Makes the robot say whatever is in the reply parameter """
        try:
            print("Starting talk")
            start_record.speechTalk(reply)
        except RuntimeError as e:
            if e == "Future canceled.":
                print("Stopped talking")

class AutoTalk():
    """ Class for defining the methods to make the robot auto talk """
    def getPicture(self):
        """ Method that takes a picture and transfers it to the computer """
        start_record.takePicture()
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
