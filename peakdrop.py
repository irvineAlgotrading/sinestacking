import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import sys
import threading

# Subclass GraphicsLayoutWidget to handle close event
class CustomGraphWidget(pg.GraphicsLayoutWidget):
    def closeEvent(self, event):
        timer.stop()  # Stop the timer
        app.quit()  # Quit the application

# Constants
WAVELENGTH_MIN = 1e-9  # 1 nanometer
WAVELENGTH_MAX = 1e-7  # 100 micrometers
Y_MAX = 100  # 100%
Y_MIN = 0    # 0%
SPIKE_INTERVAL = 10e-10  # 500 nanometers
UPDATE_INTERVAL_MS = 1  # 100 milliseconds
MAJOR_SPIKE_PROBABILITY = 0.005  # Probability of a major spike
NORMAL_Y_MAX = 30  # 5% for normal data
MAJOR_SPIKE_Y_MIN = 70  # 60% minimum for major spikes
MAJOR_SPIKE_Y_MAX = 100  # 80% maximum for major spikes

# Initialize wavelengths
wavelengths = np.arange(WAVELENGTH_MIN, WAVELENGTH_MAX, SPIKE_INTERVAL)

# Initialize values
values = np.random.uniform(Y_MIN, NORMAL_Y_MAX, len(wavelengths))

# Create the PyQtGraph application
app = QtWidgets.QApplication([])
win = CustomGraphWidget(show=True, title="Real Time Plot")
plot = win.addPlot(title="Real Time Data")
curve = plot.plot(wavelengths, values, pen='y')

# Set fixed y-axis range
plot.setYRange(Y_MIN, Y_MAX)

def update():
    global values
    # Normal random changes for all values
    normal_values = np.random.uniform(Y_MIN, NORMAL_Y_MAX, len(wavelengths))

    # Introduce major spikes with a small probability
    for i in range(len(wavelengths)):
        if np.random.uniform(0, 1) < MAJOR_SPIKE_PROBABILITY:
            normal_values[i] = np.random.uniform(MAJOR_SPIKE_Y_MIN, MAJOR_SPIKE_Y_MAX)

    # Update values
    values = normal_values

    # Update line plot
    curve.setData(wavelengths, values)

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(UPDATE_INTERVAL_MS)

def listen_for_resume():
    while input() != 'resume':
        pass
    timer.start()

# Start listening for resume command in a separate thread
listen_thread = threading.Thread(target=listen_for_resume, daemon=True)
listen_thread.start()

# Start the PyQt event loop
if (sys.flags.interactive != 1) or not hasattr(QtGui, 'PYQT_VERSION'):
    QtWidgets.QApplication.instance().exec_()
