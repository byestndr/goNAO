from naoai import naoai
from walkingnao import joytest
import pygame
from multiprocessing import Value
from time import sleep

started = Value('i', 0)         


class joybutton():
    def controllerButtons(self, ip, port, model):
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
            elif joytest.controller.buttonStat(3) == 1 and started.value == 0:
                # The AI button
                started.value = 1
                print("Starting AI, press circle to stop.\n")
                naoai.connection_details.runFromMainStart(ip, port, model)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

    def OnAiOff(self, ip, port, model):
        done = False
        while done == False:
            if joytest.controller.buttonStat(1) == 1 and started.value == 1:
                print("Stopping Mics")
                naoai.connection_details.runFromMainStop(ip, port, model)
                started.value = 0
            else:
                pass

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True



