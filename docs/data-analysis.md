# Data analysis workflow

Run commands from the SATURN-AI repository with its Python virtual environment activated.

## Inputs and project requirements

The importer supports the recorded SL1000 CSV format used by the reference shots. It does not provide a general CSV importer.

A saved project contains absolute source-file paths, SHA-256 hashes, a one-based reference sample, a display window, and named measurement windows.

Keep source CSV files unchanged and at their saved locations. Project loading rejects changed or missing sources. Current projects use provisional time alignment with zero time correction.

Spectrum and sensitivity generation require measurement windows inside the display window and fully covered by the recording. Sample selection includes the start boundary and excludes the stop boundary.

## Desktop workflow

Launch the desktop application:

```powershell
python .\gui\saturn_gui.py
```

Open its Data Analysis panel.

1. Use **New Project...** to select source CSV files and save reference-sample, display-window, baseline, and candidate-event settings. Alternatively, browse to an existing saved project.
2. Choose an output folder.
3. Use **Preview Raw Waveforms**, then **Open Viewer**, to inspect raw samples, provisional alignment, measurement windows, and measurements.
4. Use **Generate Spectra**, then **Open Viewer**, to compare the saved window spectra and voltage variances.
5. Use **Generate Window Sensitivity**, then **Open Viewer**, to inspect how shifted and wider windows affect the results.

Generation runs in a background worker. The default output folder is `%LOCALAPPDATA%\SATURN\analysis`. Each operation creates a separate run folder. Open Viewer opens the latest successful result.

Completed report files are retained if viewer generation fails. The error message identifies the run folder.

The spectrum viewer offers all-shot and individual-shot selection. Its table shows saved baseline and candidate-event voltage variances and their ratio. A zero baseline gives an undefined ratio; missing named windows display N/A.

## Command-line spectrum report and viewer

Supply a saved project and unused output filenames:

```powershell
& {
    $ErrorActionPreference = 'Stop'
    $project = 'C:\path\project.json'
    $report = 'C:\path\spectra.json'
    $viewer = 'C:\path\spectra.html'

    python -m data_analysis.spectrum_report --project $project --output $report
    if ($LASTEXITCODE -ne 0) { throw 'Spectrum report failed.' }

    python -m data_analysis.spectrum_viewer --report $report --output $viewer
    if ($LASTEXITCODE -ne 0) { throw 'Spectrum viewer failed.' }

    Start-Process $viewer
}
```

CLI commands use the supplied output paths. Existing output files are never overwritten.

To redisplay a saved report, run only the viewer command with a new HTML filename. Redisplay uses saved spectra and does not reverify the original CSV files.

## Command-line raw waveform preview

```powershell
python -m data_analysis.projects open --project "C:\path\project.json" --output "C:\path\raw-viewer.html"
```

This opens the raw waveform comparison using saved project settings and measurement windows. Choose a new output filename each time.

## Window sensitivity

For each saved measurement window, the sensitivity report calculates four variants:

| Variant | Boundaries |
| --- | --- |
| Original | Saved boundaries |
| Earlier | Shift both boundaries earlier by 20% of the original duration |
| Later | Shift both boundaries later by 20% of the original duration |
| Wider | Extend each boundary by 25% of the original duration |

All variants must fit within the display window and recorded waveform. Invalid variants cause generation to fail; they are not clipped.

```powershell
& {
    $ErrorActionPreference = 'Stop'
    $project = 'C:\path\project.json'
    $report = 'C:\path\sensitivity.json'
    $viewer = 'C:\path\sensitivity.html'

    python -m data_analysis.window_sensitivity --project $project --output $report
    if ($LASTEXITCODE -ne 0) { throw 'Sensitivity report failed.' }

    python -m data_analysis.sensitivity_viewer --report $report --output $viewer
    if ($LASTEXITCODE -ne 0) { throw 'Sensitivity viewer failed.' }

    Start-Process $viewer
}
```

The viewer selector chooses a shot and measurement window. Each selection displays four saved spectra and a matching table of boundaries, sample counts, voltage variances, and variance ratios relative to the original window.

A zero original variance gives an undefined ratio. Wider windows change sample count and frequency-bin spacing. Overlapping variants are not independent repeat measurements.

For three shots with two measurement windows each, the report contains six comparisons and 24 window results.

## Processing and provenance

Each selected window is processed separately:

- Subtract its mean voltage.
- Apply a rectangular window with no zero padding.
- Calculate a one-sided power spectral density in V^2/Hz.
- Verify that the sum of PSD bins times frequency-bin spacing matches AC RMS squared.

Reports preserve source and project provenance, requested boundaries, sample count, sampling information, removed mean, and processing choices.

HTML viewers embed Plotly and saved metadata for offline use. Spectrum viewers display frequency in MHz and PSD on a logarithmic axis. DC is omitted from the plot; zero-power bins appear as gaps. Tables use saved full-spectrum integrated power.

Raw previews preserve recorded voltage samples without smoothing or baseline subtraction.

Click legend entries to hide or show spectra. Double-click to isolate a trace. Scroll to zoom.

## Interpretation limits

These are exploratory measurements of recorded voltage. They do not establish neutron origin, correct the instrument response, or implement filtering or event detection.

Integrated spectral power is mean-subtracted voltage variance in V^2. Variance ratios are not neutron yield or signal-to-noise ratio.

Frequency-bin spacing is 1 / (sample count * sample interval). For 100 samples at 0.1 microseconds per sample, spacing is 100 kHz and Nyquist frequency is 5 MHz. A maximum at 0.1 MHz is the first nonzero bin, not by itself evidence of a characteristic oscillation.

Short rectangular windows can produce spectral leakage. Review raw waveform timing, baseline selection, and sensitivity to boundaries before choosing further processing. Neutron attribution requires supporting experimental evidence and detector characterization.

## Verification

Run the complete regression suite:

```powershell
python -m pytest -q
git diff --check
```

Manual desktop acceptance should cover project creation, raw preview, spectrum generation, sensitivity generation, and opening each result. Check that viewer selectors update both spectra and their corresponding tables.

The reference-shot spectrum acceptance check reproduced all six original spectra and processing metadata exactly. At the desktop sensitivity integration checkpoint, the full suite passed 621 tests with one skipped test.
