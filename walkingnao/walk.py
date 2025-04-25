from naoai import qiapi
from qi import Application
import threading
from time import sleep
import traceback
from sys import exit
import math

# Argument Parser
class connection_details():
    def runFromMain(ipadd, portnum, qistarted, mode, automode):
        global ip, port, walkMode
        ip, port, walkMode = ipadd, portnum, mode
        
        try:
            # Initialize qi framework.
            global walking
            walking = qiapi.qiservice(ip, port, qistarted)
        except RuntimeError:
            print ("Can't connect to NAO at \"" + ip + "\" at port " + str(port) +".\n"
                "Please check your script arguments. Run with -h option for help.")
            exit(1)
        print("Starting walk")
        
        if automode == False:
            controllerWalk(0)
        else:
            obstacle = threading.Event()
            obstacle.clear()
            walkloop = threading.Thread(target=autowalk().walkLoop, args=(obstacle, 0))
            sonars = threading.Thread(target=autowalk().sonars, args=(obstacle,))

            walkloop.start()
            sonars.start()
            
            
        
        
# Controller walking function
def controllerWalk(isStarted):
    
    from walkingnao import joytest
    import pygame

    done = False
    while done == False:
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
        
        if walkMode.is_set() == True:
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
        elif walkMode.is_set() == False:
            x, y = x * 0.2, y * 0.2
            print(x, y)

            walking.moveHead(y, x)

        # Pygame listener
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Done")
                done = True

        sleep(0.1)

class autowalk():
    def sonars(self, obstacle):
        walking.initSonar()
        self.sonarLeft = []
        self.sonarRight = []
        
        while True:
            self.sonarLeft.append(walking.sonarLeft())
            if len(self.sonarLeft) > 5:
                del self.sonarLeft[0]
                self.leftAvg = math.fsum(self.sonarLeft) / len(self.sonarLeft)
                #print(f"Left Average is: {leftAvg}")

            self.sonarRight.append(walking.sonarRight())
            if len(self.sonarRight) > 5:
                del self.sonarRight[0]
                self.rightAvg = math.fsum(self.sonarRight) / len(self.sonarRight)
                #print(f"Right Average is: {rightAvg}")

            if len(self.sonarLeft) > 5 and len(self.sonarRight) > 5:
                if self.leftAvg < 0.5 or self.rightAvg < 0.5:
                    self.avoid(obstacle)
                else:
                    print("Normal")
    
    def avoid(self, obstacle):
        obstacle.set()
        print("Avoiding")
        if self.leftAvg < 0.5 and self.rightAvg > 0.5:
            walking.walkto(0, 0, 1)
        elif self.rightAvg < 0.5 and self.leftAvg > 0.5:
            walking.walkto(0, 0, -1)
        else:
            walking.walkto(0, 0, 1)
        


        
           
               

    def walkLoop(self, obstacle, isStarted):
        walking.initMove(isStarted)
        isStarted = 1
        while True:
            if obstacle.is_set() == False:
                walking.walkto(-1, 0, 0)
        

    
    
    
        

    
    
