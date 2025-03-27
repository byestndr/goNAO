from naoai import naoai
import joytest
from . import walk
import pygame
from naoai import qiapi
import threading
from time import sleep

class joybutton():
    def controllerButtons(self, ip, port, model, started, qistarted):
        done = False
        modes = ("walking", "headControl")
        currentMode = 0
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
                # AI button
                started.set()
                print("Starting AI, press circle to stop.\n")
                naoai.connection_details.runFromMainStart(ip, port, model, qistarted)
            # DPAD UP
            if joytest.controller.hatpos() == (0, 1):
                for x in modes:
                    try:
                        currentMode = modes.index(modes[currentMode+1])
                        print(modes[currentMode])
                        break
                    except IndexError:
                        pass
                        
            # DPAD DOWN
            elif joytest.controller.hatpos() == (0, -1) and currentMode != 0:
                for x in modes:
                    try:
                        currentMode = modes.index(modes[currentMode-1])
                        #print(modes[currentMode])
                        print(modes[currentMode])
                        break
                    except IndexError:
                        print(currentMode)
                        pass
                    
            # DPAD LEFT
            # elif joytest.controller.buttonStat(13) == 1:
            #     pass
            #  DPAD RIGHT
            # elif joytest.controller.buttonStat(14) == 1:
            #     pass
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
while True:
    joybutton().controllerButtons(False, False, False, False, False)

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

