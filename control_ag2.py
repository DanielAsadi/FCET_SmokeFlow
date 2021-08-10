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


def readEnc(loops, filename, period, theta):
    # initializng csv values
    start = time.perf_counter()
    iteration = 0
    fieldnames = ["t", "angle", "iteration"]
    completed = False
    linelist = []
    camStart = 0
    camEnd = 0
    camDelay = 0
    voltage = 0
    v = False
    offset = 0
    if period == 2.5:
        offset = 17
    #filename = filename +'.csv'

    # writing csv headers commented out for thread.py
    # with open(filename, 'w') as csv_file: #move to thread.py
    #csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    # csv_writer.writeheader() #add ability to write to specific data folder
    print('READING AND SAVING DATA...')

    for i in range(loops):
        loop_start = time.perf_counter()
        line = ser2.readline()  # read a byte
        if line:
            try:
                # updating values
                string = line.decode()  # convert the byte string to a unicode string
                linelist = string.split('\t')
                # convert the unicode string to an int
                #print(linelist)
                angle = int(linelist[0])
                if len(linelist)>1:
                    voltage = float(linelist[1])
                #print(str(angle)+'\t'+str(voltage))

                loop_end = time.perf_counter()
                t2 = round((loop_end-loop_start), 5)
                #print(t2)

                if voltage > 4:
                    #camEnd = time.perf_counter()
                    #camDelay = round((camEnd-camStart), 5)
                    #print('CAM DELAY:'+str(camDelay))
                    #break
                    v = True
                
                iteration += 1
                end = time.perf_counter()
                t = round((end-start), 3)  # update time

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
                # print(t, angle, iteration)

                if v:
                    break

                # trigger
                # need to set to ahead of actual phase angle of interest because of delay
                if angle == theta and t > 2 and not completed:
                    controlCam(ser) # add delay
                    camStart = time.perf_counter()
                    wireStart = time.perf_counter()
                    controlWire(ser)  # smoke deployed
                    wireEnd = time.perf_counter()
                    t3 = round((wireEnd-wireStart), 3)  # update time
                    print('Finished') # now need to measure time delay of smoke
                    completed = True
                    #break
            except ValueError:
                print('ERROR')
        #time.sleep(0.01) #need to change
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
            if setting == 1:
                freq = int(input('Enter active grid frequency (Hz):\n'))
                theta = int(input('Enter encoder trigger angle (°):\n'))
                period = 1/freq
        except ValueError:
            print('ERROR')
            continue
        if setting == 1:
            controlValve(ser)
            print('Letting liquid settle...')
            #time.sleep(10)  # let liquid settle - Re 60k: 15s, Re 100k: 10s
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
                # run sequence, max 1000 iterations
                readEnc(2000, filename, period, theta)
                # save_plt(filename) #save png of chart
                print()
        elif setting == 0:
            emergencyStop(ser)
        else:
            print('ERROR')
