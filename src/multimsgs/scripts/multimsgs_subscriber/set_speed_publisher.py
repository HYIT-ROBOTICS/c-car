#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
####          Copyright 2020 GuYueHome (www.guyuehome.com).          ###
########################################################################

# 该例程将发布/person_info话题，自定义消息类型learning_topic::Person

from multiprocessing import connection
import rospy
from multimsgs.msg import Motor_data_type

########################################################################
#port="/dev/ttyUSB0"
########################################################################

def speed_publisher():
	# ROS节点初始化
	rospy.init_node('set_speed_publisher', anonymous=True)

	# 创建一个Publisher，发布名为/person_info的topic，消息类型为learning_topic::Person，队列长度10
	speed_info_pub = rospy.Publisher('/speed_info', Speed, queue_size=10)

	#设置循环的频率
	rate = rospy.Rate(10) 

	while not rospy.is_shutdown():
		# 初始化learning_topic::Person类型的消息
		speed_msg = Motor_data_type()
		speed_msg.speed  = read_left_motorspeed()

		# 发布消息
		speed_info_pub.publish(speed_msg)
		rospy.loginfo("Publsh speed message[%s, %s]", speed_msg.name, speed_msg.speed)
		# 按照循环频率延时
		rate.sleep()
		# 初始化learning_topic::Person类型的消息
		speed_msg = Speed()
		speed_msg.name = "Right"
		speed_msg.speed  = read_left_motorspeed()

		# 发布消息
		speed_info_pub.publish(speed_msg)
		rospy.loginfo("Publsh speed message[%s, %s]", speed_msg.name, speed_msg.speed)

		# 按照循环频率延时
		rate.sleep()

if __name__ == '__main__':
	#connection485(port)
	try:
		speed_publisher()
	except rospy.ROSInterruptException:
		pass
