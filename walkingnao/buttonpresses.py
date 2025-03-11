from naoai import naoai
from . import joytest
from . import walk
import pygame
from naoai import qiapi

# from multiprocessing import Value
import threading
from time import sleep

# started = Value('i', 0)         


class joybutton():
    def controllerButtons(self, ip, port, model, started, qistarted):
        done = False
        while done == False:
            # Cross
            if joytest.controller.buttonStat(0) == 1:
                pass
            # Circle
            elif joytest.controller.buttonStat(1) == 1 and started.is_set() == False:
                qiapi.qiservice(ip, port, qistarted).recover()
            # Square
            elif joytest.controller.buttonStat(3) == 1:
                print("Waving")
                qiapi.qiservice(ip, port, qistarted).wave()
            # Triangle
            elif joytest.controller.buttonStat(2) == 1 and started.is_set() == False:
                # The AI button
                started.set()
                print("Starting AI, press circle to stop.\n")
                naoai.connection_details.runFromMainStart(ip, port, model, qistarted)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

    def OnAiOff(self, ip, port, model, started, qistarted, apikey):
        done = False

        while done == False:
            if joytest.controller.buttonStat(1) == 1 and started.is_set() == True:
                light = qiapi.qiservice(ip, port, qistarted)
                print("Stopping Mics")
                threading.Thread(target=light.aiThinking, args=(started, )).start()
                naoai.connection_details.runFromMainStop(ip, port, model, qistarted, apikey)
                started.clear()
            else:
                pass

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

