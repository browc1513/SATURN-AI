"""Create saved analysis projects without blocking the desktop interface."""

import math
from pathlib import Path
from queue import Empty, Queue
import threading
import tkinter as tk
from tkinter import filedialog, ttk


def create_project(destination, paths, fields):
    """Parse form values and use the existing source-verifying project writer."""
    from data_analysis.projects import save_project

    name = fields["name"].strip()
    if not name:
        raise ValueError("Enter a project name.")
    if not paths:
        raise ValueError("Select at least one CSV file.")

    try:
        reference = int(fields["reference"].strip())
    except ValueError as error:
        raise ValueError("Reference sample must be a positive whole number.") from error
    if reference < 1:
        raise ValueError("Reference sample must be a positive whole number.")

    numbers = {}
    for key in (
        "display_start", "display_stop", "baseline_start",
        "baseline_stop", "event_start", "event_stop",
    ):
        try:
            value = float(fields[key])
        except ValueError as error:
            raise ValueError("Time boundaries must be finite numbers.") from error
        if not math.isfinite(value):
            raise ValueError("Time boundaries must be finite numbers.")
        numbers[key] = value

    return save_project(
        destination, name, paths,
        reference_sample=reference,
        start_us=numbers["display_start"],
        stop_us=numbers["display_stop"],
        measurement_windows={
            "Baseline": [numbers["baseline_start"], numbers["baseline_stop"]],
            "Candidate event": [numbers["event_start"], numbers["event_stop"]],
        },
    )


class ProjectDialog:
    def __init__(self, parent, on_saved, initial_folder):
        self.window = tk.Toplevel(parent)
        self.window.title("New Analysis Project")
        self.window.geometry("700x650")
        self.window.minsize(620, 620)
        self.window.transient(parent)
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.on_saved = on_saved
        self.initial_folder = Path(initial_folder)
        self.paths = []
        self.busy = False
        self.closed = False
        self.results = Queue()
        self.controls = []
        self.fields = {}
        self.status = tk.StringVar(value="Select the recorded CSV files.")

        frame = ttk.Frame(self.window, padding=16)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(1, weight=1)

        source_button = ttk.Button(
            frame, text="Select CSV Files...", command=self.choose_sources
        )
        source_button.grid(row=0, column=0, sticky="w")
        self.controls.append(source_button)
        self.sources = tk.Listbox(frame, height=5)
        self.sources.grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=(8, 12)
        )

        definitions = [
            ("name", "Project name", "Neutron measurement comparison"),
            ("reference", "Reference sample (one-based)", "801250"),
            ("display_start", "Display start (µs)", "-50"),
            ("display_stop", "Display stop (µs)", "100"),
            ("baseline_start", "Baseline start (µs)", "-30"),
            ("baseline_stop", "Baseline stop (µs)", "-20"),
            ("event_start", "Candidate event start (µs)", "20"),
            ("event_stop", "Candidate event stop (µs)", "30"),
        ]
        for row, (key, label, default) in enumerate(definitions, start=2):
            ttk.Label(frame, text=label).grid(
                row=row, column=0, sticky="w", padx=(0, 12), pady=4
            )
            variable = tk.StringVar(value=default)
            self.fields[key] = variable
            entry = ttk.Entry(frame, textvariable=variable)
            entry.grid(row=row, column=1, sticky="ew", pady=4)
            self.controls.append(entry)

        ttk.Label(
            frame,
            text=(
                "Time zero uses the selected sample for every shot and remains "
                "provisional. Windows include their start and exclude their stop."
            ),
            wraplength=620, justify="left",
        ).grid(row=10, column=0, columnspan=2, sticky="w", pady=12)

        save_button = ttk.Button(
            frame, text="Save Project...", command=self.start
        )
        save_button.grid(row=11, column=0, sticky="w", pady=4)
        self.controls.append(save_button)
        self.progress = ttk.Progressbar(frame, mode="indeterminate")
        self.progress.grid(
            row=12, column=0, columnspan=2, sticky="ew", pady=8
        )
        ttk.Label(
            frame, textvariable=self.status, wraplength=620, justify="left"
        ).grid(row=13, column=0, columnspan=2, sticky="w")
        self.poll_id = self.window.after(100, self.poll)

    def choose_sources(self):
        paths = filedialog.askopenfilenames(
            parent=self.window, title="Select recorded shot CSV files",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if paths:
            self.paths = list(paths)
            self.sources.delete(0, tk.END)
            for path in self.paths:
                self.sources.insert(tk.END, path)
            self.status.set(f"{len(self.paths)} files selected.")

    def start(self):
        if self.busy:
            return
        if not self.paths:
            self.status.set("Select at least one CSV file first.")
            return
        destination = filedialog.asksaveasfilename(
            parent=self.window, title="Save analysis project",
            initialdir=str(
                self.initial_folder
                if self.initial_folder.exists() else Path.home()
            ),
            initialfile="measurement-project.json",
            defaultextension=".json",
            filetypes=[("JSON project", "*.json")],
        )
        if not destination:
            return
        if Path(destination).exists():
            self.status.set("That file already exists. Choose a new filename.")
            return

        fields = {key: variable.get() for key, variable in self.fields.items()}
        paths = tuple(self.paths)
        self.busy = True
        for control in self.controls:
            control.configure(state="disabled")
        self.progress.start()
        self.status.set("Checking settings and verifying source files...")
        threading.Thread(
            target=self.worker, args=(destination, paths, fields),
            daemon=True, name="SATURNProjectCreation",
        ).start()

    def worker(self, destination, paths, fields):
        try:
            record = create_project(destination, paths, fields)
        except Exception as error:
            self.results.put(("error", str(error)))
        else:
            self.results.put(("saved", (Path(destination), record)))

    def poll(self):
        if self.closed:
            return
        try:
            kind, result = self.results.get_nowait()
        except Empty:
            pass
        else:
            self.busy = False
            self.progress.stop()
            for control in self.controls:
                control.configure(state="normal")
            if kind == "error":
                self.status.set(f"Project was not saved:\n{result}")
            else:
                destination, record = result
                self.on_saved(destination)
                self.status.set(
                    f'Saved {len(record["shots"])} shots:\n{destination}\n'
                    "You can now generate spectra in the analysis panel."
                )
        self.poll_id = self.window.after(100, self.poll)

    def close(self):
        if self.busy:
            self.status.set("Wait for source verification and saving to finish.")
            return
        self.closed = True
        self.window.after_cancel(self.poll_id)
        self.window.destroy()
