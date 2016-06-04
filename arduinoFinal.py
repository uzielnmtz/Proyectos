#!/usr/bin/env python
#Practica Final
#Codigo con 2 termistores y un sensor

import time
import warnings
import numpy as np
import matplotlib.pyplot as plt
import serial
from collections import deque
from optparse import OptionParser


parser = OptionParser()
parser.add_option('-f','--file',dest = "fname", help = 'Data file',metavar='FILE')
(options,args) = parser.parse_args()



N = 200
temp = deque([0]*N,maxlen = N)
term1 = deque([0] * N, maxlen=N)  # deque con longitud maxima N


#Creamos la figura
plt.ion()
fig, (axt,ax1)= plt.subplots(1,2)
axt.set_title('Temperatura[C]')
ax1.set_title('Termistor 1')
tti, = axt.plot(temp)
ll, = ax1.plot(term1)


arduino = serial.Serial('/dev/ttyACM0',baudrate = 9600,timeout = 1.0)
data = np.zeros((1,3))

#Resetea Arduino
arduino.setDTR(False)
time.sleep(1)
arduino.flushInput()
arduino.setDTR(True)

with arduino:
    while True:
        try:
            line = arduino.readline()
            if not line:
                continue
            aux = np.fromstring(line.decode('ascii',errors='replace'),sep='\t')
            data = np.vstack((data,aux))
            temp.append(aux[0])
            term1.append(aux[1])
            tti.set_ydata(temp)
            ll.set_ydata(term1)
            axt.set_ylim(min(temp)-5,max(temp)+5)
            ax1.set_ylim(min(term1) - 500, max(term1) + 500)
            plt.pause(0.001)
        except ValueError:
            warnings.warn("Error, saltando linea {}".format(line))
        except KeyboardInterrupt:
            print("\n")
            print("Saliendo...")
            break


np.savetxt(options.fname,data)
