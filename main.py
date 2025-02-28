import argparse
from sys import exit
from walkingnao import buttonpresses
from walkingnao import walk
from naoai import stoptts
import threading

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="IP address for the NAO robot. Cannot be a simulated robot as they are not supported")
    parser.add_argument("--port", type=int, default=9559,
                        help="NAO port")
    parser.add_argument("--model", choices=['gemini', 'deepseek', "gemma"], default="gemma", 
                        help="Choose an AI model for NAO to use")
else:
    raise RuntimeError("Script must be run as main")
    exit(1)

args = parser.parse_args()

# Sets started variable for the button detector
started = threading.Event()
started.clear()
qistart = threading.Event()
qistart.clear()

# Defines processes
buttonDetector = threading.Thread(target=buttonpresses.joybutton().controllerButtons, args=(args.ip, args.port, args.model, started, qistart))
naoTranscribeOff = threading.Thread(target=buttonpresses.joybutton().OnAiOff, args=(args.ip, args.port, args.model, started, qistart))
walker = threading.Thread(target=walk.connection_details.runFromMain, args=(args.ip, args.port, qistart))

# Starts Processes
try:
    walker.start()
    buttonDetector.start()
    naoTranscribeOff.start()
except KeyboardInterrupt:
    stoptts.connection_details.runFromMain(args.ip, args.port)