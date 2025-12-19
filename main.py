import argparse
import threading
from concurrent.futures import ProcessPoolExecutor
from sys import exit, stdout
from os import path
from time import sleep
from resource.config import Configuration as config
import resource.qiapi as qiapi
import walkingnao.walk as walk
import walkingnao.autowalk as autowalk
import walkingnao.buttonpresses as buttonpresses
import naoai.ai_getpicture as ai_getpicture

class RobotAddress:
    def __init__(self, ipaddress, robotport):
        self.ip = ipaddress
        self.port = robotport

class AiInfo:
    def __init__(self, model, isGemini, sysPrompt, geminiKey=None):
        self.ollamaModel = model
        self.usingGemini = isGemini
        self.systemPrompt = sysPrompt
        self.apiKey = geminiKey


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="IP address for the NAO robot. Cannot be a simulated robot as they are not supported")
    parser.add_argument("--port", type=int, default=9559,
                        help="NAO port (Defaults to port 9559)")

    exclude_models = parser.add_mutually_exclusive_group(required=False)
    exclude_models.add_argument("--model", help="Choose an AI model for NAO to use. If it is not set, it defaults to the last used model.")
    exclude_models.add_argument("--gemini", action="store_true", help="Sets model to Gemini. Incompatible with --model flag.")

    parser.add_argument("-s", "--system", action="store_true", help="Set the system prompt to use by the AI")
    parser.add_argument("--auto", "-a", action="store_true", help="Turns on autonomous mode (beta)")
else:
    raise RuntimeError("Script must be run as main")
    exit(1)

args = parser.parse_args()

api_key = None
if args.gemini is False:
    model = config().modelType(args.model)
    api_key = None
elif args.gemini is True:
    model = "gemini"
    api_key = config().geminiApiKey()

robotInfo = RobotAddress(args.ip, args.port)
aiInfo = AiInfo(args.model, args.gemini, args.system, api_key)

sysprompt = config().systemPrompt(args.system)

# Sets started variable for the button detector
started = threading.Event()
started.clear()
qistart = threading.Event()
qistart.clear()
walkMode = threading.Event()
walkMode.set()


class RobotAPI:
    hasQiStarted = qistart
    apiService = qiapi.QiService(robotInfo, hasQiStarted)

NaoAPI = RobotAPI.apiService

if args.auto is True:
    autotalk = threading.Thread(target=ai_getpicture.AutoTalk(robotInfo, NaoAPI, aiInfo).talkLoop)
    walker = threading.Thread(target=autowalk.ConnectionDetails().runFromMain, args=(NaoAPI, ))
else:
    buttonDetector = threading.Thread(target=buttonpresses.JoyButton().controllerButtons, args=(robotInfo, NaoAPI, started, walkMode))
    naoTranscribeOff = threading.Thread(target=buttonpresses.JoyButton().onAiOff, args=(robotInfo, NaoAPI, aiInfo, started))
    walker = threading.Thread(target=walk.ConnectionDetails().startWalk, args=(NaoAPI, walkMode))

current_directory = path.dirname(path.realpath(__file__))

if not path.isdir(f'{current_directory}/tiny.en'):
    stdout.write("Downloading transcription model")
    stdout.flush()
    from faster_whisper import download_model
    download_model("tiny.en", "tiny.en")
    stdout.write('\b')
    stdout.write('Downloaded transcription model')
    stdout.flush()


# Starts Processes
try:
    walker.start()
    if args.auto is False:
        buttonDetector.start()
        naoTranscribeOff.start()
    elif args.auto is True:
        sleep(5)
        autotalk.start()
except KeyboardInterrupt:
    if args.auto is True:
        print("Stopping sonars")
        NaoAPI.stopSonar()
    exit(0)
