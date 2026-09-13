import sys
import os
import tkinter as tk


# Ensure project paths are accessible
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
)

sys.path.append(PROJECT_ROOT)


# ---------- Import S.A.T.U.R.N. ----------

from core.saturn_instance import get_saturn

saturn = get_saturn("saturn_config.json")


# ============================================================
# GUI FUNCTIONS
# ============================================================

def submit_query(event=None):
    """
    Send the user's text directly to SATURN's central
    Language User Interface.
    """

    query = query_var.get().strip()

    if not query:
        return

    update_chat(
        f"\nYou:\n{query}\n"
    )

    query_var.set("")

    try:
        result = saturn.handle_query(query)

        response = result.get(
            "response",
            "No response was generated."
        )

        update_chat(
            f"{saturn.name}:\n\n{response}\n"
        )

    except Exception as error:
        update_chat(
            f"{saturn.name}:\n\n"
            f"Something went wrong while processing "
            f"your request:\n{error}\n"
        )

    query_entry.focus_set()


# ============================================================
# CHAT OUTPUT
# ============================================================

def update_chat(message):
    chat_output.configure(state="normal")
    chat_output.insert(tk.END, message + "\n")
    chat_output.configure(state="disabled")
    chat_output.see(tk.END)


# ============================================================
# APP INITIALIZATION
# ============================================================

root = tk.Tk()

root.title("S.A.T.U.R.N.")
root.geometry("900x650")
root.minsize(650, 450)


# ============================================================
# MAIN CONTAINER
# ============================================================

main_frame = tk.Frame(
    root,
    bg="#1e1e1e"
)

main_frame.pack(
    fill="both",
    expand=True
)


# ============================================================
# CHAT OUTPUT WINDOW
# ============================================================

chat_frame = tk.Frame(
    main_frame,
    bg="#1e1e1e"
)

chat_frame.pack(
    fill="both",
    expand=True,
    padx=12,
    pady=(12, 6)
)

chat_scrollbar = tk.Scrollbar(chat_frame)
chat_scrollbar.pack(
    side="right",
    fill="y"
)

chat_output = tk.Text(
    chat_frame,
    state="disabled",
    wrap="word",
    bg="#1e1e1e",
    fg="#d4d4d4",
    insertbackground="#ffffff",
    font=("Consolas", 11),
    padx=12,
    pady=12,
    relief="flat",
    borderwidth=0,
    yscrollcommand=chat_scrollbar.set
)

chat_output.pack(
    side="left",
    fill="both",
    expand=True
)

chat_scrollbar.configure(
    command=chat_output.yview
)


# ============================================================
# QUERY INPUT AREA
# ============================================================

input_frame = tk.Frame(
    main_frame,
    bg="#1e1e1e"
)

input_frame.pack(
    fill="x",
    padx=12,
    pady=(6, 12)
)

query_var = tk.StringVar()

query_entry = tk.Entry(
    input_frame,
    textvariable=query_var,
    font=("Consolas", 12),
    bg="#2d2d2d",
    fg="#ffffff",
    insertbackground="#ffffff",
    relief="flat",
    borderwidth=0
)

query_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=10,
    padx=(0, 8)
)

send_button = tk.Button(
    input_frame,
    text="Send",
    command=submit_query,
    font=("Consolas", 11),
    padx=18,
    pady=8
)

send_button.pack(
    side="right"
)

query_entry.bind(
    "<Return>",
    submit_query
)


# ============================================================
# STARTUP MESSAGE
# ============================================================

update_chat(
    f"{saturn.name} is online and ready."
)

query_entry.focus_set()


# ============================================================
# LAUNCH
# ============================================================

root.mainloop()
