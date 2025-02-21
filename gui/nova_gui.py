import sys
import os
import tkinter as tk
from tkinter import ttk
import numpy as np
from scipy.stats import norm
from numpy.fft import fft, ifft

# Ensure Python can find physics subsystems and math engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'math_engine')))

# Import all physics and math functions
from physics_subsystems.forces_work_energy import (
    force, work, power, kinetic_energy, potential_energy, momentum, impulse
)
from physics_subsystems.particle_systems import (
    center_of_mass, total_momentum, collision_momentum, impulse_momentum
)
from math_engine import (
    add, subtract, multiply, divide,
    differentiate, integrate,
    matrix_multiply, matrix_inverse, matrix_determinant, matrix_eigenvalues,
    compute_mean, compute_std, normal_distribution,
    fourier_transform, inverse_fourier_transform
)

# Function to update input labels dynamically
def update_inputs(*args):
    selected_function = function_var.get()
    
    input_config = {
        "Force (F = m * a)": ["Mass (kg)", "Acceleration (m/s²)"],
        "Work (W = F * d * cos(θ))": ["Force (N)", "Displacement (m)"],
        "Power (P = W / t)": ["Work (J)", "Time (s)"],
        "Kinetic Energy (KE = 1/2 * m * v²)": ["Mass (kg)", "Velocity (m/s)"],
        "Potential Energy (PE = m * g * h)": ["Mass (kg)", "Height (m)"],
        "Momentum (p = m * v)": ["Mass (kg)", "Velocity (m/s)"],
        "Impulse (J = F * t)": ["Force (N)", "Time (s)"],
        "Total Momentum": ["Masses (comma-separated)", "Velocities (comma-separated)"],
        "Impulse-Momentum": ["Mass (kg)", "Initial Velocity (m/s), Final Velocity (m/s)"],
        "Add": ["Number 1", "Number 2"],
        "Subtract": ["Number 1", "Number 2"],
        "Multiply": ["Number 1", "Number 2"],
        "Divide": ["Numerator", "Denominator"],
        "Differentiate": ["Function f(x)", "Point x"],
        "Integrate": ["Function f(x)", "Lower Limit, Upper Limit"],
        "Matrix Multiply": ["Matrix A (comma-separated rows)", "Matrix B (comma-separated rows)"],
        "Matrix Inverse": ["Matrix A (comma-separated rows)", ""],
        "Matrix Determinant": ["Matrix A (comma-separated rows)", ""],
        "Matrix Eigenvalues": ["Matrix A (comma-separated rows)", ""],
        "Mean": ["Dataset (comma-separated)", ""],
        "Standard Deviation": ["Dataset (comma-separated)", ""],
        "Normal Distribution": ["x", "Mean, Standard Deviation"],
        "Fourier Transform": ["Signal (comma-separated)", ""],
        "Inverse Fourier Transform": ["Frequency Data (comma-separated)", ""]
    }

    if selected_function in input_config:
        label1.config(text=input_config[selected_function][0])
        label2.config(text=input_config[selected_function][1])

# Function to perform calculations
def calculate():
    selected_function = function_var.get()
    
    try:
        val1 = entry1.get().strip()
        val2 = entry2.get().strip()

        if "," in val1:
            val1 = np.array([float(x) for x in val1.split(",")])
        else:
            val1 = float(val1)

        if "," in val2:
            val2 = np.array([float(x) for x in val2.split(",")])
        else:
            val2 = float(val2)

        functions = {
            "Add": add,
            "Subtract": subtract,
            "Multiply": multiply,
            "Divide": divide,
            "Differentiate": differentiate,
            "Integrate": integrate,
            "Matrix Multiply": matrix_multiply,
            "Matrix Inverse": matrix_inverse,
            "Matrix Determinant": matrix_determinant,
            "Matrix Eigenvalues": matrix_eigenvalues,
            "Mean": compute_mean,
            "Standard Deviation": compute_std,
            "Normal Distribution": normal_distribution,
            "Fourier Transform": fourier_transform,
            "Inverse Fourier Transform": inverse_fourier_transform
        }

        result = functions[selected_function](val1, val2) if selected_function in functions else "Invalid selection"
        result_label.config(text=f"Result: {result}")
    
    except ValueError:
        result_label.config(text="Invalid input. Enter valid numbers.")

# Create the main GUI window
root = tk.Tk()
root.title("N.O.V.A. Physics Calculator")

# Dropdown for selecting function
function_var = tk.StringVar()
function_dropdown = ttk.Combobox(root, textvariable=function_var)
function_dropdown["values"] = list(update_inputs.__globals__["input_config"].keys())
function_dropdown.grid(row=0, column=1, padx=10, pady=10)
function_dropdown.set("Select a calculation")
function_dropdown.bind("<<ComboboxSelected>>", update_inputs)

# Input fields with labels
label1 = tk.Label(root, text="Input 1:")
label1.grid(row=1, column=0)
entry1 = tk.Entry(root)
entry1.grid(row=1, column=1)

label2 = tk.Label(root, text="Input 2:")
label2.grid(row=2, column=0)
entry2 = tk.Entry(root)
entry2.grid(row=2, column=1)

# Calculate button
calculate_button = tk.Button(root, text="Calculate", command=calculate)
calculate_button.grid(row=3, column=1, pady=10)

# Result label
result_label = tk.Label(root, text="Result: ")
result_label.grid(row=4, column=1, pady=10)

# Run GUI loop
root.mainloop()
