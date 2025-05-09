import math
from time import sleep
from sys import exit
import naoai.qiapi as qiapi

# Argument Parser
class ConnectionDetails():
    def runFromMain(ipadd, portnum, qistarted):
        """ Class with methods for connecting to the NAO. """
        global ip, port, walkMode
        ip, port = ipadd, portnum

        try:
            # Initialize qi framework.
            global robot_api
            robot_api = qiapi.QiService(ip, port, qistarted)
        except RuntimeError:
            print ("Can't connect to NAO at \"" + ip + "\" at port " + str(port) +".\n"
                "Please check your script arguments. Run with -h option for help.")
            exit(1)
        print("Starting autowalk")

        robot_api.initMove(0)
        AutoWalk().sonars()

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
