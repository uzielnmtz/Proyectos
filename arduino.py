import time
import warnings
import numpy as np
import matplotlib.pyplot as plt
import serial
from collections import deque
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Output file")
parser.add_argument("-p", "--port", help="Port")
parser.add_argument("-N", help="Log length")
parser.add_argument("-t", "--timeout")
parser.add_argument("-b", "--baudrate")
parser.add_argument("--plot", help="Display plot", action="store_true")
args = parser.parse_args()

# Parse config
if args.file:
    file_name = args.file
else:
    file_name = "data.txt"

if args.N:
    N = int(args.N)
else:
    N = 200

if args.port:
    port = '/dev/cu.usbmodem' + args.port
else:
    port = '/dev/cu.usbmodem1421'

if args.timeout:
    timeout_ = float(args.timeout)
else:
    timeout_ = 1.0

if args.baudrate:
    baudrate_ = int(args.baudrate)
else:
    baudrate_ = 9600


foto = deque([0] * N, maxlen=N)

# Plot config
if args.plot:
    plt.ion()
    fig, ax = plt.subplots(1, 1)
    ax.set_title("Fotoresistencia")
    plot, = ax.plot(foto)

arduino = serial.Serial(port, baudrate=baudrate_, timeout=timeout_)
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

np.savetxt(file_name, data)
