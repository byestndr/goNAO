import speech_recognition as sr
from requests import post
from re import sub
from re import DOTALL
import qi
import sys
from time import sleep
import argparse
from whisper import load_model
from whisper import transcribe
# import traceback
from os import path
from os import system
from configparser import ConfigParser
from ollama import chat
from ollama import ChatResponse

class audiorecorder():
    def __init__(self, app):
        app.start()
        session = app.session
        # Connect to the services
        try:
            self.aas = session.service("ALAudioRecorder")
            self.tts= session.service("ALTextToSpeech")
            print("Connected to ALAudioRecorder and ALTextToSpeech service")
        except Exception as e:
            print("Could not connect to service")
            # traceback.print_exc()
            sys.exit(1)
    def startRecord(self, filename, filetype, samplerate, channels):
        self.aas.startMicrophonesRecording(filename, filetype, samplerate, channels)
    def stopRecord(self):
        self.aas.stopMicrophonesRecording()
    def speechTalk(self, reply):
        self.tts.setLanguage("English")
        self.tts.say(reply)

    

# This connects to the NAO
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="IP address for the NAO robot. Cannot be a simulated robot as they are not supported")
    parser.add_argument("--port", type=int, default=9559,
                        help="NAO port")
    parser.add_argument("--model", choices=['gemini', 'deepseek', "gemma"], default="gemma", 
                        help="Choose an AI model for NAO to use")
    parser.add_argument("--norobot", "-n", action='store_true', default=False, 
                        help="Runs the script without connecting to the NAO robot")

    args = parser.parse_args()
    if args.norobot == False:
        try:
            # Initialize qi framework.
            connection_url = "tcp://" + args.ip + ":" + str(args.port)
            ipadd = args.ip
            app = qi.Application(["NAOAI", "--qi-url=" + connection_url])
        except RuntimeError:
            print ("Can't connect to NAO at \"" + args.ip + "\" at port " + str(args.port) +".\n"
                   "Please check your script arguments. Run with -h option for help.")
            sys.exit(1)



# AI response class
class airesponse():
    def gemini(self, prompt):
        if args.model == "gemini":
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
                        {"text": "You are a robot named 'nao' responding to a human in a conversation"}
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
    def ollamaresponse(self, prompt):
        if args.model == "deepseek":
            model = 'deepseek-r1:1.5b'
        else:
            model = 'naoGemma'
        
        response: ChatResponse = chat(model=model, messages=[
          {
            'role': 'user',
            'content': prompt,
          },
        ])
        
        if args.model == "deepseek":
            response = response['message']['content']
            nothink = sub(r"<think>.*?</think>\n?", "", response, flags=DOTALL) 
            print(nothink)
            return(nothink)
        else:
            response = response['message']['content']
            print(sub('[*]', " ", response))
            return(sub('[*]', " ", response))

# Checks if the no robot flag is on and runs depending on if it is
if args.norobot == False:
    try: 
        # Loops the querying and responds
        while True:
            start_record = audiorecorder(app)
            channels = [0, 0, 1, 0]
            start_record.stopRecord()
            start_record.startRecord("/home/nao/recordings/microphones/request.wav", "wav", 48000, channels)
            sleep(3)
            start_record.stopRecord()
            audfile = path.dirname(path.realpath(__file__))+"/request.wav"
            # SCPs the file over to the host
            sshcom = f"nao@{ipadd}:/home/nao/recordings/microphones/request.wav {audfile}"    
            system("sshpass -p 'nao' scp -o StrictHostKeyChecking=no "+sshcom) 
            
            # Transcribes using whisper
            model = whisper.load_model("tiny")
            prompt = model.transcribe(audfile)
            print(prompt["text"])
            
            ## If you want to use sphinx, uncomment this and comment out the openai code
            # audfile = path.dirname(path.realpath(__file__))+"/request.wav"
            # sp = sr.Recognizer()
            # with sr.AudioFile(audfile) as sourceaud:
            #         audio = sp.record(sourceaud)
            # # Transcribes
            # try:
            #     prompt = sp.recognize_sphinx(audio)
            #     print(prompt)
            # except sr.UnknownValueError:
            #     print("Sphinx could not understand audio")
            # except sr.RequestError as e:
            #     print("Sphinx error; {0}".format(e))

            

            # Make NAO say the response by calling the method corresponding to each model
            start_record.speechTalk(airesponse(prompt))
            sleep(1)


    except KeyboardInterrupt:
        print("Exiting the program")
        sleep(1)
        print("Stopping current recordings")
        start_record.stopRecord()
        print("Stopped")
        sys.exit()
else:
    airesponse().ollamaresponse(input("Enter the prompt: "))