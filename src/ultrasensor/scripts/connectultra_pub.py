#!/usr/bin/env python

import rospy
import os
import serial
import serial.tools.list_ports as port_list
from SerialUltra import *

ports = list(port_list.comports())
baudrate = 9600
serialPort = ""
port = '/dev/ttyUSB0'

def connection(po):
    global serialPort
    try:
        serialPort = serial.Serial(port=po, baudrate=baudrate, bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE)
        print("Serial Port is opened as:", po)
        return 1
    except:
        return 0


def connection485(po):
    global serialPort
    try:
        send = serial.Serial(
            port='COM5',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        print("Serial Port is opened as:", po)
        return 1
    except:
        return 0


connection(port)
sens1 = SerialUltra(serialPort, 5, 2)
sens2 = SerialUltra(serialPort, 5, 4)
sens3 = SerialUltra(serialPort, 5, 5)
sens4 = SerialUltra(serialPort, 5, 6)
sens5 = SerialUltra(serialPort, 5, 7)
sens6 = SerialUltra(serialPort, 5, 8)

'''while True:
    print("222  ", sens1.read())
    print("444  ", sens2.read())
    print("555  ", sens3.read())
    print("666  ", sens4.read())
    print("777  ", sens5.read())
    print("888  ", sens6.read())'''

def talker():
    pub = rospy.Publisher('serial_chatter', read)
    rospy.init_node('serial_talker', anonymous=True)
    r = rospy.rate(10) #10hz
    msg = read()
    msg.name = "Sensor is: "
    msg.age = 10

    while not rospy.is_shutdown():
        rospy.loginfo(msg)
        pub.publish(msg)
        r.sleep()

if __name__ == '__main__':
   try:
      talker()
   except rospy.ROSInterruptException: pass
