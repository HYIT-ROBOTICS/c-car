#!/usr/bin/env python

from __future__ import print_function

import serial
import time
import rospy
import sys, select
from rtk.msg import RTK
from std_msgs.msg import String

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty

rtkmsg = String()

class RtkPub():
    def __init__(self):
        global rtkmsg
        # Get the ~private namespace parameters from command line or launch file.
        init_message = rospy.get_param('~message', 'received rtk')
        self.rate = float(rospy.get_param('~rate', '1.0'))
        self.topic = rospy.get_param('~topic', 'rtk_cordinates')
        rospy.loginfo('rate = %d', self.rate)
        rospy.loginfo('topic = %s', self.topic)
        # Create a publisher for our custom message.
        self.pub = rospy.Publisher(self.topic, RTK, queue_size=1)
        # Set the message to publish as our custom message.
        self.msg = RTK()
        # Initialize message variables.

        # Main while loop.
    def run(self):
        # Fill in custom message variables with values from dynamic reconfigure server.
        self.msg.message = rtkmsg
        # Publish our custom message.
        self.pub.publish(self.msg)
        # Sleep for a while before publishing new messages. Division is so rate != period.
        if self.rate:
            rospy.sleep(1/self.rate)
        else:
            rospy.sleep(1.0)


if __name__ == "__main__":
    rospy.init_node('rtktalker')
    try:
        rtk = RtkPub()
        ser = serial.Serial("/dev/ttyACM0", 9600)
        print("received: ",ser)
        while not rospy.is_shutdown():
              line = str(str(ser.readline())[2:])
              #print("line: ",line)
              #print("four chars: ", line[:2])
              if(line[:4] == ('NGGA')):
                line = line.split(",", 14)
                #print("filtered: ",line)
                rtkmsg.data = str(line[2][:2])+"d"+str(line[2][2:4])+"m"+str(float(line[2][4:])*60).ljust(9, '0')+"s N\n"+str(line[4][:3])+"d"+str(line[4][3:5])+"m"+str(float(line[4][5:])*60).ljust(9, '0')+"s E"
                print("message: ",rtkmsg.data)
                rtk.pub.publish(rtkmsg.data)
        ser.close()
    except rospy.ROSInterruptException: pass
