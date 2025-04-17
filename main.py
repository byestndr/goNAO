import argparse
from sys import exit
from walkingnao import buttonpresses
from walkingnao import walk
from naoai import stoptts
import threading
from configparser import ConfigParser
from configparser import NoOptionError
from os import path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="IP address for the NAO robot. Cannot be a simulated robot as they are not supported")
    parser.add_argument("--port", type=int, default=9559,
                        help="NAO port")
    parser.add_argument("--model", choices=['gemini', 'deepseek', "gemma"], default="gemma", 
                        help="Choose an AI model for NAO to use")
    parser.add_argument("-s", "--system", action="store_true", help="Set the system prompt to use by the AI")
    parser.add_argument("--auto", "-a", action="store_true", help="Turns on autonomous mode (beta)")
else:
    raise RuntimeError("Script must be run as main")
    exit(1)

args = parser.parse_args()

scriptpath = (path.dirname(path.realpath(__file__)))
configpath = scriptpath + "/config.ini"
config = ConfigParser()
config.read(configpath)

# Get Gemini API key if it doesn't exist
try:
    if args.model == "gemini" and path.isfile(configpath) == True:
        api_key = config.get('Main', 'api_key')
    elif args.model == "gemini" and path.isfile(configpath) == False:
        keysave = input("Set a Gemini API key: ")
        config.set('Main', 'api_key', keysave)
        with open(configpath, 'w') as configfile:
            config.write(configfile)
        api_key = config.get('Main', 'api_key')
    else:
        api_key = "none"
except NoOptionError:
    keysave = input("Set a Gemini API key: ")
    config.set('Main', 'api_key', keysave)
    with open(configpath, 'w') as configfile:
        config.write(configfile)
    api_key = config.get('Main', 'api_key')
    

# System prompt flag
try:   
    if args.system == False and path.isfile(configpath) == True:
        sysprompt = config.get('Main', 'system_prompt')
    elif args.system == True or path.isfile(configpath) == False:
        keysave = input("Set a system prompt: ")
        config.set('Main', 'system_prompt', keysave)
        with open(configpath, 'w') as configfile:
            config.write(configfile)
        sysprompt = config.get('Main', 'system_prompt')
except NoOptionError:
    keysave = input("Set a system prompt: ")
    config.set('Main', 'system_prompt', keysave)
    with open(configpath, 'w') as configfile:
        config.write(configfile)
    sysprompt = config.get('Main', 'system_prompt')


# Sets started variable for the button detector
started = threading.Event()
started.clear()
qistart = threading.Event()
qistart.clear()
walkMode = threading.Event()
walkMode.set()

# Defines processes
buttonDetector = threading.Thread(target=buttonpresses.joybutton().controllerButtons, args=(args.ip, args.port, args.model, started, qistart, walkMode))
naoTranscribeOff = threading.Thread(target=buttonpresses.joybutton().OnAiOff, args=(args.ip, args.port, args.model, started, qistart, api_key, sysprompt))
walker = threading.Thread(target=walk.connection_details.runFromMain, args=(args.ip, args.port, qistart, walkMode))

# Starts Processes
try:
    walker.start()
    buttonDetector.start()
    naoTranscribeOff.start()
except KeyboardInterrupt:
    print("Stopping")
    stoptts.connection_details.runFromMain(args.ip, args.port)