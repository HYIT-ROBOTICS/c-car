#!/usr/bin/env python

from __future__ import print_function
import RPi.GPIO as GPIO
import rospy
from multimsgs.msg import Motor_data_type
import sys, select
import time

but_pin = 23
flag = 1
dr = "00"
sp = 0
deg = 0


if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty

'''moveBindings = {
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
        '''

def start(but_pin):
    global emr_state
    if GPIO.input(but_pin):
        emr_state = 'safe'
    else:
        ne = NodeExample()
        emr_state="emrgence"
        sp=0
        dr = "stop"
        ne.run()
    print(state)


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
    flag = 1
    rospy.init_node('pytalker_em')
    settings = saveTerminalSettings()
	
    x = 0
    y = 0
    z = 0
    th = 0
    status = 0 
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
    GPIO.setup(but_pin, GPIO.IN)  # button pin set as input
    GPIO.setwarnings(False) # disable warnings
    GPIO.add_event_detect(but_pin, GPIO.FALLING, callback=start, bouncetime=10)

    print ("Emergency System is Ready!!")
    #dr = "forward"
    try:
        ne = NodeExample()
	#ne.run()
        while(1):
            pass
    finally:
        GPIO.cleanup()


	    
    except rospy.ROSInterruptException: pass
