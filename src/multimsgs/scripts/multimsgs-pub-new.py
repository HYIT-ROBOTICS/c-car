#!/usr/bin/env python

from __future__ import print_function

import rospy
from multimsgs.msg import wheel
import sys, select

name = ""
leftsp = 0
rightsp = 0
sp = 0

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty

moveBindings = {
    'i': (1, 0, 0, 0),
    'j': (0, 0, 0, 1),
    'l': (0, 0, 0, -1),
    'm': (-1, 0, 0, -1),
    'I': (1, 0, 0, 0),
    'J': (0, 1, 0, 0),
    'L': (0, -1, 0, 0),
    'M': (-1, 1, 0, 0),
    ' ': (1, 3, 0, 0),
}

speedBindings = {
    'q': (1.1, 1.1),
    'a': (.9, .9),
    'w': (1.0, 1.0),
    's': (.8, .8),
}


def getKey(settings):
    tty.setraw(sys.stdin.fileno())
    # sys.stdin.read() returns a string on Linux
    print("Waiting a key ...")
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def saveTerminalSettings():
    return termios.tcgetattr(sys.stdin)


# Node example class.
class NodeExample():
    global name, sp

    # Must have __init__(self) function for a class, similar to a C++ class constructor.
    def __init__(self):
        # Get the ~private namespace parameters from command line or launch file.
        init_message = rospy.get_param('~message', 'hello')
        self.rate = float(rospy.get_param('~rate', '100.0'))
        self.topic = rospy.get_param('~topic', 'wheelchatter')
        rospy.loginfo('rate = %d', self.rate)
        rospy.loginfo('topic = %s', self.topic)
        # Create a publisher for our custom message.
        self.pub = rospy.Publisher(self.topic, wheel, queue_size=10)
        # Set the message to publish as our custom message.
        self.msg = wheel()
        # Initialize message variables.

        # Main while loop.

    def run(self):
        # Fill in custom message variables with values from dynamic reconfigure server.
        self.msg.name = str(name)
        self.msg.sp = str(sp)
        # Publish our custom message.
        self.pub.publish(self.msg)
        rospy.loginfo("motorname:%s,speed:%s",self.msg.name,self.msg.sp)
        # Sleep for a while before publishing new messages. Division is so rate != period.
        if self.rate:
            rospy.sleep(1 / self.rate)
        else:
            rospy.sleep(1.0)


# Main function.
if __name__ == "__main__":
    rospy.init_node('pytalker_wheel')
    settings = saveTerminalSettings()

    x = 0
    y = 0
    z = 0
    th = 0
    status = 0

    try:
        ne = NodeExample()
        while (1):
            key = getKey(settings)
            if key in speedBindings.keys():
                if (key == 'q' or key == 'Q'):
                    if (leftsp < 10):
                        leftsp = leftsp + 1
                        sp=leftsp
                        name = "left"
                        ne.run()
                elif (key == 'a' or key == 'A'):
                    if (leftsp > 0):
                        leftsp = leftsp - 1
                        sp=leftsp
                        name = "left"
                        ne.run()
                if (key == 'w' or key == 'W'):
                    if (rightsp < 10):
                        rightsp = rightsp + 1
                        sp=rightsp
                        name = "right"
                        ne.run()
                elif (key == 's' or key == 'S'):
                    if (rightsp > 0):
                        rightsp = rightsp - 1
                        sp=rightsp
                        name = "right"
                        ne.run()

                print("speed: ", sp)
                print("name: ", name)
                print("speed key = ", key)
            else:
                # Skip updating cmd_vel if key timeout and robot already
                # stopped.
                if key == '' and x == 0 and y == 0 and z == 0 and th == 0:
                    continue
                x = 0
                y = 0
                z = 0
                th = 0
                if (key == '\x03'):
                    break

    except rospy.ROSInterruptException:
        pass
