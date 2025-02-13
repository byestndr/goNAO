import argparse
import sys
from walkingnao import buttonpresses
from walkingnao import walk
from naoai import stoptts
import multiprocessing

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="IP address for the NAO robot. Cannot be a simulated robot as they are not supported")
    parser.add_argument("--port", type=int, default=9559,
                        help="NAO port")
    parser.add_argument("--model", choices=['gemini', 'deepseek', "gemma"], default="gemma", 
                        help="Choose an AI model for NAO to use")
    excluded = parser.add_mutually_exclusive_group(required=False)
else:
    raise RuntimeError("Script must be run as main")
    sys.exit(1)


args = parser.parse_args()

# Defines processes
walk.connection_details.runFromMain(args.ip, args.port)

buttonDetector = multiprocessing.Process(target=buttonpresses.controllerButtons, args=(args.ip, args.port, args.model))
naoTranscribeOff = multiprocessing.Process(target=buttonpresses.OnAiOff, args=(args.ip, args.port, args.model))
walker = multiprocessing.Process(target=walk.controllerWalk)

# Starts Processes
try:
    buttonDetector.start()
    naoTranscribeOff.start()
    walker.start()
except KeyboardInterrupt:
    stoptts.connection_details(args.ip, args.port)
    stoptts.end()