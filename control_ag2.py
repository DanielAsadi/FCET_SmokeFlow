# Daniel Asadi
# Eng Sci 2T3
# FCET Lab, UTIAS
# test putting funcs in eachother

import serial
import time
import csv

filename = 't1.csv'

# Experimentally determine delays and order, might have to do threading for delays to not interrupt other processes
# If multiple inputs need to be turned on at same time adjust ser.write letter to same letter


def controlValve(ser):  # add 2s timer
    ser.write(b'A')  # high
    print('VALVE OPEN')
    time.sleep(2)  # valve duration
    ser.write(b'B')  # low
    print('VALVE CLOSED')


def controlCam(ser):  # might have to change
    ser.write(b'C')  # high
    time.sleep(0.1)
    ser.write(b'D')  # low
    print('CAM RECORD')
    time.sleep(0.1)
    ser.write(b'C')  # high
    time.sleep(0.1)
    ser.write(b'D')  # low
    print('CAM READY')

    # measuring cam delay
    camStart = time.perf_counter()

    while True:
        line = ser2.readline()  # read a byte
        if line:
            try:
                # updating values
                string = line.decode()  # convert the byte string to a unicode string
                linelist = string.split('\t')
                # convert the unicode string to an int
                voltage = float(linelist[1])

                if voltage > 4:
                    arduinoDelay = linelist[2]
                    camEnd = time.perf_counter()
                    camDelay = round((camEnd-camStart), 5)
                    print('CAM DELAY:'+str(camDelay))
                    print('ARDUINO CAM DELAY:'+str(arduinoDelay))
                    completed = False
                    break
            except ValueError:
                print('ERROR')


def controlWire(ser):
    ser.write(b'E')  # high
    print('WIRE ON')
    time.sleep(2)  # wire duration - Re 60k: 2s, Re 100k: 1.5s
    ser.write(b'F')  # low
    print('WIRE OFF')


def controlCap(ser):  # not included in circuit yet
    ser.write(b'G')  # high
    print('CAP DISCHARGED')
    time.sleep(1)  # discharging duration
    ser.write(b'H')  # low
    print('CAP CHARGING')


def readEnc(loops, filename):
    # initializng csv values
    start = time.perf_counter()
    iteration = 0
    fieldnames = ["t", "angle", "iteration"]
    completed = False
    status = 0
    linelist = []
    #filename = filename +'.csv'

    # writing csv headers commented out for thread.py
    # with open(filename, 'w') as csv_file: #move to thread.py
    #csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    # csv_writer.writeheader() #add ability to write to specific data folder
    print('READING AND SAVING DATA...')

    for i in range(loops):
        line = ser2.readline()  # read a byte
        if line:
            try:
                # updating values
                string = line.decode()  # convert the byte string to a unicode string
                linelist = string.split('\t')
                # convert the unicode string to an int
                angle = int(linelist[0])
                voltage = float(linelist[1])
                # print(str(angle)+'\t'+str(voltage))

                end = time.perf_counter()
                t = round((end-start), 3)  # update time
                iteration += 1

                if t > 5:
                    status = 1
                # writing to csv
                with open(filename, 'a') as csv_file:
                    csv_writer = csv.DictWriter(
                        csv_file, fieldnames=fieldnames)
                    info = {
                        "t": t,
                        "angle": angle,
                        "iteration": iteration
                    }
                    csv_writer.writerow(info)
                    #print(t, angle, iteration)
                    # time.sleep(0.001) #need to change

                # trigger
                # need to set to ahead of actual phase angle of interest because of delay
                if angle >= 0 and status == 1:
                    controlCam(ser)
                    controlWire(ser)  # smoke deployed
                    print('Finished')
                    completed = True
                    break
            except ValueError:
                print('ERROR')
    if not completed:
        print('ERROR, position range not detected')


def emergencyStop(ser):
    ser.write(b'B')  # low
    print('VALVE CLOSED')
    ser.write(b'D')  # low
    print('CAM OFF')
    ser.write(b'F')  # low
    print('WIRE OFF')
    ser.write(b'H')  # low
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
            #filename = str(input('Enter trial name:\n'))
            setting = int(input('Start: [1]\nExit: [0]\n'))
        except ValueError:
            print('ERROR')
            continue
        if setting == 1:
            controlValve(ser)
            print('Letting liquid settle...')
            time.sleep(10)  # let liquid settle - Re 60k: 15s, Re 100k: 10s
            try:
                # retry dispensing liquid
                setting = int(
                    input('Continue: [1]\nRetry bead formation: [2]\n'))
            except ValueError:
                print('ERROR')
                continue
            if setting == 2:
                continue
            else:
                readEnc(1000, filename)  # run sequence, max 1000 iterations
                # save_plt(filename) #save png of chart
                print()
        elif setting == 0:
            emergencyStop(ser)
        else:
            print('ERROR')
