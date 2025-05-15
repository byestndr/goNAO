# goNAO!
Make your NAO to walk and talk!

## Setup
Use any Python version 3.7 - 3.11 as libqi bindings are only available for those versions. This project has only been tested on Python 3.11.
Make sure that dependencies from [requirements.txt](https://github.com/byestndr/goNAO/blob/main/requirements.txt) are installed.

## Usage
To use, clone this repo and run the main python file with the IP address of the NAO and the AI model you want to use.
```
usage: main.py [-h] [--ip IP] [--port PORT] [--model MODEL | --gemini] [-s] [--auto]

options:
  -h, --help     show this help message and exit
  --ip IP        IP address for the NAO robot. Cannot be a simulated robot as they are not supported
  --port PORT    NAO port (Defaults to port 9559)
  --model MODEL  Choose an AI model for NAO to use. If it is not set, it defaults to the last used model.
  --gemini       Sets model to Gemini. Incompatible with --model flag.
  -s, --system   Set the system prompt to use by the AI
  --auto, -a     Turns on autonomous mode (beta)
  ```

## What have I done?

What I have done to NAO is make it fun to control and talk to as well as improve its ability to work as a demo robot. The following is what is implemented so far.

### Features

- You can manually control the NAO using a DualShock 4 controller. Using a controller, you can control aspects such as:
    - Walking
    - Emotes and Dances (More emotes may come soon)
    - AI (Talk to the robot using on-device AI or connect to Google’s servers and use Gemini)
    - Control its head
- It also has an autonomous mode which:
    - Lets NAO walk on its own
    - Avoids obstacles using the sonars
    - Describe its environment (sarcastically) by taking pictures and sending it to Gemini or an on-device model.
    - Automatically wave using face detection (sometimes)

There are many features I would love to add and some of these are under this to-do section:

### To-do

- Allow you to alter the prompt of the automatic talk mode
- Add more emotes and dances to the manual controller mode
- Add foot bumper support to autonomous mode
- Possibly do something with the tactile sensors
- Let the robot detect human emotions and feed it into the AI
- A UI and button remapper

## Libraries
- [Faster Whisper](https://github.com/SYSTRAN/faster-whisper) - Audio Transcription
- [Ollama](https://github.com/ollama/ollama) - Locally run AI models
- [Paramiko](https://github.com/paramiko/paramiko) - SFTP audio files
- [Pygame](https://github.com/pygame/pygame) - Reading controller information
- [libqi](https://github.com/aldebaran/libqi) - Interfacing with the NAO robot

## License
goNAO is licensed under the GNU GPL version 3 license. More info is in [LICENSE](https://github.com/byestndr/goNAO/blob/main/LICENSE).
