print("Initializing modules...")
from requests import post
from re import sub
from .qiapi import qiservice
from sys import exit
# from whisper import transcribe
from faster_whisper import WhisperModel
from multiprocessing import Process, Queue
# import traceback
from os import path, remove
import paramiko
from ollama import chat, ChatResponse

# This connects to the NAO
class connection_details():
    def runFromMainStart(ipadd, portnum, modelname, qistarted):
        global ip, port, model
        ip, port, model = ipadd, portnum, modelname
        try:
            # Initialize qi framework.
            global ipaddr, app, start_record
            ipaddr = ip
            start_record = qiservice(ip, port, qistarted)

        except RuntimeError:
            print ("Can't connect to NAO at \"" + ip + "\" at port " + str(port) +".\n"
                   "Please check your script arguments. Run with -h option for help.")
            exit(1)
        transcriber().queryingOn()

    def runFromMainStop(ipadd, portnum, modelname, qistarted, apikey, sysprompt):
        global ip, port, model
        ip, port, model = ipadd, portnum, modelname
        say = Queue()
        transcriber().queryingOff()
        whisperprocess = Process(target=transcriber().transcribing, args=(modelname, say, apikey, sysprompt))
        whisperprocess.start()
        whisperprocess.join()
        talk = str(say.get())
        transcriber.tts(talk, qistarted)

# AI response class
class airesponse():
    def gemini(self, prompt, api_key, sysprompt):
        # Sends the data to Gemini
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"
        
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
        
        # Transcribes using whisper
        # print("Transcribing...")
        # whispmodel = load_model("tiny")
        # print("Model loaded")
        # query = whispmodel.transcribe(audfile)
        # cleanedQuery = (query["text"])
        # print("\nWhisper thinks you said: "+cleanedQuery)
        
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
        
    def tts(reply, qistarted):
        try:
            print("Starting talk")
            start_record.speechTalk(reply)
        except RuntimeError as e:
            if e == "Future canceled.":
                print("Stopped talking")

