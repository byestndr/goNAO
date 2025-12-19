import math
from time import sleep
from sys import exit
import resource.qiapi as qiapi

# Argument Parser
class ConnectionDetails():
    """ Class with methods for connecting to the NAO. """
    def runFromMain(self, api):
        """ Method for connecting to NAO and starting autowalk """
        print("Starting autowalk")

        api.initMove(0)
        AutoWalk(api).sonars()

class AutoWalk():
    """ Class called upon when autowalk mode is enabled """
    def __init__(self, api):
        self.sonarLeft = []
        self.sonarRight = []
        self.leftAvg = 0
        self.rightAvg = 0
        self.api = api
    def sonars(self):
        """ Receive values from sonar and avoids obstacles based on those values """
        self.api.initSonar()

        while True:
            if self.api.fallDetection() is False:
                self.api.recover()

            # Calculate sonar averages
            self.sonarLeft.append(self.api.sonarLeft())
            if len(self.sonarLeft) > 3:
                del self.sonarLeft[0]
                self.leftAvg = math.fsum(self.sonarLeft) / len(self.sonarLeft)
                #print(f"Left Average is: {leftAvg}")

            self.sonarRight.append(self.api.sonarRight())
            if len(self.sonarRight) > 3:
                del self.sonarRight[0]
                self.rightAvg = math.fsum(self.sonarRight) / len(self.sonarRight)
                #print(f"Right Average is: {rightAvg}")

            # Checks if the average is calculated yet and if it is less than 0.4
            if self.leftAvg < 0.4 or self.rightAvg < 0.4 and self.api.faceDetection() == []:
                self.avoid()
                sleep(1)
            elif self.api.faceDetection() is None or self.api.faceDetection() == []:
                self.api.walkto(-1, 0, 0)
            else:
                print(self.api.faceDetection())
                self.api.stopMove()
                self.api.wave()
                sleep(1)

    def avoid(self):
        """ Called when the robot needs to avoid an obstacle """
        print("Avoiding")
        if self.leftAvg < 0.4 and self.rightAvg > 0.4:
            self.api.walkto(0, 0, 1)
        elif self.rightAvg < 0.4 and self.leftAvg > 0.4:
            self.api.walkto(0, 0, -1)
        else:
            self.api.walkto(0, 0, 1)
