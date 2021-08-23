# Daniel Asadi
# Eng Sci 2T3
# FCET Lab, UTIAS

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

filename = 'Data/1672/1672'


def create_plt(filename):  # convert time axis to phase
    data = pd.read_csv(filename+'.csv')
    plt.rcParams['font.size'] = '4'
    x = data['t']
    y = data['angle']
    plt.xlabel('Phase angle [deg]')
    plt.ylabel('Encoder angle [deg]')

    x_angle = []

    frequency_Hz = get_frequency_from_interpolation(filename)
    frequency_rad = 360 * frequency_Hz

    for i in range(len(x)):
        t = x[i]
        angle = y[i]
        if angle == min(y):
            phaseShift = 360 - t * frequency_rad
            break

    for t in x:
        t_angle = t * frequency_rad + phaseShift
        x_angle.append(t_angle)

    plt.xticks(np.arange(0, max(x_angle)+1, 360))
    plt.xticks(rotation=60)
    plt.plot(x_angle, y, linewidth=1)
    fig = plt.gcf()
    fig.set_size_inches(6.4, 3.6)
    plt.savefig(filename+'phase.png', dpi=300)
    plt.show()


def get_frequency_from_interpolation(filename):
    data = pd.read_csv(filename+'.csv')
    x = data['t']
    y = data['angle']
    choose_angle = y[0] - 1
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
    print('The frequency is', freq, 'Hz')
    return freq


if __name__ == "__main__":
    create_plt(filename)
