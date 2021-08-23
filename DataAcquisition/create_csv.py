#Daniel Asadi
#Eng Sci 2T3
#FCET Lab, UTIAS

import csv
import time

angle = 0 #global var so it can be changed from a different file
filename = 't1.csv'
start = time.perf_counter()
t = 0
iteration = 1
fieldnames = ["t", "angle", "iteration"]

with open(filename, 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

for i in range(3000):
    loop_start = time.perf_counter()
    end = time.perf_counter()
    t = round((end-start), 3) #update time
    with open(filename, 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        info = {
            "t": 0,
            "angle": 0,
            "iteration": 0
        }
        csv_writer.writerow(info)
        #print(t, angle, iteration)
        iteration+=1
    loop_end = time.perf_counter()
    t2 = round((loop_end-loop_start), 5)
    print(t2)
    #time.sleep(0.001) #need to change
print('done createcsv')