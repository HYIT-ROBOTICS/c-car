#!/usr/bin/env python

from __future__ import print_function
import RPi.GPIO as GPIO
import rospy
from multimsgs.msg import Motor_data_type
import sys, select
import time

dr = "00"
sp = 0
deg = 0
but_pin = 23
emr_state = "safe"

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty


def start(but_pin):
    global emr_state
    if GPIO.input(but_pin):
    	emr_state="safe"
    else:
        emr_state="emergency"
        ne = NodeExample()
        dr = "stop"
        ne.run()
    print(emr_state)

#----------------------------------------------
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
    rospy.init_node('pytalker2')
    settings = saveTerminalSettings()
	
    x = 0
    y = 0
    z = 0
    th = 0
    status = 0 
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
    GPIO.setup(but_pin, GPIO.IN)  # button pin set as input
    #GPIO.setup(bump_pin, GPIO.IN) # Front and back bumpers
    GPIO.setwarnings(False) # disable warnings
    GPIO.add_event_detect(but_pin, GPIO.BOTH, callback=start, bouncetime=20)
    #GPIO.add_event_detect(but_pin, GPIO.RISING, callback=stop, bouncetime=10)
    print ("Emergency System is Ready!")
    try:
        while True:
            pass
            
    finally:
        GPIO.cleanup()
