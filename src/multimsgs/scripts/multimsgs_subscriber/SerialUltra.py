import serial
import time


class SerialUltra:
    #serialPort = ""

    def __init__(self, con):
        self.serialPort = con
        #self.serialPort=serial.Serial(con)
        print("Serial connection object created ...",self.serialPort)
        return

    def write(self, sendstr):
        print("Recieved for serial communication - ",sendstr, " to send to ",self.serialPort)
        while True:
            try:
                self.serialPort.write(sendstr)
                time.sleep(0.1)
                print("sending data succeeded!")
                return True
            except serial.serialutil.SerialException:
                print(self.serialPort, "   Connection is not available")
        return 0

    def read(self):
        while True:
            try:
                data = self.serialPort.readline()
                time.sleep(0.1)
                print(data)
                return data
            except serial.serialutil.SerialException:
                print(self.serialPort, "   Connection is not available")
        return 0
