import serial
import serial.tools.list_ports as port_list
from SerialUltra import *
import binascii
from binascii import unhexlify
from command import *


maintenance = True
ports = list(port_list.comports())
baudrate = 9600
serialPort = "/dev/ttyUSB0"
port = "/dev/ttyUSB0"

# port = 'COM5'


def connection485(po):
    global serialPort
    try:
        serialPort = serial.Serial(port=po, baudrate=baudrate, bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE)
        print("Serial Port is opened as:", po)
        return 1
    except:
        return 0


connection485(port)
test1 = SerialUltra(serialPort)

'''
def run_left_drive_motor(m,dr,ss):
    str_cmd_left_drive = controller_cmd_str(m, dr, "00", ss)  # left drive motor  motor forward rotation  speed 5
    d = unhexlify(str_cmd_left_drive.replace(" ",""))
    print("variable d is formed as: ",d)
    test1.write(d)  # test send data. Returns true if the message was sent successfully
    if (not maintenance): test1.read()  # test write data. If the read succeeds, the read data is returned.
    else: return True
'''
def run_forward_drive_motor(m,dr,ss):
    str_cmd_left_drive = controller_cmd_str(m, dr, "00", ss)  # left drive motor 
    str_cmd_right_drive = controller_cmd_str(m, dr, "00", ss)  # right drive motor
    ##how do you unhexlify str_cmd_right_drive
    d = unhexlify(str_cmd_left_drive.replace(" ",""))
    print("variable d is formed as: ",d)
    test1.write(d)  # test send data. Returns true if the message was sent successfully
    if (not maintenance): test1.read()  # test write data. If the read succeeds, the read data is returned.
    else: return True

def run_backward_drive_motor(m,dr,ss):
    str_cmd_left_drive_back = controller_cmd_str(m, dr, "00", ss)  # left drive motor
    str_cmd_right_drive_back = controller_cmd_str(m, dr, "00", ss)
    ##how do you unhexlify str_cmd_right_drive
    d = unhexlify(str_cmd_left_drive_back.replace(" ",""))
    print("variable d is formed as: ",d)
    test1.write(d)  # test send data. Returns true if the message was sent successfully
    if (not maintenance): test1.read()  # test write data. If the read succeeds, the read data is returned.
    else: return True

def run_stop_motor(m,dr,ss):
    str_cmd_left_drive_stop = controller_cmd_str(m, dr, "00", ss)  # stop motor
    str_cmd_right_drive_stop = controller_cmd_str(m, dr, "00", ss)  # stop motor | speed 0
    ##how do you unhexlify str_cmd_right_drive
    d = unhexlify(str_cmd_left_drive_stop.replace(" ",""))
    test1.write(d)  # test send data. Returns true if the message was sent successfully
    if (not maintenance): test1.read()  # test write data. If the read succeeds, the read data is returned.
    else: return True

def run_turn_left(m,turn,deg):
    str_cmd_turn_left = controller_cmd_str("0A", turn, "00", deg)  # turn left
    #d = bytes.fromhex(str_cmd_turn_left)
    d = unhexlify(str_cmd_turn_left.replace(" ",""))
    test1.write(d)  # test send data. Returns true if the message was sent successfully
    if (not maintenance): test1.read()  # test write data. If the read succeeds, the read data is returned.
    else: return True

def run_turn_right(m,turn,deg):
    str_cmd_turn_right = controller_cmd_str("0A", turn, "00", deg)  # turn right
    #d = bytes.fromhex(str_cmd_turn_right)
    d = unhexlify(str_cmd_turn_right.replace(" ",""))
    test1.write(d)  # test send data. Returns true if the message was sent successfully
    if (not maintenance): test1.read()  # test write data. If the read succeeds, the read data is returned.
    else: return True
