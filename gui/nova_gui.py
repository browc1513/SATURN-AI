import sys
import os
import tkinter as tk
from tkinter import ttk
import numpy as np
from scipy.stats import norm
from numpy.fft import fft, ifft

# Ensure project paths are accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'math_engine')))

# Import N.O.V.A.
from core.nova_instance import nova

# Physics and math imports
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

# ---------- GUI Functions ----------

def update_inputs(*args):
    selected_function = function_var.get()
    if selected_function in input_config:
        label1.config(text=input_config[selected_function][0])
        label2.config(text=input_config[selected_function][1])

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

        result = functions[selected_function](val1, val2) if selected_function in functions else "Invalid selection"
        result_label.config(text=f"Result: {result}")
        nova.speak(f"Here’s the result: {result}")
        update_chat(f"{nova.name}: Here’s the result: {result}")

    except Exception as e:
        result_label.config(text="Invalid input. Please check your entries.")
        nova.speak("Hmm... something didn’t add up. Want to double-check those numbers?")
        update_chat(f"{nova.name}: Something went wrong: {str(e)}")

def change_mode(event=None):
    selected_mode = mode_var.get().lower()
    nova.set_mode(selected_mode)
    update_chat(f"{nova.name} switched to {selected_mode.capitalize()} Mode.")

def update_chat(message):
    chat_output.configure(state='normal')
    chat_output.insert(tk.END, message + "\n")
    chat_output.configure(state='disabled')
    chat_output.see(tk.END)

# ---------- App Init ----------
nova.react_to_task("math")  # Set default mode
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
input_config = {
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

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("N.O.V.A. Physics & Math Assistant")

# Function selection
function_var = tk.StringVar()
function_dropdown = ttk.Combobox(root, textvariable=function_var, width=40)
function_dropdown["values"] = list(input_config.keys())
function_dropdown.set("Select a calculation")
function_dropdown.grid(row=0, column=1, columnspan=2, padx=10, pady=10)
function_dropdown.bind("<<ComboboxSelected>>", update_inputs)

# Input fields
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

# Result display
result_label = tk.Label(root, text="Result: ")
result_label.grid(row=4, column=1, pady=10)

# Mode switch dropdown
mode_var = tk.StringVar()
mode_dropdown = ttk.Combobox(root, textvariable=mode_var, width=20)
mode_dropdown["values"] = ["Science", "Creative", "Chill"]
mode_dropdown.set("Science")
mode_dropdown.grid(row=0, column=0, padx=10, pady=10)
mode_dropdown.bind("<<ComboboxSelected>>", change_mode)

# Chat output window (scrollable)
chat_output = tk.Text(root, height=12, width=60, state='disabled', bg="#1e1e1e", fg="#d4d4d4")
chat_output.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Launch
update_chat(f"{nova.name} is online and ready in Science Mode.")
root.mainloop()
