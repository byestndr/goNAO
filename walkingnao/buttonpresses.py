""" Interface with the DualShock 4 """
import threading
import pygame
from goNAO.naoai import qiapi, stoptts, naoai
from goNAO.walkingnao import joystick

class JoyButton():
    """ Control what happens with what happens during button presses """
    def controllerButtons(self, ip, port, model, started, qistarted, walkmode, auto, apikey):
        """ Watch for button presses """
        done = False
        modes = ("walking", "headControl")
        current_mode = 0
        while done is False:
            # Cross
            if joystick.controller.buttonStat(0) == 1:
                pass
            # Circle
            elif joystick.controller.buttonStat(1) == 1 and started.is_set() is False:
                qiapi.QiService(ip, port, qistarted).recover()
            # Square
            elif joystick.controller.buttonStat(3) == 1:
                print("Waving")
                qiapi.QiService(ip, port, qistarted).wave()
            # Triangle
            elif joystick.controller.buttonStat(2) == 1 and started.is_set() is False:
                # AI button
                started.set()
                print("Starting AI, press circle to stop.\n")
                naoai.ConnectionDetails.runFromMainStart(ip, port, model, qistarted, auto, apikey)
            # DPAD UP
            elif joystick.controller.hatpos() == (0, 1):
                for x in modes:
                    try:
                        current_mode = modes.index(modes[current_mode+1])
                        print(modes[current_mode])
                        walkmode.clear()
                        break
                    except IndexError:
                        pass
            # DPAD DOWN
            elif joystick.controller.hatpos() == (0, -1) and current_mode != 0:
                for x in modes:
                    try:
                        current_mode = modes.index(modes[current_mode-1])
                        print(modes[current_mode])
                        walkmode.set()
                        print(walkmode.is_set())
                        break
                    except IndexError:
                        pass
            elif joystick.controller.buttonStat(9) == 1:
                stoptts.ConnectionDetails().runFromMain(ip, port, qistarted)
                started.clear()
            # DPAD LEFT
            # elif joytest.controller.buttonStat(13) == 1:
            #     pass
            #  DPAD RIGHT
            # elif joytest.controller.buttonStat(14) == 1:
            #     pass
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

    def onAiOff(self, ip, port, model, started, qistarted, apikey, sysprompt):
        """ Actions to take when microphones turn off """
        done = False
        while done is False:
            if joystick.controller.buttonStat(1) == 1 and started.is_set():
                light = qiapi.QiService(ip, port, qistarted)
                print("Stopping Mics")
                threading.Thread(target=light.aiThinking, args=(started, )).start()
                naoai.ConnectionDetails.runFromMainStop(ip, port, model, qistarted, apikey, sysprompt)
                started.clear()
            else:
                pass

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
