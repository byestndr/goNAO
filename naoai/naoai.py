"""Connect AI to NAO"""

import asyncio
from multiprocessing import Process, Queue
from naoai.ai_transcriber import Transcriber
from naoai.ai_response import AiResponse

# TODO: Get Autotalk up and working again


# This connects to the NAO
class ConnectionDetails:
    """Class with methods for connecting to the NAO."""

    def __init__(self, address, api):
        self.ip, self.port = address.ip, address.port
        self.robot_api = api

    def startMicrophone(self, api):
        """Method for starting the AI function"""

        Transcriber().queryingOn(api)
    def startTranscription(self, modelInfo):
        """Method for stopping the AI function"""
        # TODO: Get rid of the queue and multiprocessing process
        system_prompt = modelInfo.systemPrompt

        say = Queue()
        Transcriber().queryingOff(self.robot_api, self.ip)

        transcribed_text = Transcriber().transcribing()

        if modelInfo.usingGemini:
            reply = AiResponse().gemini(transcribed_text, modelInfo.apiKey, system_prompt)
        else:
            reply = AiResponse().ollama(transcribed_text, modelInfo.ollamaModel, system_prompt)

        Transcriber().tts(reply, self.robot_api)
