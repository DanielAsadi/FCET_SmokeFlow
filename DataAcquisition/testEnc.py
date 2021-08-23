import serial
import time
from datetime import datetime

ser2 = serial.Serial('COM5', 115200, timeout=0.01)
time.sleep(2)
lst = []

for i in range(1000):
    lstart = datetime.now().timestamp()
    line = ser2.readline()   # read a byte
    print(line)
    if line:
        try:
            # updating values
            s = line.decode()
            # s1 = int(line.decode().strip())  # convert the byte string to a unicode string
            s2 = s.strip('\r\n')
            val = int(s2)
            ser2.reset_input_buffer()
            ser2.reset_output_buffer()
            lend = datetime.now().timestamp()
            lt = lend-lstart
            lst.append(lt)
            #print(val)
        except ValueError:
            print('ERROR')
    else:
        print("fail")
ser2.close()
print('avg:', sum(lst) / len(lst))
