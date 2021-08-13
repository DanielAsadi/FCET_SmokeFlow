import pandas as pd

def get_frequency_from_interpolation(filename):
    
    data = pd.read_csv(filename)
    x = data['t']
    y = data['angle']
    choose_angle = 45
    rising_midpoints = []
    decimal_places = 3
    delta_t_avg = 0

    for index_freq in range(0, len(y) - 2):

        if y[index_freq] < choose_angle < y[index_freq + 2]:

            m = (y[index_freq + 2] - y[index_freq]) / (x[index_freq + 2] - x[index_freq])
            b = y[index_freq + 2] - m * x[index_freq + 2]
            rising_midpoints.append(round((choose_angle - b) / m, decimal_places))

        elif y[index_freq + 2] == choose_angle and y[index_freq] < choose_angle:

            rising_midpoints.append(round(x[index_freq + 2], decimal_places))

    for index_freq in range(0, len(rising_midpoints) - 1):

        delta_t_avg += (rising_midpoints[index_freq + 1] - rising_midpoints[index_freq]) / (len(rising_midpoints) - 1)

    print("The frequency is", round(1 / delta_t_avg, decimal_places), "Hz")

if __name__ == "__main__":
    get_frequency_from_interpolation('Data/test.csv')