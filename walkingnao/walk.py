from naoai import qiapi
from qi import Application
from walkingnao import joytest
import pygame
import argparse
from time import sleep
import traceback

# Argument Parser
class connection_details():
    def runFromCurrent():
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", type=str, default="127.0.0.1",
                            help="IP address for the NAO robot. Cannot be a simulated robot as they are not supported")
        parser.add_argument("--port", type=int, default=9559,
                            help="NAO port")
        global ip, port
        args = parser.parse_args()
        ip, port = args.ip, args.port
        
        try:
            # Initialize qi framework.
            connection_url = "tcp://" + ip + ":" + str(port)
            global walking
            app = Application(["NAOAI", "--qi-url=" + connection_url])
            walking = qiapi.qiservice(app)
            walking.hasFallen()

        except RuntimeError:
            print ("Can't connect to NAO at \"" + ip + "\" at port " + str(port) +".\n"
                "Please check your script arguments. Run with -h option for help.")
            exit(1)

    def runFromMain(ipadd, portnum, qistarted):
        global ip, port, model, norobot, nomic
        ip, port = ipadd, portnum
        
        try:
            # Initialize qi framework.
            global walking
            walking = qiapi.qiservice(ip, port, qistarted)
        except RuntimeError:
            print ("Can't connect to NAO at \"" + ip + "\" at port " + str(port) +".\n"
                "Please check your script arguments. Run with -h option for help.")
            exit(1)
        print("Starting walk")
        controllerWalk(0)
        
        
if __name__ == "__main__":
    connection_details.runFromCurrent()
        
# Controller walking function
def controllerWalk(isStarted):
    done = False
    while done == False:

        # If the robot falls, it should automatically recover
        # ROBOT DOES NOT RECOVER PLEASE FIX
        # MAKE CONTROLLER BUTTON
        # if walking.ifFallen() == True:
        #     print("FALLEN")
        #     walking.recover()
        # else:
        #     pass

        # Gets position for x and y axes on the left stick
        # Controller Axes
        y = joytest.controller.axispos(0)
        x = joytest.controller.axispos(1)
        # Z is rotation
        z = joytest.controller.axispos(3)

        # Checks if Z axis is being used
        if z > 0 or z < 0:
            x, y = 0, 0
        
        # Only uses one axis at a time
        if abs(x) > abs(y):
            y = 0
        elif abs(y) > abs(x):
            x = 0
        elif abs(y) == abs(x):
            x, y = 0, 0 
            
        
        # Prints values out for debugging
        print(x * -0.7, y * -0.7, z * -0.7)

        # Checks if app has been initialized yet and initalizes
        walking.initMove(isStarted)
        isStarted = 1

        # Walks robot
        if x != 0 or y != 0 or z != 0:
            walking.walkto(x, y, z)
        elif x == 0 and y == 0 and z == 0:
            walking.stopMove()
        
        # Pygame listener
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Done")
                done = True

        sleep(0.1)

if __name__ == "__main__":
    controllerWalk(0)