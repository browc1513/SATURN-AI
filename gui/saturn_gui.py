import sys
import os
import threading
import tkinter as tk


# Ensure project paths are accessible
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
)

sys.path.append(PROJECT_ROOT)


# ---------- Import S.A.T.U.R.N. ----------

from core.saturn_instance import get_saturn
from voice.speech_to_text import listen_once
from voice.text_to_speech import (
    speak_async,
    set_voice_enabled,
    is_voice_enabled,
)

saturn = get_saturn("saturn_config.json")

STARTUP_INTRODUCTION = (
    "S.A.T.U.R.N. is online and ready. "
    "Voice interface active."
)


# ============================================================
# GUI FUNCTIONS
# ============================================================

def process_query(query):
    """
    Send text directly to SATURN's central Language User Interface.

    Both typed input and speech recognition use this same function.
    """

    query = str(query).strip()

    if not query:
        return

    update_chat(
        f"\nYou:\n{query}\n"
    )

    try:
        result = saturn.handle_query(query)

        response = result.get(
            "response",
            "No response was generated."
        )

        update_chat(
            f"{saturn.name}:\n\n{response}\n"
        )

        speak_async(
            response
        )

    except Exception as error:
        update_chat(
            f"{saturn.name}:\n\n"
            f"Something went wrong while processing "
            f"your request:\n{error}\n"
        )

    query_entry.focus_set()


def submit_query(event=None):
    """
    Submit text currently in the chat entry box.
    """

    query = query_var.get().strip()

    if not query:
        return

    query_var.set("")

    process_query(
        query
    )


# ============================================================
# PUSH-TO-TALK
# ============================================================

def start_push_to_talk():
    """
    Start one microphone listening session in a background thread.

    The GUI remains responsive while SATURN listens.
    """

    if mic_button.cget("state") == "disabled":
        return

    mic_button.configure(
        state="disabled",
        text="Listening..."
    )

    query_entry.configure(
        state="disabled"
    )

    threading.Thread(
        target=_push_to_talk_worker,
        daemon=True,
        name="SATURNPushToTalk",
    ).start()


def _push_to_talk_worker():
    """
    Perform speech recognition away from Tkinter's GUI thread.
    """

    result = listen_once()

    root.after(
        0,
        lambda: _finish_push_to_talk(
            result
        )
    )


def _finish_push_to_talk(result):
    """
    Return the microphone result to the Tkinter thread.
    """

    mic_button.configure(
        state="normal",
        text="🎤 Talk"
    )

    query_entry.configure(
        state="normal"
    )

    if not result.get(
        "success",
        False,
    ):
        update_chat(
            f"{saturn.name}:\n\n"
            f"{result.get('response', 'I could not understand the microphone input.')}\n"
        )

        query_entry.focus_set()
        return

    transcript = result.get(
        "text",
        ""
    ).strip()

    if not transcript:
        query_entry.focus_set()
        return

    # Show exactly what speech recognition heard and route it through
    # the same SATURN.handle_query() path used by typed messages.
    query_var.set(
        transcript
    )

    root.update_idletasks()

    submit_query()


# ============================================================
# TEXT-TO-SPEECH CONTROL
# ============================================================

def toggle_voice():
    """
    Enable or disable spoken SATURN responses.
    """

    new_state = not is_voice_enabled()

    set_voice_enabled(
        new_state
    )

    if new_state:
        voice_button.configure(
            text="🔊 Voice: On"
        )
    else:
        voice_button.configure(
            text="🔇 Voice: Off"
        )


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

voice_button = tk.Button(
    input_frame,
    text="🔊 Voice: On",
    command=toggle_voice,
    font=("Consolas", 11),
    padx=12,
    pady=8
)

voice_button.pack(
    side="left",
    padx=(0, 8)
)

mic_button = tk.Button(
    input_frame,
    text="🎤 Talk",
    command=start_push_to_talk,
    font=("Consolas", 11),
    padx=14,
    pady=8
)

mic_button.pack(
    side="left",
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
    STARTUP_INTRODUCTION
)

speak_async(
    STARTUP_INTRODUCTION
)

query_entry.focus_set()


# ============================================================
# LAUNCH
# ============================================================

root.mainloop()
