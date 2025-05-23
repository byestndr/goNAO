from time import sleep
from sys import exit
from threading import Event
import resource.qiapi as qiapi

# Argument Parser
class ConnectionDetails():
    def runFromMain(ipadd, portnum, qistarted, mode, stop=False, log=None):
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
        controllerWalk(0, stop, log)


# Controller walking function
def controllerWalk(isStarted, stop, log):
    """ Reads inputs from controller and changes speed of the robot according to its values """
    done = False
    if type(stop) == threading.Event:
            stop = stop.is_set()
    from walkingnao import joystick
    import pygame
    while done is False and stop is False:
        # Gets position for x and y axes on the left stick
        # Controller Axes
        y = joystick.controller().axispos(0)
        x = joystick.controller().axispos(1)
        # Z is rotation
        z = joystick.controller().axispos(3)

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
            if log is not None:
                log.put(str(x * -0.7, y * -0.7, z * -0.7))
            else:
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
    robot_api.stopMove()
    return
