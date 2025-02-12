import argparse
import sys
import naoai
import walkingnao


if __name__ == "__main__":
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
else:
    raise RuntimeError("Script must be run as main")
    sys.exit(1)

args = parser.parse_args()