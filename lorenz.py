import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
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
t = np.linspace(0, 100, num=10000)

# Solve the differential equations
solution = odeint(lorenz_system, initial_state, t)

# Extract solutions
x, y, z = solution.T

# Set up the figure, the axis, and the plot element
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

# Axes limits
ax.set_xlim(-20, 20)
ax.set_ylim(0, 50)

# Title and labels
ax.set_title('Lorenz Attractor Projection on the xz-plane')
ax.set_xlabel('x')
ax.set_ylabel('z')

# Initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# Animation function: this is called sequentially
def animate(i):
    line.set_data(x[:i], z[:i])
    return line,

# Call the animator
ani = FuncAnimation(fig, animate, init_func=init, frames=len(t), interval=1, blit=True)

# To save the animation, use the line below
# ani.save('lorenz_attractor.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

# # Plot x vs z
# plt.figure()
# plt.plot(x, z)
# plt.title('Lorenz Attractor Projection on the xz-plane')
# plt.xlabel('x')
# plt.ylabel('z')
plt.show()
