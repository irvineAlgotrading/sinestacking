import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize frequency and phase
frequency = 1000.0
phase = 0.0

# This function is called periodically from FuncAnimation
def update(frame_number, line, ax):
    # Use the global frequency and phase variables
    global frequency, phase

    # Increase the phase
    phase += 0.05

    # Generate new data for plotting
    x = np.linspace(0, 1, 100)
    a = np.sin(frequency ** ((x - phase)))  # sine wave with changing frequency and phase
    b = np.sin(a - phase)
    y = np.sin(b + phase)
    # y = x

    # Update the data of the line with the new values
    line.set_data(x, y)

    # Adjust limits if necessary
    ax.set_xlim(np.min(x), np.max(x))
    ax.set_ylim(-1, 1)

    return line,

# This function will be called when the mouse is moved over the plot
def on_move(event):
    global frequency

    # Check if the event was within the Axes
    if event.inaxes:
        # Set the frequency based on the mouse x-coordinate (scaled)
        # Map the mouse x position to a frequency range
        # Assuming the plot width represents a frequency range from 0.1 to 2.0
        plot_width = event.inaxes.get_xlim()[1] - event.inaxes.get_xlim()[0]
        frequency = 0.1 + (event.xdata / plot_width) * 1.9

# Set up the figure, the axis, and the plot element
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

# Axes labels
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')

# Connect the mouse move event to the function
fig.canvas.mpl_connect('motion_notify_event', on_move)

# This calls the 'update' function periodically
ani = FuncAnimation(fig, update, fargs=(line, ax), interval=50, blit=True)

# Show the plot
plt.show()
