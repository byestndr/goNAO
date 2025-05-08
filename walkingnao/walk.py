import math
from time import sleep
from sys import exit
from naoai import qiapi
from qi import Application

# Argument Parser
class ConnectionDetails():
    def runFromMain(ipadd, portnum, qistarted, mode, automode):
        """ Class with methods for connecting to the NAO. """
        global ip, port, walkMode
        ip, port, walkMode = ipadd, portnum, mode

        try:
            # Initialize qi framework.
            global robot_api
            robot_api = qiapi.QiService(ip, port, qistarted)
        except RuntimeError:
            print ("Can't connect to NAO at \"" + ip + "\" at port " + str(port) +".\n"
                "Please check your script arguments. Run with -h option for help.")
            exit(1)
        print("Starting walk")

        if automode is False:
            controllerWalk(0)
        else:
            robot_api.initMove(0)
            AutoWalk().sonars()

# Controller walking function
def controllerWalk(isStarted):
    """ Reads inputs from controller and changes speed of the robot according to its values """
    import pygame
    from walkingnao import joytest

    done = False
    while done is False:
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

        if walkMode.is_set() is True:
            # Prints values out for debugging
            print(x * -0.7, y * -0.7, z * -0.7)

            # Checks if app has been initialized yet and initalizes
            robot_api.initMove(isStarted)
            isStarted = 1

            # Walks robot
            if x != 0 or y != 0 or z != 0:
                robot_api.walkto(x, y, z)
            elif x == 0 and y == 0 and z == 0:
                robot_api.stopMove()
        elif walkMode.is_set() is False:
            x, y = x * 0.2, y * 0.2
            print(x, y)

            robot_api.moveHead(y, x)

        # Pygame listener
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Done")
                done = True

        sleep(0.1)

class AutoWalk():
    """ Class called upon when autowalk mode is enabled """
    def sonars(self):
        """ Receive values from sonar and avoids obstacles based on those values """
        robot_api.initSonar()
        self.sonarLeft = []
        self.sonarRight = []
        self.leftAvg = 0
        self.rightAvg = 0

        while True:
            if robot_api.fallDetection() is False:
                robot_api.recover()

            # Calculate sonar averages
            self.sonarLeft.append(robot_api.sonarLeft())
            if len(self.sonarLeft) > 5:
                del self.sonarLeft[0]
                self.leftAvg = math.fsum(self.sonarLeft) / len(self.sonarLeft)
                #print(f"Left Average is: {leftAvg}")

            self.sonarRight.append(robot_api.sonarRight())
            if len(self.sonarRight) > 5:
                del self.sonarRight[0]
                self.rightAvg = math.fsum(self.sonarRight) / len(self.sonarRight)
                #print(f"Right Average is: {rightAvg}")

            # Checks if the average is calculated yet and if it is less than 0.4
            if self.leftAvg < 0.4 or self.rightAvg < 0.4 and robot_api.faceDetection() == []:
                self.avoid()
                sleep(1)
            elif robot_api.faceDetection() is None or robot_api.faceDetection() == []:
                robot_api.walkto(-1, 0, 0)
            else:
                print(robot_api.faceDetection())
                robot_api.stopMove()
                robot_api.wave()
                sleep(1)

    def avoid(self):
        """ Called when the robot needs to avoid an obstacle """
        print("Avoiding")
        if self.leftAvg < 0.4 and self.rightAvg > 0.4:
            robot_api.walkto(0, 0, 1)
        elif self.rightAvg < 0.4 and self.leftAvg > 0.4:
            robot_api.walkto(0, 0, -1)
        else:
            robot_api.walkto(0, 0, 1)
