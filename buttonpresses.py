#from naoai import naoai
from walkingnao import joytest
import pygame
# from multiprocessing import Value
import threading
from time import sleep

# started = Value('i', 0)         


class joybutton():
    def controllerButtons(self, ip, port, model, started):
        done = False
        while done == False:
            # Cross
            if joytest.controller.buttonStat(0) == 1:
                pass
            # Circle
            elif joytest.controller.buttonStat(1) == 1:
                pass
            # Square
            elif joytest.controller.buttonStat(2) == 1:
                pass
            # Triangle
            elif joytest.controller.buttonStat(3) == 1 and started.is_set() == False:
                # The AI button
                started.set()
                print("Starting AI, press circle to stop.\n")
                #naoai.connection_details.runFromMainStart(ip, port, model)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

    def OnAiOff(self, ip, port, model, started):
        done = False
        while done == False:
            if joytest.controller.buttonStat(1) == 1 and started.is_set() == True:
                print("Stopping Mics")
                #naoai.connection_details.runFromMainStop(ip, port, model)
                started.clear()
            else:
                pass

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

