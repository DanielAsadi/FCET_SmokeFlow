#import serial
#import time
#import create_plot
#import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation
#import pandas as pd
#from itertools import count
import csv
from threading import Thread
import subprocess

filename = 't1.csv'
fieldnames = ["t", "angle", "iteration"]
#filename = str(input('Enter trial name:\n'))
#filename = set_filename()

#writing csv headers
with open(filename, 'w') as csv_file: #move to thread.py
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader() #add ability to write to specific data folder

t1 = Thread(target=subprocess.run, args=([ "python", "control_ag2.py"],))
t2 = Thread(target=subprocess.run, args=([ "python", "create_plot.py"],))

t1.start()
t2.start()
t1.join()
t2.join()