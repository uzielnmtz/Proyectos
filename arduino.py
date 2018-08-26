import time
import warnings
import numpy as np
import matplotlib.pyplot as plt
import serial
from collections import deque
import argparse
import platform

os = platform.system()
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Output file")
parser.add_argument("-p", "--port", help="Port")
parser.add_argument("-N", help="Log length", default=200, type=int)
parser.add_argument("-t", "--timeout", default=1.0, type=float)
parser.add_argument("-b", "--baudrate", default=9600, type=int)
parser.add_argument("--plot", help="Display plot", action="store_true")
args = parser.parse_args()

if args.port:
    if os == "Darwin":
        port = '/dev/cu.usbmodem' + args.port
    elif os == "Linux":
        port = "/dev/" + args.port
else:
    if os == "Darwin":
        port = '/dev/cu.usbmodem1421'

foto = deque([0] * N, maxlen=N)

# Plot config
if args.plot:
    plt.ion()
    fig, ax = plt.subplots(1, 1)
    ax.set_title("Fotoresistencia")
    plot, = ax.plot(foto)

arduino = serial.Serial(port, baudrate=args.baudrate, timeout=args.timeout)
data = np.zeros((1, 1))

# Arduino reset
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
            if args.plot:
                ax.set_ylim(min(foto) - 100, max(foto) + 100)
                plot.set_ydata(foto)
                plt.pause(0.01)
        except ValueError:
            warnings.warn("Error, skipping line {}".format(line))
        except KeyboardInterrupt:
            print('\n')
            print('Exiting...')
            break

np.savetxt(args.file, data)
