import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import sys
import threading
import time
from collections import deque

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
    'CO2': {'center': 2340, 'width': 20, 'height': 1.0},
    'Water': {'center': 3700, 'width': 25, 'height': 1.2},
    'Methane': {'center': 3020, 'width': 15, 'height': 1.1},
    # Add other gases and their peak properties here
}

# Timestamps for managing peak reductions
last_reduction_time = time.time() - 5  # Initialize to allow immediate peak reduction
reduction_duration = 1  # Duration of the reduction in seconds
peak_reduced = False  # Flag to indicate if a peak is currently reduced
reduced_gas = None  # To keep track of which gas is reduced

# Create the PyQtGraph application
app = QtWidgets.QApplication([])
win = CustomGraphWidget(show=True, title="Simulated Gas Spectrograph")
plot = win.addPlot(title="Real Time Data")
curve = plot.plot(wavenumbers, values, pen='y')

# Set fixed y-axis range
plot.setYRange(0, 1.5)

# Function to add peaks to the values
def add_peaks(wavenumbers, values, reduce_peak=False, reduced_gas=None):
    global gas_peaks, gas_histories

    for gas, properties in gas_peaks.items():
        width = int(np.random.normal(properties['width'], 2))
        if reduce_peak and gas == reduced_gas:
            height = np.random.normal(properties['height'] * 0.6, 0.05)  # Reduced height by 40%
        else:
            height = np.random.normal(properties['height'], 0.05)

        peak_center_index = np.searchsorted(wavenumbers, properties['center'])
        start_index = max(peak_center_index - width // 2, 0)
        end_index = min(peak_center_index + width // 2, len(wavenumbers))
        values[start_index:end_index] = height
        # Update history immediately after setting the peak values
        gas_histories[gas].append(height)

# Create deques for storing historical values of each gas peak
history_length = 80  # 50 ms of history
gas_histories = {gas: deque(maxlen=history_length) for gas in gas_peaks}

# Label for displaying the wavenumber
warning_label = pg.TextItem(anchor=(0.5, 0), color='w')
plot.addItem(warning_label, ignoreBounds=True)
warning_label.setPos((WAVELENGTH_MAX - WAVELENGTH_MIN) / 2, 1.4)  # Upper center position

# Function to update the historical values and check the standard deviation
def check_std_deviation():
    for gas, history in gas_histories.items():
        # Append the latest value to the history
        latest_value = values[np.searchsorted(wavenumbers, gas_peaks[gas]['center'])]
        history.append(latest_value)

        # Only check if we have a full history
        if len(history) == history_length:
            std_dev = np.std(history)
            mean_val = np.mean(history)

            # Calculate the number of standard deviations the latest value is from the mean
            deviations_from_mean = (latest_value - mean_val) / std_dev if std_dev else 0

            # If the deviation is more than 3, display the warning
            if np.abs(deviations_from_mean) > 1.8:
                warning_text = f"{gas_peaks[gas]['center']} cm-1"
                # print(f"Deviation triggered at wavenumber: {warning_text}")

                # Set the label text and ensure it's visible
                warning_label.setText(warning_text)
                warning_label.setVisible(True)

                # Use a singleShot timer to clear the label after 5 seconds
                QtCore.QTimer.singleShot(2000, lambda: warning_label.setText(''))

                # Break after finding the first deviation
                break
# Timer and update function
def update():
    global last_reduction_time, peak_reduced, reduced_gas

    # Create baseline noise
    noise = np.random.normal(0, 0.02, len(wavenumbers))

    # Reset values to noise for each update
    values[:] = noise

    current_time = time.time()

    # Check standard deviation
    check_std_deviation()

    # Check if it's been 5 seconds since the last reduction
    if current_time - last_reduction_time >= 5 and not peak_reduced:
        # Reduce a random peak
        reduced_gas = np.random.choice(list(gas_peaks.keys()))
        add_peaks(wavenumbers, values, reduce_peak=True, reduced_gas=reduced_gas)
        peak_reduced = True
        last_reduction_time = current_time
    elif peak_reduced and current_time - last_reduction_time < reduction_duration:
        # Keep the reduced peak
        add_peaks(wavenumbers, values, reduce_peak=True, reduced_gas=reduced_gas)
    else:
        # Add peaks without reduction
        add_peaks(wavenumbers, values)
        peak_reduced = False

    # Update the plot
    curve.setData(wavenumbers, values)

    # Check standard deviation immediately after updating values
    check_std_deviation()

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

# Adjust the warning label position
def resize_event():
    # Update label position to stay at the top center
    warning_label.setPos((WAVELENGTH_MAX - WAVELENGTH_MIN) / 2, 1.45)

# Connect the resize event
plot.getViewBox().sigResized.connect(resize_event)

# Ensure the label is hidden on startup
warning_label.setText('')
warning_label.setVisible(False)

# Start the PyQt event loop
if (sys.flags.interactive != 1) or not hasattr(QtGui, 'PYQT_VERSION'):
    QtWidgets.QApplication.instance().exec_()