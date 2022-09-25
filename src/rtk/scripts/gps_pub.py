#import rospy
import serial
import time
from socket import timeout
from std_msgs.msg import String

msg = String()


if __name__ == "__main__":
    '''
    rospy.init_node("gps_p");
    pub = rospy.Publisher("rtk", String, queue_size=10)
    msg = String()
    rate = rospy.Rate(7)
    '''
    ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
    print("received: ",ser)
    while True:
        line = str(str(ser.readline())[2:])
        #print("line: ",line)
        #print("four chars: ", line[:2])
        if(line[:4] == ('NGGA')):
            line = line.split(",", 14)
            #print("filtered: ",line)
            msg.data = str(line[2][:2])+"d"+str(line[2][2:4])+"m"+str(float(line[2][4:])*60)+"s N\n"+str(line[4][:2])+"d"+str(line[4][2:4])+"m"+str(float(line[4][4:])*60)+"s E"
            print("message: ",msg.data)
            #pub.publish(msg)
            #rate.sleep()
    ser.close()
        

