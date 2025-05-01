print("Initializing modules...")
from requests import post
from re import sub
from .qiapi import qiservice
from sys import exit
from faster_whisper import WhisperModel
from multiprocessing import Process, Queue
# import traceback
from os import path, remove
import paramiko
from ollama import chat, ChatResponse
from time import sleep
from base64 import b64encode

# This connects to the NAO
class connection_details():
    def runFromMainStart(ipadd, portnum, modelname, qistarted, auto, apikey):
        global ip, port, model, qistart
        ip, port, model, qistart = ipadd, portnum, modelname, qistarted
        try:
            # Initialize qi framework.
            global ipaddr, app, start_record
            ipaddr = ip
            start_record = qiservice(ip, port, qistarted)

        except RuntimeError:
            print ("Can't connect to NAO at \"" + ip + "\" at port " + str(port) +".\n"
                   "Please check your script arguments. Run with -h option for help.")
            exit(1)
        if auto == False:
            transcriber().queryingOn()
        elif auto == True:
            while True:
                sleep(60)
                path = autotalk().getPicture()
                autotalk.analyzePic(path, apikey)
            
    
    def runFromMainStop(ipadd, portnum, modelname, qistarted, apikey, sysprompt):
        global ip, port, model
        ip, port, model = ipadd, portnum, modelname
        say = Queue()
        transcriber().queryingOff()
        whisperprocess = Process(target=transcriber().transcribing, args=(modelname, say, apikey, sysprompt))
        whisperprocess.start()
        whisperprocess.join()
        talk = str(say.get())
        transcriber.tts(talk)

# AI response class
class airesponse():
    def gemini(self, prompt, api_key, sysprompt):
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
        return(sub('[*]', " ", response))
    def ollamaImage(self, path):
        
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
                {"text": "Your role is a robotic assistant whose job is to sarcastically in a hilarious matter describe what is happening in this image in one sentenced."}
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
    
class transcriber():
    def queryingOn(self):
        # Checks to see if mics are on
        channels = [0, 0, 1, 0]
        start_record.stopRecord()
        start_record.startRecord("/home/nao/recordings/microphones/request.wav", "wav", 48000, channels)
        print("SPEAK NOW")            
    def queryingOff(self):
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
        if path.isfile(audfile) == True:
            remove(audfile)

        # Make NAO say the response by calling the method corresponding to each model
        if model == "gemini":
            reply = airesponse().gemini(cleanedQuery, apikey, sysprompt)
        else:
            reply = airesponse().ollama(cleanedQuery, model, sysprompt)

        # Puts the reply into the speech queue
        say.put(reply)
        
    def tts(reply):
        try:
            print("Starting talk")
            start_record.speechTalk(reply)
        except RuntimeError as e:
            if e == "Future canceled.":
                print("Stopped talking")

class autotalk():
    def getPicture(self):
        start_record.takePicture()
        picfile = path.dirname(path.realpath(__file__))+"/frame.jpg"
        # SCPs the file over to the host
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ipaddr,22,username='nao',password='nao')
        ssh.open_sftp().get('/home/nao/recordings/camera/frame.jpg', picfile)
        return picfile
    def analyzePic(picfile, apikey):
        if model == "gemini":
            reply = airesponse.geminiImage(picfile, apikey)
        else:
            reply = airesponse().ollamaImage(picfile)
        
        if path.isfile(picfile) == True:
            remove(picfile)
        transcriber.tts(reply)