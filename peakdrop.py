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

# Constants for the plot
WAVELENGTH_MIN = 600  # Min wavenumber in cm-1
WAVELENGTH_MAX = 4000  # Max wavenumber in cm-1
SPIKE_INTERVAL = 1  # 1 cm-1 interval between points
UPDATE_INTERVAL_MS = 1  # 1 ms update rate

# Initialize wavenumbers
wavenumbers = np.arange(WAVELENGTH_MIN, WAVELENGTH_MAX, SPIKE_INTERVAL)
values = np.zeros(len(wavenumbers))

# Gas peak wavenumbers (for example purposes, use actual values for real gases)
gas_peaks = {
    'CO2': 2340,
    'Water': 3700,
    'Methane': 3020,
    # Add other gases and their peak wavenumbers here
}

# Create the PyQtGraph application
app = QtWidgets.QApplication([])
win = CustomGraphWidget(show=True, title="Simulated Gas Spectrograph")
plot = win.addPlot(title="Real Time Data")
curve = plot.plot(wavenumbers, values, pen='y')

# Set fixed y-axis range
plot.setYRange(0, 1.5)

# Timer and update function
def update():
    # Create baseline noise
    noise = np.random.normal(0, 0.02, len(wavenumbers))
    
    # Reset values to noise for each update
    values[:] = noise
    
    # Add random peaks at gas wavenumbers
    for gas, peak in gas_peaks.items():
        if np.random.random() < 0.05:  # 5% chance to simulate a gas peak
            peak_width = np.random.randint(10, 30)  # Random peak width
            peak_height = np.random.uniform(0.1, 1.5)  # Random peak height
            peak_start = peak - peak_width // 2
            peak_end = peak + peak_width // 2
            peak_range = np.arange(peak_start, peak_end)
            values[peak_range] = peak_height

    # Update the plot
    curve.setData(wavenumbers, values)

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(UPDATE_INTERVAL_MS)

# Start listening for resume command in a separate thread
def listen_for_resume():
    while input() != 'resume':
        pass
    timer.start()

listen_thread = threading.Thread(target=listen_for_resume, daemon=True)
listen_thread.start()

# Start the PyQt event loop
if (sys.flags.interactive != 1) or not hasattr(QtGui, 'PYQT_VERSION'):
    QtWidgets.QApplication.instance().exec_()
