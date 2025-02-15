from naoai import naoai
from walkingnao import joytest
import pygame

def controllerButtons(ip, port, model):
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
        elif joytest.controller.buttonStat(3) == 1:
            # The AI button
            global started
            started = 1
            print("Starting AI")
            naoai.connection_details.runFromMainStart(ip, port, model)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

def OnAiOff(ip, port, model):
    done == False
    while done == False:
        if joytest.controller.buttonStat(3) == 1 and started == 1:
            naoai.connection_details.runFromMainStop(ip, port, model)
            global started
            started = 0
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True