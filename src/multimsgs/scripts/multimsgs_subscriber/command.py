from crc16 import *
import binascii
from binascii import unhexlify


def toBytes(str):
    d = unhexlify(str.replace(" ",""))
    return d

def controller_cmd_str(dev_id, cmd, phb, plb):
    str = "01 02"
    str = str + dev_id + cmd + phb + plb
    crc = crc16(str)
    str = str + crc
    print ("cmd_str successfully created", str)
    return str


def power_controller_command(cmd, phb, plb):
    str = "04 02"
    str = str + cmd + phb + plb
    return str


def query_command(dev_id):
    str = "03 00 34 00 01"
    str = dev_id + str
    return str


if __name__ == '__main__':
    str1 = controller_cmd_str("01", "01", "00", "05")  # left drive motor  motor forward rotation  speed 5
    str2 = controller_cmd_str("02", "01", "00", "05")  # right drive motor  motor forward rotation  speed 5
    print(str1)
    print(str2)

