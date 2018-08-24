import time
import warnings
import numpy as np
import matplotlib.pyplot as plt
import serial
from collections import deque


N = 200
foto = deque([0] * N, maxlen=N)  # deque con longitud maxima N


#Creamos la figura
plt.ion()
fig, ax = plt.subplots(1,1)
ax.set_title("Fotoresistencia")
plot, = ax.plot(foto)

arduino = serial.Serial('/dev/cu.usbmodem1411',baudrate = 9600,timeout = 1.0)
data = np.zeros((1,1))

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
			curr = np.fromstring(line.decode('ascii', errors='replace'), sep='\t')
			data = np.vstack((data, curr))
			foto.append(curr[0])
			ax.set_ylim(min(foto) - 100, max(foto) + 100)
			plot.set_ydata(foto)
			plt.pause(0.01)
		except ValueError:
			warnings.warn("Error, saltando linea {}".format(line))
		except KeyboardInterrupt:
			print('\n')
			print('Saliendo...')
			break

np.savetxt("45", data)
