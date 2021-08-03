#Daniel Asadi
#Eng Sci 2T3
#FCET Lab, UTIAS

import csv
import time

def create_csv(filename):
    t = 0 #add live timing
    angle = 0
    iteration = 1
    filename = 'data.csv' #add prompt to name file

    fieldnames = ["Time", "angle", "Iteration"]

    with open(filename, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    while True:

        with open(filename, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            info = {
                "Time": t,
                "angle": angle,
                "Iteration": iteration
            }

            csv_writer.writerow(info)
            #print(t, angle, iteration)

        time.sleep(1) #need to change