import pygame
from os import environ
from time import sleep
from sys import exit
environ['SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS]'] = '1'

pygame.display.init()
# Initialize joystick
pygame.joystick.init()
print("Number of joysticks: "+str(pygame.joystick.get_count()))
try:
    joys = pygame.joystick.Joystick(0)
except pygame.error:
    print("No joysticks detected, please connect one.")
    exit(1)
joys.init()
#axes = (0, 1)
#print(axes)

class controller:
    def axispos(axesnum):
        if joys.get_axis(axesnum) < -0.1 or joys.get_axis(axesnum) > 0.1:
            # Prints the axes for debugging
            # print(f"Axis number is {axesnum} and the value is {joys.get_axis(axesnum)}")
            return joys.get_axis(axesnum)
        else:
            return 0    
    def buttonStat(button):
        return joys.get_button(button)
    def buttonNum():
        return range(joys.get_numbuttons())
    def hatpos():
        return joys.get_hat(0)

# done = False
