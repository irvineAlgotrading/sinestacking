import tkinter as tk
from tkinter import ttk
import math

# Create the main window
root = tk.Tk()
root.title("RSS Analysis Tool")

# Frame to hold the widgets
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.columnconfigure(1, weight=1)  # Configure the column to center widgets

# Lists to store tolerance entry widgets and their corresponding delete buttons
tolerances = []  
delete_buttons = []

# Function to update the positions of the buttons and labels
def update_positions():
    for i, (entry, btn) in enumerate(zip(tolerances, delete_buttons)):
        entry.grid(row=i+1, column=1, sticky=(tk.W, tk.E))
        btn.grid(row=i+1, column=2)
    calculate_button.grid(row=len(tolerances) + 1, column=1, sticky=tk.EW)
    rss_label.grid(row=len(tolerances) + 2, column=1, sticky=tk.EW)
    max_tol_label.grid(row=len(tolerances) + 3, column=1, sticky=tk.EW)
    hybrid_label.grid(row=len(tolerances) + 4, column=1, sticky=tk.EW)

# Function to delete a tolerance field
def delete_tolerance(index):
    tolerances[index].destroy()  # Remove the entry widget
    delete_buttons[index].destroy()  # Remove the delete button
    del tolerances[index]  # Remove the entry from the list
    del delete_buttons[index]  # Remove the button from the list
    update_positions()  # Update positions of widgets

# Function to add a new tolerance field
def add_tolerance_field():
    entry = ttk.Entry(frame)
    entry.grid(column=1, row=len(tolerances)+1, sticky=(tk.W, tk.E))
    tolerances.append(entry)

    # Add a delete button for the tolerance field
    delete_button = ttk.Button(frame, text="Delete", command=lambda: delete_tolerance(len(tolerances)-1))
    delete_button.grid(column=2, row=len(tolerances), sticky=tk.W)
    delete_buttons.append(delete_button)

    update_positions()

# Button to add new tolerance fields
add_button = ttk.Button(frame, text="Add Tolerance", command=add_tolerance_field)
add_button.grid(column=1, row=0, sticky=tk.EW)

# Function to perform RSS calculation and compute maximum tolerance and hybrid measure
def calculate_results():
    rss = math.sqrt(sum(float(t.get())**2 for t in tolerances if t.get()))
    max_tol = sum(float(t.get()) for t in tolerances if t.get())
    hybrid = (rss + max_tol) / 2

    rss_label.config(text=f"RSS: {rss}")
    max_tol_label.config(text=f"Max: {max_tol}")
    hybrid_label.config(text=f"Hybrid: {hybrid}")

# Button to calculate results
calculate_button = ttk.Button(frame, text="Calculate Results", command=calculate_results)

# Labels to display the results with fixed widths
rss_label = ttk.Label(frame, text="RSS: ", anchor='center', width=30)
max_tol_label = ttk.Label(frame, text="Max: ", anchor='center', width=30)
hybrid_label = ttk.Label(frame, text="Hybrid: ", anchor='center', width=30)

# Add the first tolerance field by default
add_tolerance_field()

# Start the application
root.mainloop()
