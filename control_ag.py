#Daniel Asadi
#Eng Sci 2T3
#FCET Lab, UTIAS

import serial
import time
#Experimentally determine delays and order, might have to do threading for delays to not interrupt other processes
#If multiple inputs need to be turned on at same time adjust ser.write letter to same letter

def controlValve(ser): #add 2s timer
    ser.write(b'A') #high
    print('VALVE OPEN')
    time.sleep(2) #valve duration
    ser.write(b'B') #low
    print('VALVE CLOSED')

def controlCam(ser): #might have to change
    ser.write(b'C') #high
    time.sleep(0.1)
    ser.write(b'D') #low
    print('CAM RECORD')
    time.sleep(0.1)
    ser.write(b'C') #high
    time.sleep(0.1)
    ser.write(b'D') #low
    print('CAM READY')

def controlWire(ser):
    ser.write(b'E') #high
    print('WIRE ON')
    time.sleep(2) #wire duration - Re 60k: 2s, Re 100k: 1.5s
    ser.write(b'F') #low
    print('WIRE OFF')

def controlCap(ser): #not included in circuit yet
    ser.write(b'G') #high
    print('CAP DISCHARGED')
    time.sleep(1) #discharging duration
    ser.write(b'H') #low
    print('CAP CHARGING')

def readEnc(loops):
    for i in range(loops):
        line = ser2.readline() #read a byte
        if line:
            try:
                string = line.decode() #convert the byte string to a unicode string
                pos = int(string) #convert the unicode string to an int
                print(pos)
                if 0<=pos<=500: #need to set to ahead of actual phase angle of interest because of delay
                    controlCam(ser)
                    controlWire(ser) #smoke deployed
                    print('Finished')
                    break               
            except ValueError:
                print('ERROR')
        if i == loops-1:
            print('ERROR, position range not detected')

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
    ser2 = serial.Serial('COM5', 115200, timeout=1)
    time.sleep(2)
    setting = 5

    while True:
        try:
            setting = int(input('Start: [1]\nExit: [0]\n'))
        except ValueError:
                print('ERROR')
                continue
        if setting == 1:
            controlValve(ser)
            print('Letting liquid settle...')
            time.sleep(10) #let liquid settle - Re 60k: 15s, Re 100k: 10s
            try:
                setting = int(input('Continue: [1]\nRetry bead formation: [2]\n')) #retry dispensing liquid
            except ValueError:
                print('ERROR')
                continue
            if setting == 2:
                continue
            else:
                readEnc(1000)               
                print()
        elif setting == 0:
            emergencyStop()
        else:
            print('ERROR')