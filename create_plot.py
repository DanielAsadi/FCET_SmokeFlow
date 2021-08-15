#Daniel Asadi
#Eng Sci 2T3
#FCET Lab, UTIAS

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from itertools import count

filename = 'Data/1671'

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

    x_angle = []

    frequency_Hz = get_frequency_from_interpolation(filename)
    frequency_rad = 360 * frequency_Hz

    for t in x:

        t_angle = t * frequency_rad
        x_angle.append(t_angle)

    for t_angle in x_angle:
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
    plt.plot(x_angle, y, linewidth=1)
    fig = plt.gcf()
    fig.set_size_inches(6.4, 3.6)
    plt.savefig(filename+'phase.png', dpi=300)
    plt.show()

def get_frequency_from_interpolation(filename):
    data = pd.read_csv(filename+'.csv')
    x = data['t']
    y = data['angle']
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
    print('The frequency is', freq, 'Hz')
    return freq

if __name__ == "__main__":
    create_plt(filename)