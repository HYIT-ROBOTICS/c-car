#!/usr/bin/env python

import serial
import time

def listener():
    rospy.init_node('serial_listener', anonymous=True)
    rospy.Subscriber("serial_chatter", callback)

if __name__=='__main__:
    listener()

