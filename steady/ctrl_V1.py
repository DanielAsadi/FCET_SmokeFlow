#Daniel Asadi
#Eng Sci 2T3
#FCET Lab, UTIAS

import serial
import time

def controlValve(ser, pos):
    val = input("Valve control: ") #h for high l for low
    ser.write(val.encode())

def controlCam(ser, pos):
        print("flash")

def controlWire(ser, pos):
        print("heat up")

def controlCap(ser, pos):
        print("charge/discharge")

if __name__ == "__main__":
    # make sure the 'COM#' is set according the Windows Device Manager
    ser = serial.Serial('COM5', 115200, timeout=1)
    time.sleep(2)

    for i in range(1000):
        line = ser.readline()   # read a byte
        if line:
            string = line.decode()  # convert the byte string to a unicode string
            try:
                pos = int(string) # convert the unicode string to an int
                print(pos)
                controlValve(ser, pos)
            except ValueError:
                pass        
    ser.close()