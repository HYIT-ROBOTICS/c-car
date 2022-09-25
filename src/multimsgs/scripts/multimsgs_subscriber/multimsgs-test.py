#!/usr/bin/env python

import serial
import rospy
from connectultra import *
from SerialUltra import *
import serial.tools.list_ports as port_list
from multimsgs.msg import Motor_data_type

turn = "00"
deg = "00"


# A 2nd comlement for 32 bithex
def s32(value):
    if value == -1: return 0
    value = int((str("0x") + value),16)
    return -(value & 0X80000000) | (value & 0x7fffffff)

# Create a callback function for the subscriber.
def callback(data):
    global turn, deg
    dr = "01"
    # Simply print out values in our custom message.
    rospy.loginfo(rospy.get_name() + " heard %s %s %s", data.dir, data.sp, data.deg)
    if (data.dir == "forward"): dr = "01"
    if (data.dir == "backward"): dr = "02"
    if (data.dir == "stop"): dr = "03"

    if (deg != int(data.deg)):
       if (int(data.deg) > 0):
           turn = "02"
           deg = str(data.deg)
       else:
           turn = "01"
           deg = str(abs(data.deg))
    deg = str(hex(int(deg)))[2:]
    if (len(deg) <2): deg = "0"+deg

    if (int(data.sp) < 10): ss = "0"+ str(data.sp)
    else: ss = str(data.sp)

    ## Backwheel with Motor Drive
    if (dr == "01"):
    # moving forward
        if (run_forward_drive_motor("01",dr, ss) or run_forward_drive_motor("02",dr, ss)): 
            print ("Forward with", ss, " speed")
	else: print("Error: command is not recieved by robotbase- ","01-", dr,"-", ss)
    elif (dr == "02"):
    # moving backward
        if (run_backward_drive_motor("01", dr, ss) or run_backward_drive_motor("02", dr, ss)): 
            print ("Backward with", ss, " speed")
        else: print("Error: command is not recieved by robotbase- ","02-", dr,"-", ss)
    elif (dr == "03"):
    # stop
        if (run_stop_motor("01", dr, ss) or run_stop_motor("02", dr, ss)): 
            print ("Stopped with", ss, " speed")
        else: print("Error: command is not recieved by robotbase- ","01", dr, ss)
   
    ## Frontwheel with no drive
    if (turn == "01"):
       run_turn_left("0A", turn, deg)
       print ("Left turn with", deg, " degree")
       #str_cmd_turn_left = controller_cmd_str("0A", turn, "00", deg)  # turn left
       #test1.read()  # test write data. If the read succeeds, the read data is returned.
    elif (turn == "02"):
       run_turn_right("0A", turn, deg)
       print ("Right turn with", deg, " degree")
       #str_cmd_turn_right = controller_cmd_str("0A", turn, "00", deg)  # turn right
       #test1.read()  # test write data. If the read succeeds, the read data is returned.

# This ends up being the main while loop.
def listener():
    # Get the ~private namespace parameters from command line or launch file.
    topic = rospy.get_param('~topic', 'chatter')
    # Create a subscriber with appropriate topic, custom message and name of callback function.
    rospy.Subscriber(topic, Motor_data_type, callback)
    # Wait for messages on topic, go to callback function when new messages arrive.
    rospy.spin()

# Main function.
if __name__ == '__main__':
    # Initialize the node and name it.
    rospy.init_node('pylistener', anonymous = True)
    # Go to the main loop.
    listener()
    print
