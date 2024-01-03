import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Lorenz system parameters
sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

# Lorenz system differential equations
def lorenz_system(current_state, t):
    x, y, z = current_state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

# Initial conditions
initial_state = [-8, 8, 27]

# Time points
t = np.linspace(0, 50, num=5000)

# Solve the differential equations
solution = odeint(lorenz_system, initial_state, t)

# Extract solutions
x, y, z = solution.T

# Set up the figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set up line and point objects
line, = ax.plot([], [], [], lw=2)
point, = ax.plot([], [], [], 'go')

# Axes labels
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')

# Setting the axes properties
ax.set_xlim3d([-20.0, 20.0])
ax.set_ylim3d([-30.0, 30.0])
ax.set_zlim3d([0.0, 50.0])
ax.set_title('3D Lorenz Attractor')

# Initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    line.set_3d_properties([])
    point.set_data([], [])
    point.set_3d_properties([])
    return line, point

# Animation function: this is called sequentially
def animate(i):
    line.set_data(x[:i], y[:i])
    line.set_3d_properties(z[:i])
    point.set_data(x[i], y[i])
    point.set_3d_properties(z[i])
    return line, point

# Call the animator
ani = FuncAnimation(fig, animate, init_func=init, frames=len(t), interval=1, blit=False)

plt.show()
