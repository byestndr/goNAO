from os import environ
from time import sleep
from sys import exit
import pygame
environ['SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS]'] = '1'

class controller:
    def __init__(self):
        pygame.display.init()
        # Initialize joystick
        pygame.joystick.init()
        # print("Number of joysticks: "+str(pygame.joystick.get_count()))
        try:
            self.joys = pygame.joystick.Joystick(0)
        except pygame.error:
            print("No joysticks detected, please connect one.")
            exit(1)
        self.joys.init()
        #axes = (0, 1)
        #print(axes)
    def axispos(self, axesnum):
        if self.joys.get_axis(axesnum) < -0.1 or self.joys.get_axis(axesnum) > 0.1:
            # Prints the axes for debugging
            # print(f"Axis number is {axesnum} and the value is {self.joys.get_axis(axesnum)}")
            return self.joys.get_axis(axesnum)
        else:
            return 0
    def buttonStat(self, button):
        return self.joys.get_button(button)
    def buttonNum():
        return range(self.joys.get_numbuttons())
    def hatpos():
        return self.joys.get_hat(0)

done = False
while done == False:
    print(controller().axispos(1))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Done")
            done = True
