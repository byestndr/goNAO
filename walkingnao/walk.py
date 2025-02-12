from qi import Application
import joytest
import pygame
import argparse
from time import sleep
import traceback
import multiprocessing
import naoai

isStarted = 0

# Services and robot interfacing class
class walk():
    def __init__(self, app):
        app.start()
        session = app.session
        # Connect to the services
        try:
            self.loco = session.service("ALMotion")
            self.pos = session.service("ALRobotPosture")
            self.mem = session.service("ALMemory")
            print("Connected to the Motion and Posture services")
        except Exception as e:
            print("Could not connect to service")
            traceback.print_exc()
            exit(1)
    def walkto(self, x, y, z):
        # Slows down the movement to prevent falls
        self.loco.moveToward(x * -0.7, y * -0.7, z * -0.7)
    def start(self, started):
        if started == 0:
            self.pos.goToPosture("StandInit", 0.5)
            self.loco.wakeUp()
            self.loco.moveInit()
    def stopMove(self):
        self.loco.stopMove()
    # Subscribes to robot fallen event and sees if robot falls
    def hasFallen(self):
        if self.mem.subscriber("robotHasFallen") != True:
            return True
    # Attempts to recover robot
    def recover(self):
        self.pos.goToPosture("LyingBack", 0.6)
        self.pos.goToPosture("Sit", 0.6)
        self.pos.goToPosture("StandInit", 0.6)

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="IP address for the NAO robot. Cannot be a simulated robot as they are not supported")
    parser.add_argument("--port", type=int, default=9559,
                        help="NAO port")

args = parser.parse_args()

try:
    # Initialize qi framework.
    connection_url = "tcp://" + args.ip + ":" + str(args.port)
    app = Application(["NAOAI", "--qi-url=" + connection_url])
    walking = walk(app)
except RuntimeError:
    print ("Can't connect to NAO at \"" + args.ip + "\" at port " + str(args.port) +".\n"
        "Please check your script arguments. Run with -h option for help.")
    exit(1)

# Controller walking function
def controllerWalk():
    done = False
    while done == False:

        # If the robot falls, it should automatically recover
        if walking.hasFallen() == True:
            walking.recover()

        # Gets position for x and y axes on the left stick
        # Controller Axes
        y = joytest.controller.axispos(0)
        x = joytest.controller.axispos(1)
        # Z is rotation
        z = joytest.controller.axispos(2)

        # Checks if Z axis is being used
        if z > 0 or z < 0:
            x, y = 0, 0

        if abs(x) > abs(y):
            y = 0
        elif abs(y) > abs(x):
            x = 0
        else: 
            pass
        
        # Prints values out for debugging
        print(x, y, z)

        # Checks if app has been initialized yet and initalizes
        walking.start(isStarted)
        isStarted = 1

        # Pygame listener
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Controller code
        if x != 0 and y != 0 and z != 0:
            walking.walkto(x, y, z)
        elif x == 0 and y == 0 and z == 0:
            print("No movement")
            walking.stopMove()
        sleep(0.6)

def controllerButtons():
    while done == False:
        # Cross
        if controller.buttonStat(0) == 1:
            pass
        # Circle
        elif controller.buttonStat(1) == 1:
            pass
        # Square
        elif controller.buttonStat(2) == 1:
            pass
        # Triangle
        elif controller.buttonStat(3) == 1:
            # likely going to be the AI button
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True    

walkTheBot = multiprocessing.Process(target=controllerWalk)
buttonCommand = multiprocessing.Process(target=controllerButtons)
