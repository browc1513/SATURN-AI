import sys
import os
import tkinter as tk
from tkinter import ttk

import numpy as np
from scipy.stats import norm
from numpy.fft import fft, ifft
from sympy import Matrix, sympify, pretty


# Ensure project paths are accessible
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
)

sys.path.append(PROJECT_ROOT)


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

from math_engine.math_pipeline import interpret_and_execute_math


# ---------- Veterinary Imports ----------

from veterinary_subsystem.clinical_search import (
    search_veterinary_database,
    format_veterinary_results
)

from veterinary_subsystem.database_loader import (
    load_veterinary_database
)


# ============================================================
# FILE PATHS
# ============================================================

VETERINARY_DATABASE_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "Pathophysiology Guide.xlsx"
)


# ============================================================
# VETERINARY DATABASE HELPERS
# ============================================================

def get_species_options():
    """
    Read all unique species from the veterinary database.

    Species stored in pipe-delimited form such as:
        cattle|swine

    are separated into individual dropdown options.
    """

    try:
        workbook = load_veterinary_database(
            VETERINARY_DATABASE_PATH
        )

        guide = workbook["Guide"]

        species = set()

        if "host_species" in guide.columns:

            for value in guide["host_species"].dropna():

                for item in str(value).split("|"):

                    item = item.strip()

                    if item:
                        species.add(
                            item.capitalize()
                        )

        return [
            "Any Species",
            *sorted(species)
        ]

    except Exception:
        # Keep the GUI usable even if the workbook
        # cannot be loaded during startup.
        return [
            "Any Species"
        ]


# ============================================================
# GUI FUNCTIONS
# ============================================================

def _format_math_response(result):
    """
    Convert a universal math-pipeline result into readable GUI text.
    """

    if not result.get("success"):

        error = result.get(
            "error",
            "NOVA could not complete the math request."
        )

        stage = result.get("stage")

        if stage:
            return (
                f"I couldn't complete that request.\n\n"
                f"Stage: {stage}\n"
                f"Error: {error}"
            )

        return (
            f"I couldn't complete that request.\n\n"
            f"Error: {error}"
        )

    lines = []

    steps = result.get(
        "steps",
        []
    )

    for index, step in enumerate(
        steps,
        start=1,
    ):
        lines.append(
            f"{index}. {step}"
        )

    exact_result = result.get(
        "exact_result"
    )

    decimal_result = result.get(
        "decimal_result"
    )

    if lines:
        lines.append("")

    lines.append(
        f"Exact Answer: {exact_result}"
    )

    if (
        decimal_result is not None
        and str(decimal_result) != str(exact_result)
    ):
        lines.append(
            f"Decimal Answer: {decimal_result}"
        )

    warnings = result.get(
        "warnings",
        []
    )

    if warnings:

        lines.append("")

        for warning in warnings:
            lines.append(
                f"Warning: {warning}"
            )

    return "\n".join(lines)


def submit_math_query(event=None):
    """
    Send the user's natural-language math question through
    NOVA's universal math pipeline and display the response.
    """

    query = math_query_var.get().strip()

    if not query:
        return

    update_chat(
        f"\nYou:\n{query}\n"
    )

    math_query_var.set("")

    try:

        result = interpret_and_execute_math(
            query
        )

        response = _format_math_response(
            result
        )

        update_chat(
            f"{nova.name}:\n\n{response}\n"
        )

    except Exception as error:

        response = (
            f"Something went wrong while processing "
            f"the math request:\n{error}"
        )

        update_chat(
            f"{nova.name}:\n\n{response}\n"
        )


def submit_veterinary_query(event=None):
    """
    Search the veterinary database using clinical keywords
    and an optional species filter.
    """

    query = veterinary_query_var.get().strip()

    if not query:
        return

    selected_species = veterinary_species_var.get().strip()

    structured_filters = None

    if (
        selected_species
        and selected_species != "Any Species"
    ):
        structured_filters = {
            "host_species": selected_species.lower()
        }

    if selected_species == "Any Species":
        search_header = query

    else:
        search_header = (
            f"{query}\n"
            f"Species: {selected_species}"
        )

    update_chat(
        f"\nVeterinary Search:\n"
        f"{search_header}\n"
    )

    veterinary_query_var.set("")

    try:

        results = search_veterinary_database(
            VETERINARY_DATABASE_PATH,
            query,
            structured_filters=structured_filters
        )

        response = format_veterinary_results(
            results
        )

        update_chat(
            f"{nova.name} Veterinary Results:\n\n"
            f"{response}\n"
        )

    except Exception as error:

        response = (
            f"Something went wrong while searching "
            f"the veterinary database:\n{error}"
        )

        update_chat(
            f"{nova.name}:\n\n{response}\n"
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
# GUI SETUP
# ============================================================

root = tk.Tk()

root.title(
    "N.O.V.A. Physics, Math & Veterinary Assistant"
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
# NATURAL-LANGUAGE MATH QUERY
# ============================================================

math_query_var = tk.StringVar()

math_query_label = tk.Label(
    root,
    text="Ask NOVA a math question:"
)

math_query_label.grid(
    row=1,
    column=0,
    padx=10,
    pady=(10, 5),
    sticky="w"
)

math_query_entry = tk.Entry(
    root,
    textvariable=math_query_var,
    width=70,
    font=("Consolas", 11)
)

math_query_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=(10, 5),
    sticky="ew"
)

ask_button = tk.Button(
    root,
    text="Ask NOVA",
    command=submit_math_query
)

ask_button.grid(
    row=1,
    column=2,
    padx=10,
    pady=(10, 5)
)

math_query_entry.bind(
    "<Return>",
    submit_math_query
)


# ============================================================
# VETERINARY KEYWORD SEARCH
# ============================================================

veterinary_query_var = tk.StringVar()

veterinary_query_label = tk.Label(
    root,
    text="Veterinary keywords:"
)

veterinary_query_label.grid(
    row=2,
    column=0,
    padx=10,
    pady=5,
    sticky="w"
)

veterinary_query_entry = tk.Entry(
    root,
    textvariable=veterinary_query_var,
    width=70,
    font=("Consolas", 11)
)

veterinary_query_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=5,
    sticky="ew"
)


# ---------- Species Selector ----------

veterinary_species_var = tk.StringVar()

veterinary_species_dropdown = ttk.Combobox(
    root,
    textvariable=veterinary_species_var,
    width=15,
    state="readonly"
)

veterinary_species_dropdown["values"] = (
    get_species_options()
)

veterinary_species_dropdown.set(
    "Any Species"
)

veterinary_species_dropdown.grid(
    row=2,
    column=2,
    padx=5,
    pady=5
)


# ---------- Veterinary Search Button ----------

veterinary_search_button = tk.Button(
    root,
    text="Search Vet DB",
    command=submit_veterinary_query
)

veterinary_search_button.grid(
    row=2,
    column=3,
    padx=10,
    pady=5
)

veterinary_query_entry.bind(
    "<Return>",
    submit_veterinary_query
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
    row=3,
    column=0,
    columnspan=4,
    padx=10,
    pady=10,
    sticky="nsew"
)


# ============================================================
# WINDOW SCALING
# ============================================================

root.grid_columnconfigure(
    1,
    weight=1
)

root.grid_rowconfigure(
    3,
    weight=1
)


# Start with the math field selected.

math_query_entry.focus_set()


# ============================================================
# LAUNCH
# ============================================================

update_chat(
    f"{nova.name} is online and ready in Science Mode."
)

root.mainloop()