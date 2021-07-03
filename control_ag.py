#Daniel Asadi
#Eng Sci 2T3
#FCET Lab, UTIAS

import serial
import time
#Experimentally determine delays and order, might have to do threading for delays to not interrupt other processes
#If multiple inputs need to be turned on at same time adjust ser.write letter to same letter

def controlValve(ser):
        ser.write(b'A') #high
        print('VALVE OPEN')
        time.sleep(1)
        ser.write(b'B') #low
        print('VALVE CLOSED')

def controlCam(ser):
        ser.write(b'C') #high
        print('CAM ON')
        time.sleep(1)
        ser.write(b'D') #low
        print('CAM OFF')

def controlWire(ser):
        ser.write(b'E') #high
        print('WIRE ON')
        time.sleep(1)
        ser.write(b'F') #low
        print('WIRE OFF')

def controlCap(ser):
        ser.write(b'G') #high
        print('CAP DISCHARGED')
        time.sleep(1)
        ser.write(b'H') #low
        print('CAP CHARGING')

def activateSequence(pos): 
    if 0<pos<1000: 
        controlValve(ser)
        controlCam(ser)
        controlWire(ser)
        controlCap(ser)

def readEnc(loops):
    for i in range(loops):
        line = ser.readline() #read a byte
        if line:
            try:
                string = line.decode() #convert the byte string to a unicode string
                pos = int(string) #convert the unicode string to an int
                print(pos)
                activateSequence(pos)
            except ValueError:
                print('ERROR')
    ser.close()

def emergencyStop():
    ser.write(b'B') #low
    print('VALVE CLOSED')
    ser.write(b'D') #low
    print('CAM OFF')
    ser.write(b'F') #low
    print('WIRE OFF')
    ser.write(b'H') #low
    print('CAP CHARGING')
    ser.close()
    quit()

if __name__ == "__main__":
    # make sure the 'COM#' is set according the Windows Device Manager
    ser = serial.Serial('COM6', 115200, timeout=1)
    time.sleep(2)
    readEnc(1000)