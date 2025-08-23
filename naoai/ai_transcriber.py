import paramiko
from faster_whisper import WhisperModel
from naoai.ai_response import AiResponse
from os import path, remove



class Transcriber:
    """Transcribes audio and turns it into text. Also carries the text-to-speech method."""

    def queryingOn(self, api):
        """Turns on the microphones and defines where to save the audio file."""
        channels = [0, 0, 1, 0]
        api.stopRecord()
        api.startRecord(
            "/home/nao/recordings/microphones/request.wav", "wav", 48000, channels
        )
        print("SPEAK NOW")

    def queryingOff(self, api, ip):
        """Turns off the microphone and transfers the file over to the computer"""
        api.stopRecord()
        global audfile
        audfile = path.dirname(path.realpath(__file__)) + "/request.wav"
        print(audfile)
        # SCPs the file over to the host
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, username="nao", password="nao")
        ssh.open_sftp().get("/home/nao/recordings/microphones/request.wav", audfile)

    def transcribing(self, model, say, apikey, sysprompt):
        """
        Transcribes the audio file to text and plugs the
        transcript into the AI model. Then it puts the reply in the queue
        """
        # Sets model size
        model_size = "tiny.en"

        # Transcribes using faster whisper
        whispmodel = WhisperModel(
            model_size, device="cuda", compute_type="int8_float16"
        )
        segments, info = whispmodel.transcribe(str(audfile))

        segments = list(segments)
        for segment in segments:
            print(segment.text)
            cleanedQuery = segment.text

        # Deletes audio request
        if path.isfile(audfile) is True:
            remove(audfile)

        # Make NAO say the response by calling the method corresponding to each model
        if model == "gemini":
            reply = AiResponse().gemini(cleanedQuery, apikey, sysprompt)
        else:
            reply = AiResponse().ollama(cleanedQuery, model, sysprompt)

        # Puts the reply into the speech queue
        say.put(reply)

    def tts(self, reply, api):
        """Makes the robot say whatever is in the reply parameter"""
        try:
            print("Starting talk")
            api.speechTalk(reply)
        except RuntimeError as e:
            if e == "Future canceled.":
                print("Stopped talking")
