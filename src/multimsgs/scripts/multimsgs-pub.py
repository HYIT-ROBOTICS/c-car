#!/usr/bin/env python

from __future__ import print_function

import rospy
from multimsgs.msg import Motor_data_type
import sys, select


dr = "00"
sp = 0
deg = 0





if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty

moveBindings = {
        'i':(1,0,0,0),
        'j':(0,0,0,1),
        'l':(0,0,0,-1),
        'm':(-1,0,0,-1),
        'I':(1,0,0,0),
        'J':(0,1,0,0),
        'L':(0,-1,0,0),
        'M':(-1,1,0,0),
        ' ':(1,3,0,0),
    }

speedBindings={
        'q':(1.1,1.1),
        'a':(.9,.9),
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
    global dr, sp, deg
    # Must have __init__(self) function for a class, similar to a C++ class constructor.
    def __init__(self):
        # Get the ~private namespace parameters from command line or launch file.
        init_message = rospy.get_param('~message', 'hello')
        self.rate = float(rospy.get_param('~rate', '1.0'))
        self.topic = rospy.get_param('~topic', 'chatter')
        rospy.loginfo('rate = %d', self.rate)
        rospy.loginfo('topic = %s', self.topic)
        # Create a publisher for our custom message.
        self.pub = rospy.Publisher(self.topic, Motor_data_type, queue_size=10)
        # Set the message to publish as our custom message.
        self.msg = Motor_data_type()
        # Initialize message variables.

        # Main while loop.
    def run(self):
        # Fill in custom message variables with values from dynamic reconfigure server.
        self.msg.dir = dr
        self.msg.sp = str(sp)
        self.msg.deg = deg
        # Publish our custom message.
        print ("deg in class: ",deg)
        self.pub.publish(self.msg)
        # Sleep for a while before publishing new messages. Division is so rate != period.
        if self.rate:
            rospy.sleep(1/self.rate)
        else:
            rospy.sleep(1.0)



# Main function.
if __name__=="__main__":
    rospy.init_node('pytalker')
    settings = saveTerminalSettings()

    x = 0
    y = 0
    z = 0
    th = 0
    status = 0

    try:
        ne = NodeExample()
        while(1):
            key = getKey(settings)
            if key in moveBindings.keys():
                print("move key = ", key)
                if (key == 'i' or key == 'I'):
                    dr = "forward"
                    ne.run()
                elif (key == 'm' or key == 'M'):
                    dr = "backward"
                    ne.run()
                elif (key == ' '):
                    dr = "stop"
                    ne.run()
                    print ("stop is ", dr)
                elif (key == 'j' or key == 'J'):
                    if (deg > -90):
                       deg = deg - 5
                    ne.run()
                elif (key == 'l' or key == 'L'):
                    if (deg < 90):
                       deg = deg + 5
                    ne.run()
                print ("deg is :", deg)
            elif key in speedBindings.keys():
                if (key == 'q' or key == 'Q'):
                    if (sp < 10):
                        sp = sp + 1
                elif (key == 'a' or key == 'A'):
                    if (sp > 0):
                        sp = sp -1
                print ("speed: ",sp)
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

    except rospy.ROSInterruptException: pass
