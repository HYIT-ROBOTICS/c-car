#!/usr/bin/env python

import serial
import rospy
from connectultra import *
from SerialUltra import *
import serial.tools.list_ports as port_list
from multimsgs.msg import wheel

name = "00"
sp = "00"


# A 2nd comlement for 32 bithex
def s32(value):
    if value == -1: return 0
    value = int((str("0x") + value),16)
    return -(value & 0X80000000) | (value & 0x7fffffff)

# Create a callback function for the subscriber.
def callback(data):
    global name, sp
    if (int(data.sp) < 10):
        sp = "0" + str(data.sp)
    else:
        sp = str(data.sp)
    # Simply print out values in our custom message.
    rospy.loginfo(rospy.get_name() + " heard %s %s", data.name, data.sp)
    if (data.name == "left"):
        run_forward_drive_motor("01", "01", sp)
        rospy.loginfo ("motorname:%s,sp:%s", data.name, data.sp)
    if (data.name == "right"):
        run_forward_drive_motor("02", "01", sp)
        rospy.loginfo ("motorname:%s,sp:%s", data.name, data.sp)



# This ends up being the main while loop.
def listener():
    # Get the ~private namespace parameters from command line or launch file.
    topic = rospy.get_param('~topic', 'wheelchatter')
    # Create a subscriber with appropriate topic, custom message and name of callback function.
    rospy.Subscriber(topic, wheel, callback)
    # Wait for messages on topic, go to callback function when new messages arrive.
    rospy.spin()

# Main function.
if __name__ == '__main__':
    # Initialize the node and name it.
    rospy.init_node('pylistener_wheel', anonymous = True)
    # Go to the main loop.
    listener()
    print
