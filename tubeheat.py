import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class TubeRenderer:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
    
    def setup_ui(self):
        self.root.title("3D Tube Renderer with Thick Walls and Default Values")

        # Creating input fields with default values
        ttk.Label(self.root, text="Height:").grid(row=0, column=0)
        self.height_entry = ttk.Entry(self.root)
        self.height_entry.grid(row=0, column=1)
        self.height_entry.insert(0, "2")  # Default value

        ttk.Label(self.root, text="Inner Diameter:").grid(row=1, column=0)
        self.inner_dia_entry = ttk.Entry(self.root)
        self.inner_dia_entry.grid(row=1, column=1)
        self.inner_dia_entry.insert(0, "0.5")  # Default value

        ttk.Label(self.root, text="Wall Thickness:").grid(row=2, column=0)
        self.thickness_entry = ttk.Entry(self.root)
        self.thickness_entry.grid(row=2, column=1)
        self.thickness_entry.insert(0, "0.1")  # Default value

        ttk.Label(self.root, text="Material K Value:").grid(row=3, column=0)
        self.material_k_entry = ttk.Entry(self.root)
        self.material_k_entry.grid(row=3, column=1)

        # Render button
        render_button = ttk.Button(self.root, text="Render", command=self.render_tube)
        render_button.grid(row=4, column=0, columnspan=2)

    def render_tube(self):
        try:
            # Getting values from entries
            height = float(self.height_entry.get())
            inner_dia = float(self.inner_dia_entry.get())
            thickness = float(self.thickness_entry.get())

            # Calculating outer diameter
            outer_dia = inner_dia + 2 * thickness

            # Drawing the tube with thick walls
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            # Creating a mesh for the tube
            x = np.linspace(-outer_dia/2, outer_dia/2, 100)
            z = np.linspace(0, height, 100)
            X_outer, Z = np.meshgrid(x, z)
            Y_outer = np.sqrt((outer_dia/2)**2 - X_outer**2)

            # Plotting the outer surface
            ax.plot_surface(X_outer, Y_outer, Z, color='blue', alpha=0.6)
            ax.plot_surface(X_outer, -Y_outer, Z, color='blue', alpha=0.6)

            # Creating a mesh for the inner surface
            X_inner, Z = np.meshgrid(x, z)
            Y_inner = np.sqrt(np.maximum((inner_dia/2)**2 - X_inner**2, 0))

            # Plotting the inner surface
            ax.plot_surface(X_inner, Y_inner, Z, color='red', alpha=0.6)
            ax.plot_surface(X_inner, -Y_inner, Z, color='red', alpha=0.6)

            # Plotting the disc caps
            theta = np.linspace(0, 2 * np.pi, 100)
            r_outer = np.linspace(0, outer_dia/2, 50)
            T, R_outer = np.meshgrid(theta, r_outer)
            X_cap_outer = R_outer * np.cos(T)
            Y_cap_outer = R_outer * np.sin(T)

            # Top cap outer
            Z_cap_top_outer = np.full_like(X_cap_outer, height)
            ax.plot_surface(X_cap_outer, Y_cap_outer, Z_cap_top_outer, color='green', alpha=0.6)

            # Bottom cap outer
            Z_cap_bottom_outer = np.zeros_like(X_cap_outer)
            ax.plot_surface(X_cap_outer, Y_cap_outer, Z_cap_bottom_outer, color='green', alpha=0.6)

            # Adjusting plot limits
            ax.set_xlim([-outer_dia/2, outer_dia/2])
            ax.set_ylim([-outer_dia/2, outer_dia/2])
            ax.set_zlim([0, height])

            plt.show()
        except ValueError:
            print("Please enter valid numeric values.")

# Create the Tkinter window
root = tk.Tk()
app = TubeRenderer(root)
root.mainloop()
