#Daniel Asadi
#Eng Sci 2T3
#FCET Lab, UTIAS

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from itertools import count

filename = 't1.csv'

print('create_plot running')
plt.style.use('fivethirtyeight')
index = count()

def animate(i):
    data = pd.read_csv(filename)
    x = data['t']
    y = data['angle']
    plt.cla()
    plt.plot(x, y, linewidth=1)
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate, interval=1)

plt.tight_layout()
plt.show()