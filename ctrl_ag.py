# Daniel Asadi
# Eng Sci 2T3
# FCET Lab, UTIAS

from numpy import mat
import serial
import time
import csv
from datetime import datetime
from threading import Thread
import matplotlib.pyplot as plt
import pandas as pd
import math

# add function to calculate f before

matlab_freq = 4.796
filename = 'Data/1677'


def controlValve(ser):
    ser.write(b'A')  # high
    print('VALVE OPEN')
    time.sleep(2)  # valve duration
    ser.write(b'B')  # low
    print('VALVE CLOSED')


def controlCam(ser, camDelay):
    time.sleep(camDelay)
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


def readEnc(loops, filename, freq):
    completed = False
    t_list = []
    angle_list = []
    iteration_list = []
    trigT = 0

    p = 1/freq
    cDelay = 0.2  # cam trigger delay
    recDelay = cDelay + 0.5
    NcycDelay = math.ceil(recDelay/p)
    camDelay = NcycDelay*p-cDelay

    print('READING AND SAVING DATA...')
    start = datetime.now().timestamp()

    for i in range(loops):
        line = ser2.readline()  # read a byte
        if line:
            try:
                # updating values
                s = line.decode()  # convert the byte string to a unicode string
                s2 = s.strip('\r\n')
                angle = int(s2)
                ser2.reset_input_buffer()
                ser2.reset_output_buffer()

                i += 1
                end = datetime.now().timestamp()
                t = round(end-start, 5)  # update time
                t_list.append(t)
                angle_list.append(angle)
                iteration_list.append(i)

                if 0 <= angle <= 1 and not completed and i >= 500:  # trigger
                    t1 = Thread(target=controlCam, args=(ser, camDelay,))
                    t2 = Thread(target=controlWire, args=(ser,))
                    t1.start()
                    t2.start()
                    trigT = t + NcycDelay * p - cDelay + 0.2
                    print('Cam triggered at: '+str(trigT)+' s')
                    completed = True

                if completed and (t > (trigT+5)):
                    break
            except ValueError:
                print('ERROR')

    if not completed:
        print('ERROR, position range not detected')

    print('Finished')  # post-processing

    while True:
        try:
            print()
            setting = int(input('Continue: [1]\nRetry: [2]\n'))
            break
        except ValueError:
            print('ERROR')
    if setting == 1:
        testFrame = float(
            input('Enter time for frame of interest to test accuracy from PFV4:\n'))
        phaseTestStart = trigT + testFrame
        print('Start of phase:', trigT, 's')
        print('Start of test phase of interest:', phaseTestStart, 's')

        create_csv(filename, t_list, angle_list, iteration_list)
        create_plt(filename)
        create_txt(filename, trigT, freq)
        print()


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


def create_plt(filename):  # convert time axis to phase
    data = pd.read_csv(filename+'.csv')
    plt.rcParams['font.size'] = '4'
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
            if index_plt == 20:
                if_append = 1

    plt.xticks(rotation=60)
    plt.xticks(x_plt)
    plt.plot(x, y, linewidth=1)
    fig = plt.gcf()
    fig.set_size_inches(6.4, 3.6)
    plt.savefig(filename+'.png', dpi=300)
    plt.show()


def create_txt(filename, trigT, freq):
    f = open(filename+'Info.txt', 'w')
    f.write('Measured frequency: '+str(freq)+' Hz vs matlab '+str(f)+' Hz\n')
    f.write('Trigger start at 0 deg: '+str(trigT)+' s\n')
    f.close()


def get_frequency_from_interpolation():
    print('Acquiring frequency...')
    x = []
    y = []
    start = datetime.now().timestamp()

    while True:
        line = ser2.readline()  # read a byte
        if line:
            try:
                # updating values
                s = line.decode()  # convert the byte string to a unicode string
                s2 = s.strip('\r\n')
                angle = int(s2)
                ser2.reset_input_buffer()
                ser2.reset_output_buffer()

                end = datetime.now().timestamp()
                t = round(end-start, 5)  # update time
                x.append(t)
                y.append(angle)

                if t > 10:
                    break
            except ValueError:
                print('ERROR')

    choose_angle = 45
    rising_midpoints = []
    decimal_places = 3
    delta_t_avg = 0
    buffer = 1  # 1 or 2

    for index_freq in range(0, len(y) - buffer):

        if y[index_freq] < choose_angle < y[index_freq + buffer]:

            m = (y[index_freq + buffer] - y[index_freq]) / \
                (x[index_freq + buffer] - x[index_freq])
            b = y[index_freq + buffer] - m * x[index_freq + buffer]
            rising_midpoints.append(
                round((choose_angle - b) / m, decimal_places))

        elif y[index_freq + buffer] == choose_angle and y[index_freq] < choose_angle:

            rising_midpoints.append(
                round(x[index_freq + buffer], decimal_places))

    for index_freq in range(0, len(rising_midpoints) - 1):

        delta_t_avg += (rising_midpoints[index_freq + 1] -
                        rising_midpoints[index_freq]) / (len(rising_midpoints) - 1)

    freq = round(1 / delta_t_avg, decimal_places)
    return freq


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
    ser2 = serial.Serial('COM5', 115200, timeout=0.01)
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
                freq = get_frequency_from_interpolation()
                print('The frequency is', freq, 'Hz')
                readEnc(2000, filename, freq)
                print()
        elif setting == 0:
            emergencyStop(ser)
        else:
            print('ERROR')
