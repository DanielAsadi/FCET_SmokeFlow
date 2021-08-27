# Daniel Asadi
# Eng Sci 2T3
# FCET Lab, UTIAS

import serial
import time
import csv
from datetime import datetime
from threading import Thread
import matplotlib.pyplot as plt
import pandas as pd
import math
import subprocess
import os

# EDIT FOLLOWING VARIABLES BEFORE RUNNING
matlab_freq = 0.178588
caseNo = '1790'
extraInfoFilename = ''
filename = 'data/'+caseNo+'/'+caseNo+extraInfoFilename
valveDuration = 2
wireDuration = 2
p = 0  # phase angle trigger 0, 45, 90, 135, 180, 225, 270, 315


def controlValve(ser):
    ser.write(b'A')  # high
    print('VALVE OPEN')
    time.sleep(valveDuration)  # valve duration
    ser.write(b'B')  # low
    print('VALVE CLOSED')


def controlCam(ser, syncDelay):
    time.sleep(syncDelay)
    ser.write(b'C')  # high
    time.sleep(0.1)
    ser.write(b'D')  # low
    print('CAM RECORD')
    time.sleep(0.1)
    ser.write(b'C')  # high
    time.sleep(0.1)
    ser.write(b'D')  # low
    print('CAM READY')


def controlWire(ser, syncDelay):
    time.sleep(syncDelay-1)  # optional for low freq cases
    ser.write(b'E')  # high
    print('WIRE ON')
    time.sleep(wireDuration)  # wire duration
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
    count = 0
    frequency_rad = 0
    phaseShift = 0

    p = 1/freq
    cDelay = 0.2  # cam trigger delay
    recDelay = cDelay  # can add delay here
    NcycDelay = math.ceil(recDelay/p)
    syncDelay = NcycDelay*p-cDelay  # delay to sync trigger at 0 deg

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
                # 360, 405, 450, 495, 540, 585, 630, 675, 720

                if 0 <= angle <= 1 and count == 0:
                    count += 1
                    frequency_rad = 360 * freq
                    phaseShift = 360 - t * frequency_rad

                phase_angle = round((t * frequency_rad + phaseShift), 5)

                if round(phase_angle) % 360 == p and not completed and i >= 400:  # trigger
                    t1 = Thread(target=controlCam, args=(ser, syncDelay,))
                    t2 = Thread(target=controlWire, args=(ser, syncDelay,))
                    t1.start()
                    t2.start()
                    trigT = t + NcycDelay * p - cDelay + 0.2
                    print('Cam triggered at: '+str(trigT)+' s')
                    completed = True

                if completed and (t > (trigT+8)):
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
        emergencyStop(ser)


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
    plt.xlabel('Time [s]')
    plt.ylabel('Encoder angle [deg]')
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
    f = open(filename+'.txt', 'w')
    f.write('Measured frequency: '+str(freq) +
            ' Hz vs matlab '+str(matlab_freq)+' Hz\n')
    f.write('Trigger start at 0 deg: '+str(trigT)+' s\n')
    f.close()


def get_frequency_from_interpolation():
    while True:
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

        choose_angle = y[0] - 1
        rising_midpoints = []
        decimal_places = 5
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
        try:
            freq = round(1 / delta_t_avg, decimal_places)
            return freq
        except:
            print('Frequency calculation error. Recalculating...')


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
    ser2.close()
    quit()


if __name__ == "__main__":
    parentDir = str(os.path.dirname(__file__)).replace('/unsteady', '/data')
    if not os.path.isdir(parentDir+'/'+caseNo):
        os.mkdir(os.path.join(parentDir, caseNo))

    while True:
        try:
            # make sure the 'COM#' is set according the Windows Device Manager
            ser = serial.Serial('COM4', 115200, timeout=1)
            ser2 = serial.Serial('COM10', 115200, timeout=0.01)
            break
        except:
            print('Serial port error. Reconecting...')
        time.sleep(2)

    print('Serial ports connected')
    setting = 5

    while True:
        try:
            freq = get_frequency_from_interpolation()
            print('The frequency is', freq, 'Hz')
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
                readEnc(2000, filename, freq)
                while True:
                    try:
                        t1 = Thread(target=subprocess.run, args=(
                            ["python", "dataAcquisition/create_plot_phase.py"],))
                        t1.start()
                        print()
                    except:
                        print('Frequency calculation error. Recalculating...')
        elif setting == 0:
            emergencyStop(ser)
        else:
            print('ERROR')
