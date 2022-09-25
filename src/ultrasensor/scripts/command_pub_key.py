 #!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
####          Copyright 2020 GuYueHome (www.guyuehome.com).          ###
########################################################################

# 该例程将发布/person_info话题，自定义消息类型learning_topic::Person

import rospy
from robotbase.msg import Command
from connectultra import *
from SerialUltra import *
from command import *


def velocity_publisher():
    # ROS节点初始化
    rospy.init_node('command_publisher', anonymous=True)

    # 创建一个Publisher，发布名为/robotbase的topic，消息类型为learning_topic::Command，队列长度10
    person_info_pub = rospy.Publisher('/robotbase', Command, queue_size=10)

    # 设置循环的频率
    rate = rospy.Rate(1)
    # connection485(port)
    # test1 = SerialUltra(serialPort)
    str_cmd_left_drive = controller_cmd_str("01", "01", "00", "05")  # left drive motor  motor forward rotation  speed 5
    str_cmd_right_drive = controller_cmd_str("02", "01", "00", "05")  # right drive motor  motor forward rotation  speed 5

    str_cmd_left_drive_back = controller_cmd_str("01", "02", "00", "05")  # left drive motor  motor back rotation  speed 5
    str_cmd_right_drive_back = controller_cmd_str("02", "02", "00", "05")  # right drive motor  motor back rotation  speed 5
    
    str_cmd_left_drive_stop = controller_cmd_str("01", "03", "00", "00")  # left drive motor  motor stop rotation  speed 0
    str_cmd_right_drive_stop = controller_cmd_str("02", "03", "00", "00")  # right drive motor  motor stop rotation  speed 0

    str_cmd_turn_left = controller_cmd_str("0A", "01", "00", "2D")  #turn left
    str_cmd_turn_right = controller_cmd_str("0A", "02", "00", "2D")  # turn right


    while not rospy.is_shutdown():
        # 初始化robotbase::command类型的消息
        person_msg = Command()

        person_msg.command = str_cmd_left_drive;
        person_msg.action = "left drive motor";
        run_left_drive_motor()
        person_info_pub.publish(person_msg)
        rate.sleep()

        person_msg.command = str_cmd_right_drive;
        person_msg.action = "right drive motor";
        run_right_drive_motor()
        person_info_pub.publish(person_msg)
        rate.sleep()

        person_msg.command = str_cmd_left_drive_back;
        person_msg.action = "left drive motor back";
        run_left_drive_motor_back()
        person_info_pub.publish(person_msg)
        rate.sleep()

        person_msg.command = str_cmd_right_drive_back;
        person_msg.action = "right drive motor back";
        run_right_drive_motor_back()
        person_info_pub.publish(person_msg)
        rate.sleep()
        
        person_msg.command = str_cmd_left_drive_stop;
        person_msg.action = "left drive motor stop";
        run_left_drive_motor_stop()
        person_info_pub.publish(person_msg)
        rate.sleep()
        
        person_msg.command = str_cmd_right_drive_stop;
        person_msg.action = "right drive motor stop";
        run_right_drive_motor_stop()
        person_info_pub.publish(person_msg)
        rate.sleep()

        person_msg.command = str_cmd_turn_left;
        person_msg.action = "turn left";
        run_turn_left()
        person_info_pub.publish(person_msg)
        rate.sleep()

        person_msg.command = str_cmd_turn_right;
        person_msg.action = "turn right";
        run_turn_right()
        person_info_pub.publish(person_msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        velocity_publisher()
    except rospy.ROSInterruptException:
        pass
