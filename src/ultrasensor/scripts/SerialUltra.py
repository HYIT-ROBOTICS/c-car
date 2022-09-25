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

import serial
import time


class SerialUltra:
    last = 0
    serialPort = ""
    tr = 0
    id = 0

    def __init__(self, con, t, i):
        self.serialPort = con
        self.tr = t
        self.id = i
        print("Object ", self.id, " is created")
        return

    def read1(self, sendstr):
        raw_data = 0
        line = {}
        i = 1
        l = 0
        try:
            d = bytes.fromhex(sendstr)
            self.serialPort.write(d)
            time.sleep(0.01)
            data = self.serialPort.readline()
            print("data length:",len(data), "   Data:",data)
            if len(data) <10 or len(data) > 30:
                #print ("No Data")
                return None
            if data:
                line1 = data[4] * 0x100 + data[5]
                raw_data = line1
                self.tr = int(self.tr * line1 / 100)
                
                return int(raw_data+30)
                '''
                while i > 0 and i < 2:
                    self.serialPort.write(d)
                    time.sleep(0.2)
                    line[i] = data[4] * 0x100 + data[5]
                    if (abs(line[1] - line[i]) < self.tr):
                        #print (i," : ", line[i])
                        l = l + line[i]
                        i += 1
                return int((l + line1) / 3)
                '''
            else:
                #print("no data")
                return None
                
        except serial.serialutil.SerialException:
            print(self.serialPort, "   Connection is not available")
            return None

    def read_sensor_1(self):
        return self.read1('7F 01 12 00 00 00 00 00 03 16')
        

    def read_sensor_2(self):
        return self.read1('7F 02 12 00 00 00 00 00 03 17')

    def read_sensor_3(self):
        return self.read1('7F 03 12 00 00 00 00 00 03 18')

    def read_sensor_4(self):
        return self.read1('7F 04 12 00 00 00 00 00 03 19')

    def read_sensor_5(self):
        return self.read1('7F 05 12 00 00 00 00 00 03 1A')

    def read_sensor_6(self):
        return self.read1('7F 06 12 00 00 00 00 00 03 1B')

    def read_sensor_7(self):
        return self.read1('7F 07 12 00 00 00 00 00 03 1C')

    def read_sensor_8(self):
        return self.read1('7F 08 12 00 00 00 00 00 03 1D')

    def read(self):
        num=self.id
        if num == 1:
            return self.read_sensor_1()
        if num == 2:
            return self.read_sensor_2()
        if num == 3:
            return self.read_sensor_3()
        if num == 4:
            return self.read_sensor_4()
        if num == 5:
            return self.read_sensor_5()
        if num == 6:
            return self.read_sensor_6()
        if num == 7:
            return self.read_sensor_7()
        if num == 8:
            return self.read_sensor_8()
