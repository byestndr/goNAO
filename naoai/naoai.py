print("Initializing modules...")
from requests import post
from re import sub
from re import DOTALL
from .qiapi import qiservice
from qi import Application
from sys import exit
from time import sleep
import argparse
from whisper import load_model
from whisper import transcribe
from multiprocessing import Process
# import traceback
from os import path
from os import system
import paramiko
from configparser import ConfigParser
from ollama import chat
from ollama import ChatResponse

# This connects to the NAO
class connection_details():
    def runFromCurrent():
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", type=str, default="127.0.0.1",
                            help="IP address for the NAO robot. Cannot be a simulated robot as they are not supported")
        parser.add_argument("--port", type=int, default=9559,
                            help="NAO port")
        parser.add_argument("--model", choices=['gemini', 'deepseek', "gemma"], default="gemma", 
                            help="Choose an AI model for NAO to use")
        excluded = parser.add_mutually_exclusive_group(required=False)
        excluded.add_argument("--norobot", "-n", action='store_true', default=False, 
                            help="Runs the script without connecting to the NAO robot")
        excluded.add_argument("--nomic", "-m", action='store_true', default=False,
                            help="Allows you to prompt the AI and for NAO to speak the response without the use of microphones")
        global ip, port, model, norobot, nomic
        args = parser.parse_args()
        ip, port, model, norobot, nomic = args.ip, args.port, args.model, args.norobot, args.nomic

    def runFromMainStart(ipadd, portnum, modelname, qistarted):
        global ip, port, model, norobot, nomic
        ip, port, model, norobot, nomic = ipadd, portnum, modelname, False, False
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

    def runFromMainStop(ipadd, portnum, modelname):
        global ip, port, model, norobot, nomic
        ip, port, model, norobot, nomic = ipadd, portnum, modelname, False, False
        transcriber().queryingOff()
        whisperprocess = Process(target=transcriber().transcribing(), args=(model))
        whisperprocess.start()
        whisperprocess.join()

if __name__ == "__main__":
    connection_details.runFromCurrent()

if __name__ == "__main__" and norobot == False:
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + ip + ":" + str(port)
        ipaddr = ip
        app = Application(["NAOAI", "--qi-url=" + connection_url])
        start_record = qiservice(app)
    except RuntimeError:
        print ("Can't connect to NAO at \"" + ip + "\" at port " + str(port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        exit(1)

# AI response class
class airesponse():
    def gemini(self, prompt):
        # Sets config variables
        scriptpath = (path.dirname(path.realpath(__file__)))
        configpath = scriptpath + "/config.ini"
        config = ConfigParser()
        # Get Gemini API key if it doesn't exist
        if path.isfile(configpath) == True:
            config.read(configpath)
            api_key = config.get('Main', 'api_key')
        else:
            keysave = input("Set a Gemini API key: ")
            config['Main'] = {'api_key': keysave}
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            api_key = config.get('Main', 'api_key')
        # Sends the data to Gemini
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"
        data = {
            "system_instruction": {
                "parts": 
                    {"text": "You are a robot named 'TJ' responding to a human in a conversation. Answer in 1-2 sentences. You'll also need to be opinionated."}
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
    def ollama(self, prompt):
        if model == "deepseek":
            model = 'deepseek-r1:1.5b'
        else:
            model = 'naoGemma'
        
        response: ChatResponse = chat(model=model, messages=[
          {
            'role': 'user',
            'content': prompt,
          },
        ])
        
        if model == "deepseek":
            response = response['message']['content']
            nothink = sub(r"<think>.*?</think>\n?", "", response, flags=DOTALL) 
            print(nothink)
            return(nothink)
        else:
            response = response['message']['content']
            print(sub('[*]', " ", response))
            return(sub('[*]', " ", response))

class transcriber():
    def queryingOn(self):
        # Checks to see if mics are on
        global query
        if nomic == True:
            query = input("Enter the query: ")
        else:
            query = ""

        if query == "": 
            channels = [0, 0, 1, 0]
            start_record.stopRecord()
            start_record.startRecord("/home/nao/recordings/microphones/request.wav", "wav", 48000, channels)
            print("SPEAK NOW")            
    def queryingOff(self):
        if query == "":
            start_record.stopRecord()
            global audfile
            audfile = path.dirname(path.realpath(__file__))+"/request.wav"
            print(audfile)
            # SCPs the file over to the host
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ipaddr,22,username='nao',password='nao')
            ssh.open_sftp().get('/home/nao/recordings/microphones/request.wav', audfile)
            
    def transcribing(self, model):
        # Transcribes using whisper
        if nomic == False:
            print("Transcribing...")
            whispmodel = load_model("tiny")
            print("Model loaded")
            query = whispmodel.transcribe(audfile)
            cleanedQuery = (query["text"])
            print("\nWhisper thinks you said: "+cleanedQuery)
        else:
            cleanedQuery = query

        # Make NAO say the response by calling the method corresponding to each model
        if model == "deepseek" or model == "gemma":
            reply = airesponse().ollama(cleanedQuery)
        else:
            reply = airesponse().gemini(cleanedQuery)

        # Creates talking process
        start_record.speechTalk(reply)

# Checks if the no robot flag is on and runs depending on if it is
if __name__ == "__main__" and norobot == False:
    while 1:
        try: 
        # Loops the querying and responds
            transcriber.queryingOn()
            sleep(5)
            transcriber.queryingOff()
            transcriber.transcribing()
        except KeyboardInterrupt:
            print("Exiting the program")
            sleep(1)
            print("Stopping current recordings")
            start_record.stopRecord()
            print("Stopped")
            exit()
            
# If the no robot flag is on, run this
if __name__ == "__main__" and model == "gemini":
    airesponse().gemini(input("Enter the prompt: "))
elif __name__ == "__main__" and model == "deepseek":
    airesponse().ollama(input("Enter the prompt: "))
elif __name__ == "__main__" and model == "gemma":
    airesponse().ollama(input("Enter the prompt: "))
else:
    pass
