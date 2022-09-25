#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
####          Copyright 2022 HYIT Robotics Lab                       ###
####          Authors: Prime                                         ###
########################################################################

import rospy
from robotbase.msg import Command #this is a dummy

def callback(data): #replace "data" with the information you want
    rospy.loginfo("Command and Action is : ", (data.command, data.action))

def listener():
    rospy.init_node('minimal_subscriber', anonymous=True)
    rospy.Subscriber("/robotbase", Command, callback)

    rospy.spin() #python will not exit until the node is stopped

if __name__ == '__main__':
    listener()

