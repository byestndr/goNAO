import argparse
from sys import exit
from walkingnao import buttonpresses
from walkingnao import walk
from naoai import stoptts
import threading
from configparser import ConfigParser, NoOptionError
from os import path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="IP address for the NAO robot. Cannot be a simulated robot as they are not supported")
    parser.add_argument("--port", type=int, default=9559,
                        help="NAO port")

    exclude_models = parser.add_mutually_exclusive_group(required=False)
    exclude_models.add_argument("--model", help="Choose an AI model for NAO to use. If it is not set, it defaults to the last used model.")
    exclude_models.add_argument("--gemini", action="store_true", help="Sets model to Gemini. Incompatible with --model flag.")

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

# Checks if you are using Ollama
if args.gemini != True and args.model != "":
    import ollama
    response_object = ollama.list()
    model_list = response_object.models

    # Checks if the list is empty or not
    models = []

    if model_list: 
        for model in model_list:
            models.append(model.model)
    else: 
        print("No models found, download some models or use Gemini")
        exit(1)
    
    if args.model not in models:
        print("The model was not found. Make sure it is spelled right and if you've also typed its tag.")
        print(f"Models available: {models}")
        exit(1)

    config.set('Main', 'model', args.model)
    with open(configpath, 'w') as configfile:
        config.write(configfile)
    model = config.get('Main', 'model')
    
elif args.gemini != True and args.model == "":
    model = config.get('Main', 'model')

# Get Gemini API key if it doesn't exist
try:
    if args.gemini == True and path.isfile(configpath) == True:
        api_key = config.get('Main', 'api_key')
    elif args.gemini == True and path.isfile(configpath) == False:
        keysave = input("Set a Gemini API key: ")
        config.set('Main', 'api_key', keysave)
        with open(configpath, 'w') as configfile:
            config.write(configfile)
        api_key = config.get('Main', 'api_key')
        model = "gemini"
    else:
        api_key = "none"
except NoOptionError:
    keysave = input("Set a Gemini API key: ")
    config.set('Main', 'api_key', keysave)
    with open(configpath, 'w') as configfile:
        config.write(configfile)
    api_key = config.get('Main', 'api_key')
    model = "gemini"
    

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
buttonDetector = threading.Thread(target=buttonpresses.joybutton().controllerButtons, args=(args.ip, args.port, model, started, qistart, walkMode))
naoTranscribeOff = threading.Thread(target=buttonpresses.joybutton().OnAiOff, args=(args.ip, args.port, model, started, qistart, api_key, sysprompt))
walker = threading.Thread(target=walk.connection_details.runFromMain, args=(args.ip, args.port, qistart, walkMode, args.auto))

# Starts Processes
try:
    walker.start()
    buttonDetector.start()
    naoTranscribeOff.start()
except KeyboardInterrupt:
    print("Stopping")
    stoptts.connection_details.runFromMain(args.ip, args.port)