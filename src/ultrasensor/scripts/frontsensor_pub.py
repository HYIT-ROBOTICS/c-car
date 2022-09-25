#!/usr/bin/env python

import rospy
import os
import serial
import serial.tools.list_ports as port_list
from SerialUltra import *
from ultrasensor.msg import Sensor


min_value=200
max_value=2000
sensor_num = 2
sensor_arr=[]
sensor_stat=[]
sensor_range=[]
sensor_id=[1,2]
for i in range(0,sensor_num):
    sensor_stat.append(-1) #set all the sensor to unavailable
    sensor_arr.append(-1)
    sensor_range.append(0)
#########################################################

ports = list(port_list.comports())
# port = ports[0].device
baudrate = 9600
serialPort = ""
# port = "/dev/ttyUSB0"
port = "/dev/ttyUSB2"

def velocity_publisher():
    rospy.init_node('sensor_publisher', anonymous=True)
    sensor_info_pub = rospy.Publisher('/sensor_info', Sensor, queue_size=10)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        sensor_msg = Sensor()
        sensor_msg.id = 1
        sensor_msg.dist = 200

        sensor_info_pub.publish(sensor_msg)
        rospy.loginfo("Publsh sensor message[%d, %d]",
                      sensor_msg.id, sensor_msg.dist)

        rate.sleep()


def connection(po):
    global serialPort
    try:
        serialPort = serial.Serial(port=po, baudrate=baudrate, bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE)
        print("Serial Port is oppened as:", po)
        return 1
    except:
        return 0


def connection485(po):
    global serialPort
    try:
        send = serial.Serial(
            # port='/dev/ttyUSB0',
            port="/dev/ttyUSB4",
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        print("Serial Port is oppened as:", po)
        return 1
    except:
        return 0

def sensorData_publisher():
    connection(port)

    # sens1 = SerialUltra(serialPort, 5, 7)
    # sens2 = SerialUltra(serialPort, 5, 4)
    # sens3 = SerialUltra(serialPort, 5, 2)
    # sens4 = SerialUltra(serialPort, 5, 8)
    ######################################
    # ********** Open and check sensor port*
    counter = 0
    print("trying to open sensor")
    for i in sensor_id:  # go through all the id to check sensor availability
        print(i)
        sensor_arr[counter] = SerialUltra(serialPort, 5, i)
        value = sensor_arr[counter].read()
        print(value)
        if value == None:
            sensor_arr[counter] = -1
        print("!!! Sensor ", i, " is not connected !!! ")
        # sensor_arr[counter]=-1
        counter += 1
        print("sensor avalilables=", sensor_arr)  # Must be checked later for correct printing
        print(sensor_id)

    rospy.init_node('frontUltraSensor_pub', anonymous=True)
    frontUltraSensor_info_pub = rospy.Publisher('/frontUltraSensor_info', Sensor, queue_size=10)

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():

        for index in (sensor_id):
            pos = sensor_id.index(index)
            # print ("index: ",pos)
            sensor = sensor_arr[pos]
            if sensor != -1:
                value = sensor.read()

                if value < 200 or value > 2000:
                    print("value is not acceptable")
                    value = 0
                else:
                    print("sensor id{} range: {}".format(index, value))
                    sensor_range[pos] = value
        # print ("Sensor range array: ", sensor_range)
        os.system("rostopic pub -1 /ultras std_msgs/Int32MultiArray 'data: {0}'".format(sensor_range))
        # else:
        # print("Sensor {} unavailable".format(sensor_id[index]))

        sensor_msg = Sensor()
        sensor_msg.id = index;
        sensor_msg.dist = value;

        frontUltraSensor_info_pub.publish(sensor_msg)
        rospy.loginfo("Publish sensor message[%d, %d]",
                      sensor_msg.id, sensor_msg.dist)

        rate.sleep()



if __name__ == '__main__':
    try:
        sensorData_publisher()
    except rospy.ROSInterruptException:
        pass
