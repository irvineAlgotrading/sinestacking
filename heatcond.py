import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib import cm

# Dimensions of the aluminum block (in inches)
length = 6
width = 2
height = 1

# Convert dimensions to a smaller scale for computational efficiency
scale_factor = 10
L, W, H = length * scale_factor, width * scale_factor, height * scale_factor

# Create a 3D meshgrid for the block
x = np.linspace(0, length, L)
y = np.linspace(0, width, W)
z = np.linspace(0, height, H)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# Initialize temperature distribution in the block
# 100 C on the left face and 20 C on the right face
temperature = np.linspace(100, 20, L)

# Adjusting the temperature array to match the dimensions of the X, Y, Z arrays
temperature_3d = np.zeros((L, W, H))
for i in range(W):
    for j in range(H):
        temperature_3d[:, i, j] = temperature

# Heat conduction parameters
alpha = 0.01  # thermal diffusivity of 6061 aluminum (in m^2/s)
dt = 0.1      # time step (in seconds)

# Function to update temperature distribution
def update_temperature(temp_3d):
    # Apply a simple heat diffusion model
    new_temp = temp_3d.copy()
    for i in range(1, L-1):
        new_temp[i, :, :] = temp_3d[i, :, :] + alpha * dt * (temp_3d[i+1, :, :] - 2*temp_3d[i, :, :] + temp_3d[i-1, :, :])
    return new_temp

# Set up the figure and 3D axis for animation
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot initial state
scat = ax.scatter(X.flatten(), Y.flatten(), Z.flatten(), c=temperature_3d.flatten(), cmap='rainbow', marker='s')

# Set axis labels
ax.set_xlabel('Length (in)')
ax.set_ylabel('Width (in)')
ax.set_zlabel('Height (in)')
ax.set_title('Heat Conduction in Aluminum Block')

# Function to update the scatter plot for each frame
def animate(frame):
    global temperature_3d
    temperature_3d = update_temperature(temperature_3d)
    scat.set_array(temperature_3d.flatten())
    return scat,

# Create the animation
ani = FuncAnimation(fig, animate, frames=100, interval=100, blit=False)

plt.show()
