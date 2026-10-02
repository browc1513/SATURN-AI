"""Desktop controls for the saved-project spectrum workflow."""

import os
from pathlib import Path
from queue import Empty, Queue
import tempfile
import threading
import tkinter as tk
from tkinter import filedialog, ttk
import webbrowser


def default_output_folder():
    base = Path(os.environ.get("LOCALAPPDATA", Path.home()))
    return base / "SATURN" / "analysis"


def generate_outputs(project_path, output_folder):
    """Generate reports without accessing Tkinter or opening a browser."""
    from data_analysis.spectrum_report import save_report
    from data_analysis.spectrum_viewer import save_viewer

    folder = Path(output_folder)
    folder.mkdir(parents=True, exist_ok=True)
    run = Path(tempfile.mkdtemp(prefix="spectra-", dir=folder))
    report_path = run / "spectra.json"
    viewer_path = run / "spectra.html"
    try:
        report = save_report(project_path, report_path)
        save_viewer(report_path, viewer_path)
    except Exception as error:
        raise RuntimeError(
            f"{error}\nOutput folder: {run}\n"
            "Any completed output files have been kept."
        ) from error

    return {
        "report": report_path,
        "viewer": viewer_path,
        "shots": len(report["shots"]),
        "spectra": sum(len(shot["spectra"]) for shot in report["shots"]),
    }


class AnalysisPanel:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("SATURN Data Analysis")
        self.window.geometry("720x420")
        self.window.minsize(560, 360)
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.closed = False
        self.busy = False
        self.viewer = None
        self.results = Queue()
        self.project_dialog = None
        self.project = tk.StringVar()
        self.output = tk.StringVar(value=str(default_output_folder()))
        self.status = tk.StringVar(value="Select a saved measurement project.")

        frame = ttk.Frame(self.window, padding=16)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(0, weight=1)

        ttk.Label(frame, text="Saved project (.json)").grid(
            row=0, column=0, sticky="w"
        )
        self.project_entry = ttk.Entry(frame, textvariable=self.project)
        self.project_entry.grid(row=1, column=0, sticky="ew", pady=(4, 12))
        self.project_button = ttk.Button(
            frame, text="Browse...", command=self.choose_project
        )
        self.project_button.grid(row=1, column=1, padx=(8, 0))

        ttk.Label(frame, text="Output folder").grid(
            row=2, column=0, sticky="w"
        )
        self.output_entry = ttk.Entry(frame, textvariable=self.output)
        self.output_entry.grid(row=3, column=0, sticky="ew", pady=(4, 12))
        self.output_button = ttk.Button(
            frame, text="Browse...", command=self.choose_output
        )
        self.output_button.grid(row=3, column=1, padx=(8, 0))

        buttons = ttk.Frame(frame)
        buttons.grid(row=4, column=0, columnspan=2, sticky="w", pady=8)
        self.new_project_button = ttk.Button(
            buttons, text="New Project...", command=self.new_project
        )
        self.new_project_button.pack(side="left", padx=(0, 8))
        self.generate_button = ttk.Button(
            buttons, text="Generate Spectra", command=self.start
        )
        self.generate_button.pack(side="left")
        self.open_button = ttk.Button(
            buttons, text="Open Viewer", command=self.open_viewer,
            state="disabled",
        )
        self.open_button.pack(side="left", padx=8)
        self.progress = ttk.Progressbar(frame, mode="indeterminate")
        self.progress.grid(row=5, column=0, columnspan=2, sticky="ew", pady=8)
        ttk.Label(
            frame, textvariable=self.status, wraplength=520, justify="left"
        ).grid(row=6, column=0, columnspan=2, sticky="w", pady=8)
        ttk.Label(
            frame,
            text="Exploratory voltage spectra; neutron origin unconfirmed.",
            wraplength=520,
        ).grid(row=7, column=0, columnspan=2, sticky="w", pady=8)

        self.controls = [
            self.project_entry, self.project_button,
            self.output_entry, self.output_button, self.generate_button,
            self.new_project_button,
        ]
        self.poll_id = self.window.after(100, self.poll)

    def new_project(self):
        from gui.project_dialog import ProjectDialog

        existing = self.project_dialog
        if existing is not None and not existing.closed:
            existing.window.deiconify()
            existing.window.lift()
            return
        folder = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "SATURN" / "projects"
        self.project_dialog = ProjectDialog(
            self.window, self.project_saved, folder
        )

    def project_saved(self, path):
        self.project.set(str(path))
        self.viewer = None
        self.open_button.configure(state="disabled")
        self.status.set("Project saved and selected. Ready to generate spectra.")

    def choose_project(self):
        initial = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "SATURN" / "projects"
        path = filedialog.askopenfilename(
            parent=self.window, title="Select saved analysis project",
            initialdir=str(initial if initial.exists() else Path.home()),
            filetypes=[("JSON project", "*.json")],
        )
        if path:
            self.project.set(path)
            self.viewer = None
            self.open_button.configure(state="disabled")
            self.status.set("Ready to generate spectra from the selected project.")

    def choose_output(self):
        path = filedialog.askdirectory(
            parent=self.window, title="Select output folder"
        )
        if path:
            self.output.set(path)

    def start(self):
        if self.busy:
            return
        project = self.project.get().strip()
        folder = self.output.get().strip()
        if not project or not folder:
            self.status.set("Choose a project and output folder first.")
            return
        self.busy = True
        self.viewer = None
        self.open_button.configure(state="disabled")
        for control in self.controls:
            control.configure(state="disabled")
        self.progress.start()
        self.status.set("Verifying sources and generating spectra...")
        threading.Thread(
            target=self.worker, args=(project, folder),
            daemon=True, name="SATURNDataAnalysis",
        ).start()

    def worker(self, project, folder):
        try:
            result = generate_outputs(project, folder)
        except Exception as error:
            self.results.put(("error", str(error)))
        else:
            self.results.put(("success", result))

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
                self.status.set(f"Generation failed:\n{result}")
            else:
                self.viewer = result["viewer"]
                self.open_button.configure(state="normal")
                self.status.set(
                    f'{result["shots"]} shots; {result["spectra"]} spectra.\n'
                    f'Report: {result["report"]}\nViewer: {result["viewer"]}'
                )
        self.poll_id = self.window.after(100, self.poll)

    def open_viewer(self):
        if self.viewer:
            try:
                opened = webbrowser.open(self.viewer.resolve().as_uri())
                if not opened:
                    self.status.set(f"Open this file in your browser:\n{self.viewer}")
            except Exception as error:
                self.status.set(f"Could not open browser: {error}\n{self.viewer}")

    def close(self):
        dialog = self.project_dialog
        if dialog is not None and not dialog.closed:
            if dialog.busy:
                self.status.set("Wait for project saving to finish before closing.")
                dialog.window.lift()
                return
            dialog.close()
        self.closed = True
        self.window.after_cancel(self.poll_id)
        self.window.destroy()


def open_analysis_panel(parent):
    existing = getattr(parent, "_analysis_panel", None)
    if existing is not None and not existing.closed:
        existing.window.deiconify()
        existing.window.lift()
        return existing
    panel = AnalysisPanel(parent)
    parent._analysis_panel = panel
    return panel
