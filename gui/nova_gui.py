import sys
import os
import tkinter as tk
from tkinter import ttk

import numpy as np
from scipy.stats import norm
from numpy.fft import fft, ifft
from sympy import Matrix, sympify, pretty


# Ensure project paths are accessible
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)

# ---------- Import N.O.V.A. ----------

from core.nova_instance import get_nova

nova = get_nova("nova_config.json")


# ---------- Physics Imports ----------

from physics_subsystems.forces_work_energy import (
    force,
    work,
    power,
    kinetic_energy,
    potential_energy,
    momentum,
    impulse
)

from physics_subsystems.particle_systems import (
    center_of_mass,
    total_momentum,
    collision_momentum,
    impulse_momentum
)


# ---------- Math Imports ----------

from math_engine.math_engine import (
    add,
    subtract,
    multiply,
    divide,
    differentiate,
    integrate,
    matrix_multiply,
    matrix_inverse,
    matrix_determinant,
    matrix_eigenvalues,
    matrix_rref,
    compute_mean,
    compute_std,
    normal_distribution,
    fourier_transform,
    inverse_fourier_transform
)


# ============================================================
# GUI FUNCTIONS
# ============================================================


def update_inputs(*args):
    """
    Update the labels beside the input boxes based on the
    calculation selected by the user.
    """

    selected_function = function_var.get()

    if selected_function in input_config:
        label1.config(
            text=input_config[selected_function][0]
        )

        label2.config(
            text=input_config[selected_function][1]
        )


# ============================================================
# MATRIX PARSER
# ============================================================

def parse_matrix(text):
    """
    Convert matrix text entered through the GUI into a
    list of lists that SymPy can process.

    Accepted row separators:
    - New lines
    - Semicolons

    Accepted column separator:
    - Commas

    Example:

    1,1,1,8
    0,2,1,5
    0,0,3,9
    """

    if not text.strip():
        raise ValueError("Matrix input cannot be empty.")

    # Allow both semicolons and line breaks as row separators
    cleaned_text = text.replace(";", "\n")

    rows = [
        row.strip()
        for row in cleaned_text.splitlines()
        if row.strip()
    ]

    matrix = []

    for row in rows:

        values = row.split(",")

        parsed_row = [
            sympify(value.strip())
            for value in values
        ]

        matrix.append(parsed_row)

    # Make sure all rows contain the same number of columns
    row_lengths = [
        len(row)
        for row in matrix
    ]

    if len(set(row_lengths)) != 1:
        raise ValueError(
            "All matrix rows must contain the same number of columns."
        )

    return matrix


# ============================================================
# RREF CALCULATOR
# ============================================================

def calculate_rref(matrix_text):
    """
    Parse an augmented matrix, calculate its RREF,
    determine the type of solution, and format the output.
    """

    matrix = parse_matrix(matrix_text)

    original_matrix = Matrix(matrix)

    result, pivots = matrix_rref(matrix)


    # --------------------------------------------------------
    # Basic matrix information
    # --------------------------------------------------------

    num_variables = result.cols - 1
    constant_column = result.cols - 1


    # --------------------------------------------------------
    # Build formatted output
    # --------------------------------------------------------

    output = ""

    output += "Original Augmented Matrix:\n\n"
    output += pretty(original_matrix)

    output += "\n\n"

    output += "Reduced Row Echelon Form:\n\n"
    output += pretty(result)


    # --------------------------------------------------------
    # Check for inconsistent rows
    #
    # Example:
    #
    # [0 0 0 | 1]
    #
    # means
    #
    # 0 = 1
    #
    # so the system has no solution.
    # --------------------------------------------------------

    inconsistent = False

    for i in range(result.rows):

        coefficients_are_zero = all(
            result[i, j] == 0
            for j in range(num_variables)
        )

        if (
            coefficients_are_zero
            and result[i, constant_column] != 0
        ):
            inconsistent = True
            break


    # --------------------------------------------------------
    # Identify pivots belonging to variable columns
    # --------------------------------------------------------

    variable_pivots = [
        pivot
        for pivot in pivots
        if pivot < num_variables
    ]


    # --------------------------------------------------------
    # Determine solution type
    # --------------------------------------------------------

    if inconsistent:

        output += "\n\nSolution:\n\n"
        output += "No solution.\n"
        output += "The system is inconsistent."


    elif len(variable_pivots) < num_variables:

        output += "\n\nSolution:\n\n"
        output += "The system has infinitely many solutions.\n"
        output += "One or more variables are free."


    else:

        solutions = []

        output += "\n\nSolutions:\n\n"

        for variable_index in range(num_variables):

            value = result[
                variable_index,
                constant_column
            ]

            solutions.append(value)

            output += (
                f"x{variable_index + 1} = {value}\n"
            )


        output += "\nSolution List:\n"

        output += (
            "["
            + ", ".join(str(value) for value in solutions)
            + "]"
        )


    # --------------------------------------------------------
    # Pivot information
    # --------------------------------------------------------

    output += "\n\nPivot Columns:\n"
    output += str(pivots)


    return output


# ============================================================
# MAIN CALCULATE FUNCTION
# ============================================================

def calculate():

    selected_function = function_var.get()

    try:

        val1 = entry1.get("1.0", tk.END).strip()
        val2 = entry2.get().strip()


        # ====================================================
        # RREF
        # ====================================================

        if selected_function == "RREF":

            result = calculate_rref(val1)

            result_label.config(
                text="Result: RREF calculation complete."
            )

            nova.speak(
                "Reduced row echelon form calculated."
            )

            update_chat(
                f"\n{nova.name}:\n\n{result}\n"
            )

            return


        # ====================================================
        # EXISTING CALCULATIONS
        # ====================================================

        if "," in val1:

            val1 = np.array(
                [
                    float(x)
                    for x in val1.split(",")
                ]
            )

        else:

            val1 = float(val1)


        if "," in val2:

            val2 = np.array(
                [
                    float(x)
                    for x in val2.split(",")
                ]
            )

        else:

            val2 = float(val2)


        result = (
            functions[selected_function](val1, val2)
            if selected_function in functions
            else "Invalid selection"
        )


        result_label.config(
            text=f"Result: {result}"
        )

        nova.speak(
            f"Here’s the result: {result}"
        )

        update_chat(
            f"{nova.name}: Here’s the result: {result}"
        )


    except Exception as e:

        result_label.config(
            text="Invalid input. Please check your entries."
        )

        nova.speak(
            "Hmm... something didn’t add up. "
            "Want to double-check those numbers?"
        )

        update_chat(
            f"{nova.name}: Something went wrong: {str(e)}"
        )


# ============================================================
# MODE CONTROL
# ============================================================

def change_mode(event=None):

    selected_mode = mode_var.get().lower()

    nova.set_mode(selected_mode)

    update_chat(
        f"{nova.name} switched to "
        f"{selected_mode.capitalize()} Mode."
    )


# ============================================================
# CHAT OUTPUT
# ============================================================

def update_chat(message):

    chat_output.configure(
        state="normal"
    )

    chat_output.insert(
        tk.END,
        message + "\n"
    )

    chat_output.configure(
        state="disabled"
    )

    chat_output.see(
        tk.END
    )


# ============================================================
# APP INITIALIZATION
# ============================================================

nova.react_to_task("math")


# ============================================================
# AVAILABLE FUNCTIONS
# ============================================================

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

    "RREF": matrix_rref,

    "Mean": compute_mean,

    "Standard Deviation": compute_std,

    "Normal Distribution": normal_distribution,

    "Fourier Transform": fourier_transform,

    "Inverse Fourier Transform": inverse_fourier_transform
}


# ============================================================
# INPUT LABEL CONFIGURATION
# ============================================================

input_config = {

    "Add": [
        "Number 1",
        "Number 2"
    ],

    "Subtract": [
        "Number 1",
        "Number 2"
    ],

    "Multiply": [
        "Number 1",
        "Number 2"
    ],

    "Divide": [
        "Numerator",
        "Denominator"
    ],

    "Differentiate": [
        "Function f(x)",
        "Point x"
    ],

    "Integrate": [
        "Function f(x)",
        "Lower Limit, Upper Limit"
    ],

    "Matrix Multiply": [
        "Matrix A (comma-separated rows)",
        "Matrix B (comma-separated rows)"
    ],

    "Matrix Inverse": [
        "Matrix A (comma-separated rows)",
        ""
    ],

    "Matrix Determinant": [
        "Matrix A (comma-separated rows)",
        ""
    ],

    "Matrix Eigenvalues": [
        "Matrix A (comma-separated rows)",
        ""
    ],

    "RREF": [
        "Augmented Matrix: rows = ;   columns = ,",
        ""
    ],

    "Mean": [
        "Dataset (comma-separated)",
        ""
    ],

    "Standard Deviation": [
        "Dataset (comma-separated)",
        ""
    ],

    "Normal Distribution": [
        "x",
        "Mean, Standard Deviation"
    ],

    "Fourier Transform": [
        "Signal (comma-separated)",
        ""
    ],

    "Inverse Fourier Transform": [
        "Frequency Data (comma-separated)",
        ""
    ]
}


# ============================================================
# GUI SETUP
# ============================================================

root = tk.Tk()

root.title(
    "N.O.V.A. Physics & Math Assistant"
)


# ============================================================
# FUNCTION SELECTION
# ============================================================

function_var = tk.StringVar()

function_dropdown = ttk.Combobox(
    root,
    textvariable=function_var,
    width=40
)

function_dropdown["values"] = list(
    input_config.keys()
)

function_dropdown.set(
    "Select a calculation"
)

function_dropdown.grid(
    row=0,
    column=1,
    columnspan=2,
    padx=10,
    pady=10
)

function_dropdown.bind(
    "<<ComboboxSelected>>",
    update_inputs
)


# ============================================================
# INPUT FIELD 1
# ============================================================

label1 = tk.Label(
    root,
    text="Input 1:"
)

label1.grid(
    row=1,
    column=0
)

entry1 = tk.Text(
    root,
    height=6,
    width=60,
    font=("Consolas", 10)
)

entry1.grid(
    row=1,
    column=1,
    columnspan=2,
    padx=10,
    pady=5
)


# ============================================================
# INPUT FIELD 2
# ============================================================

label2 = tk.Label(
    root,
    text="Input 2:"
)

label2.grid(
    row=2,
    column=0
)

entry2 = tk.Entry(
    root,
    width=60
)

entry2.grid(
    row=2,
    column=1,
    columnspan=2,
    padx=10
)


# ============================================================
# CALCULATE BUTTON
# ============================================================

calculate_button = tk.Button(
    root,
    text="Calculate",
    command=calculate
)

calculate_button.grid(
    row=3,
    column=1,
    pady=10
)


# ============================================================
# RESULT DISPLAY
# ============================================================

result_label = tk.Label(
    root,
    text="Result: "
)

result_label.grid(
    row=4,
    column=1,
    pady=10
)


# ============================================================
# MODE SWITCH
# ============================================================

mode_var = tk.StringVar()

mode_dropdown = ttk.Combobox(
    root,
    textvariable=mode_var,
    width=20
)

mode_dropdown["values"] = [
    "Science",
    "Creative",
    "Chill"
]

mode_dropdown.set(
    "Science"
)

mode_dropdown.grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)

mode_dropdown.bind(
    "<<ComboboxSelected>>",
    change_mode
)


# ============================================================
# CHAT OUTPUT WINDOW
# ============================================================

chat_output = tk.Text(
    root,
    height=20,
    width=85,
    state="disabled",
    bg="#1e1e1e",
    fg="#d4d4d4",

    # Monospaced font keeps matrices aligned
    font=("Consolas", 10)
)

chat_output.grid(
    row=5,
    column=0,
    columnspan=3,
    padx=10,
    pady=10
)


# ============================================================
# LAUNCH
# ============================================================

update_chat(
    f"{nova.name} is online and ready in Science Mode."
)

root.mainloop()