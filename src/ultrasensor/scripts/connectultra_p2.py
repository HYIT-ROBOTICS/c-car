'''
Written by Amir A Mokhtarzadeh
Date: Feb 2022
HuaiYin Institute of Technology - China
All right reserved for the Author
No part of this script can be copied,
changed without the Authors permission.
If any part of this script used in any documents,
or production, this disclaimer must be displayed with it.
'''
########### create initial variables for sensor#########
sensor_num = 8
sensor_arr=[]
sensor_stat=[]
sensor_range=[]
sensor_id=[1,2,3,4,5,6,7,8]
for i in range(0,sensor_num):
    sensor_stat.append(-1) #set all the sensor to unavailable
    sensor_arr.append(-1)
    sensor_range.append(0)
#########################################################
import serial
import serial.tools.list_ports as port_list
from SerialUltra_p2 import *

ports = list(port_list.comports())
# port = ports[0].device
baudrate = 9600
serialPort = ""
# port = "/dev/ttyUSB0"


port = "/dev/ttyUSB0"


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
            port="/dev/ttyUSB0",
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


connection(port)

#sens1 = SerialUltra(serialPort, 5, 7)
#sens2 = SerialUltra(serialPort, 5, 4)
#sens3 = SerialUltra(serialPort, 5, 2)
#sens4 = SerialUltra(serialPort, 5, 8)
######################################
#********** Open and check sensor port*
counter = 0
print("trying to open sensor")
for i in sensor_id: #go through all the id to check sensor availability
    print(i)
    sensor_arr[counter]=SerialUltra(serialPort,5,i)
    value=sensor_arr[counter].read()
    print(value)
    if value==None:
        sensor_arr[counter]=-1
    print("!!! Sensor ",i, " is not connected !!! ")
    #sensor_arr[counter]=-1
    counter+=1

######################################
#sensor_arr[]=
#print("sensor avalilables=", sensor_arr) # Must be checked later for correct printing
print(sensor_id)
while True:
    #print("777  ",sens1.read())
    #print("444  ",sens2.read())
    #print("222  ",sens3.read())
    #print("888  ",sens4.read())
    for index,sensor in enumerate(sensor_arr):
        #print(sensor)
        if (sensor < 0):
            print ("ddd")
            #os.system(rostopic_pub: std_msgs)
            #print("sensor id{} range: {}".format(sensor_id[index],sensor_arr[2].read()))
        #else:
            #print("Sensor {} unavailable".format(sensor_id[index]))
