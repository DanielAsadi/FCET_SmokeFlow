#Daniel Asadi
#Eng Sci 2T3
#FCET Lab, UTIAS

import serial
import time

def controlValve(ser): #add 2s timer
    ser.write(b'A') #high
    print('VALVE OPEN')
    time.sleep(2) #valve duration
    ser.write(b'B') #low
    print('VALVE CLOSED')

def controlCam(ser): #might have to change
    ser.write(b'C') #high
    time.sleep(0.001)
    ser.write(b'D') #low
    print('CAM RECORD')
    ser.write(b'C') #high
    time.sleep(0.001)
    ser.write(b'D') #low
    print('CAM READY')

def controlWire(ser):
    ser.write(b'E') #high
    print('WIRE ON')
    time.sleep(2) #wire duration
    ser.write(b'F') #low
    print('WIRE OFF')

def controlCap(ser):
    ser.write(b'G') #high
    print('CAP DISCHARGED')
    ser.write(b'H') #low
    print('CAP CHARGING')

def readEnc(loops):
    for i in range(loops):
        line = ser.readline() #read a byte
        if line:
            try:
                string = line.decode() #convert the byte string to a unicode string
                pos = int(string) #convert the unicode string to an int
                print(pos)
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
    ser = serial.Serial('COM7', 115200, timeout=1)
    time.sleep(2)
    status1 = 0
    status2 = 0
    status3 = 0
    status4 = 0
    setting = 5

    print('Initiate Sequence: [1]')
    print('Stop: [0]')

    while True:
        try:
            setting = int(input())
        except ValueError:
                print('ERROR')
        if setting == 1:
            controlValve(ser)
            time.sleep(10) #let liquid settle
            controlCam(ser)
            controlWire(ser)
        elif setting == 0:
            emergencyStop()
        else:
            print('ERROR')