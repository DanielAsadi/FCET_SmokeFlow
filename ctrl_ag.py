# Daniel Asadi
# Eng Sci 2T3
# FCET Lab, UTIAS

import serial
import time
import csv
#import datetime
from threading import Thread
import matplotlib.pyplot as plt
import pandas as pd

def controlValve(ser):
    ser.write(b'A')  # high
    print('VALVE OPEN')
    time.sleep(2)  # valve duration
    ser.write(b'B')  # low
    print('VALVE CLOSED')


def controlCam(ser):
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
    time.sleep(3)  # wire duration - Re 60k: 2s, Re 100k: 1.5s
    ser.write(b'F')  # low
    print('WIRE OFF')


def controlCap(ser):  # not included in circuit yet
    ser.write(b'G')  # high
    print('CAP DISCHARGED')
    time.sleep(1)  # discharging duration
    ser.write(b'H')  # low
    print('CAP CHARGING')


def readEnc(loops, filename, freq, theta):
    # initializng csv values
    start = time.perf_counter()
    iteration = 0
    completed = False
    linelist = []
    t_list = []
    angle_list = []
    iteration_list = []
    voltage = 0
    camDelay = 0.0037046
    delay = 0
    trigT = 0
    period = 1/freq

    # if freq == 0.4:  # experimentally determined values based on ag freq
    #smokeDelay = 0.02
    #delay = period - camDelay - smokeDelay
    # elif freq == 2:
    #smokeDelay = 1.414
    #delay = period - camDelay - smokeDelay

    print('READING AND SAVING DATA...')

    for i in range(loops):
        line = ser2.readline()  # read a byte
        if line:
            try:
                # updating values
                string = line.decode()  # convert the byte string to a unicode string
                linelist = string.split('\t')
                # convert the unicode string to an int
                # print(linelist)
                angle = int(linelist[0])
                if len(linelist) > 1:
                    voltage = float(linelist[1])
                # print(str(angle)+'\t'+str(voltage))

                # if voltage > 4:
                    #t2 = datetime.datetime.utcnow()
                    #timest = t2-t1
                    #print(str(freq)+' Hz:\t'+str(timest))
                    #f = open("camDelay.txt", "a")
                    # f.write(str(freq)+'Hz:\t'+str(timest)+'\n')
                    # f.close()

                iteration += 1
                end = time.perf_counter()
                t = round((end-start), 3)  # update time
                t_list.append(t)
                angle_list.append(angle)
                iteration_list.append(iteration)
                # print(t, angle, iteration)

                # trigger
                # need to set to ahead of actual phase angle of interest because of delay

                if iteration >= 10 and not completed:
                    # time.sleep(delay)
                    controlCam(ser)  # add delay
                    #t1 = datetime.datetime.utcnow()
                    #time1 = datetime.datetime.utcnow()
                    #t1 = Thread(target=controlValve, args=(ser,))
                    # temp continuous mode
                    t2 = Thread(target=controlWire, args=(ser,))
                    # t1.start()
                    t2.start()
                    # t1.join()
                    # t2.join()
                    trigT = t
                    print('Triggered at: '+str(trigT)+' s')
                    #time2 = datetime.datetime.utcnow()
                    #timest = time2-time1
                    #print(str('WIRE DELAY:\t'+str(timest)))
                    completed = True

                if completed and (t > (trigT+5)):
                    break

            except ValueError:
                print('ERROR')
    if not completed:
        print('ERROR, position range not detected')

    print('Finished')  # post-processing
    smokeDelay = float(input('Enter measured smoke delay from PFV4:\n'))
    print('Start of phase: '+str(trigT+camDelay+smokeDelay)+' s')
    create_csv(filename, t_list, angle_list, iteration_list)
    create_plt(filename)


def create_csv(filename, t_list, angle_list, iteration_list):
    iteration = 1
    fieldnames = ["t", "angle", "iteration"]
    filename = filename+'.csv'

    with open(filename, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    # writing to csv
    for (t, angle, iteration) in zip(t_list, angle_list, iteration_list):
        with open(filename, 'a') as csv_file:
            csv_writer = csv.DictWriter(
                csv_file, fieldnames=fieldnames)
            info = {
                "t": t,
                "angle": angle,
                "iteration": iteration
            }
            csv_writer.writerow(info)


def create_plt(filename):  # calculate freq, convert time axis to phase, increase axis tics, fix inital plot values issue
    data = pd.read_csv(filename+'.csv')
    x = data['t']
    y = data['angle']
    plt.xlabel('Time')
    plt.ylabel('Encoder angle')    
    x_plt = []
    if_append = 0
    index_plt = 1
    
    for t in x:
        if if_append:
            x_plt.append(t)
            if_append = 0
            index_plt = 1
        else:
            index_plt += 1
            if index_plt == 10:
                if_append = 1

    plt.xticks(x_plt)
    plt.plot(x, y, linewidth=1)
    plt.tight_layout()
    plt.savefig(filename+'.png')
    plt.show()


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
    freq = 1
    theta = 0

    while True:
        try:
            setting = int(input('Start: [1]\nExit: [0]\n'))
            if setting == 1:
                filename = 'Data/'+str(input('Enter trial name:\n'))
                # freq = float(input('Enter active grid frequency (Hz):\n')) TEMP
                # theta = int(input('Enter encoder trigger angle (°):\n'))
        except ValueError:
            print('ERROR')
            continue
        if setting == 1:
            controlValve(ser)
            print('Letting liquid settle...')
            # time.sleep(10)  # let liquid settle - Re 60k: 15s, Re 100k: 10s
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
                readEnc(2000, filename, freq, theta)
                # save_plt(filename) #save png of chart
                print()
        elif setting == 0:
            emergencyStop(ser)
        else:
            print('ERROR')
