#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
####          Copyright 2020 GuYueHome (www.guyuehome.com).          ###
########################################################################

# 该例程将订阅/person_info话题，自定义消息类型learning_topic::Person

import rospy
from multimsgs.msg import Motor_data_type
from multimsgs.msg import Set_speed
from multimsgs.msg import Set_pose

speed = "0"
dir = "00"
deg = "0"


def multimsg_publisher():
    global speed, dir, deg
    # ROS节点初始化
    rospy.init_node('multimsgs_SubAndPub', anonymous=True)

    # 创建一个Publisher，发布名为/person_info的topic，消息类型为learning_topic::Person，队列长度10
    speed_info_pub = rospy.Publisher('/setspeedtopic', Set_speed, queue_size=10)
    pose_info_pub = rospy.Publisher('/posetopic', Set_pose, queue_size=10)

    # 设置循环的频率
    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        # 初始化learning_topic::Person类型的消息
        speed_msg = Set_speed()
        speed_msg.sp = speed

        pose_msg = Set_pose()
        pose_msg.dir = dir
        pose_msg.deg = deg

        # 发布消息
        speed_info_pub.publish(speed_msg)
        rospy.loginfo("Publsh set speed message[%s]", speed_msg.sp)

        pose_info_pub.publish(pose_msg)
        rospy.loginfo("Publsh set pose message[direction:%s,degree:%s]", pose_msg.dir, pose_msg.deg)
        # 按照循环频率延时
        rate.sleep()


def multimsgsCallback(msg):
    global speed, dir, deg
    speed = msg.sp
    dir = msg.dir
    deg = msg.deg
    rospy.loginfo("Subscribe Speed Info: direction:%s  speed:%s  degree:%d", msg.dir, msg.sp, msg.deg)


def multimsgs_subscriber():
    # ROS节点初始化
    rospy.init_node('multimsgs_SubAndPub', anonymous=True)

    # 创建一个Subscriber，订阅名为/person_info的topic，注册回调函数personInfoCallback
    rospy.Subscriber("chatter", Motor_data_type, multimsgsCallback)


if __name__ == '__main__':
    while not rospy.is_shutdown():
        multimsgs_subscriber()
        multimsg_publisher()
