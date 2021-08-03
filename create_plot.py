#Daniel Asadi
#Eng Sci 2T3
#FCET Lab, UTIAS

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from itertools import count

plt.style.use('fivethirtyeight')

index = count()

def animate(i):
    data = pd.read_csv('data.csv')
    x = data['t']
    y = data['angle']
    plt.cla()
    plt.plot(x, y)

ani = FuncAnimation(plt.gcf(), animate, interval=1)

plt.tight_layout()
plt.show()