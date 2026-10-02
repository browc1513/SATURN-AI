# Data analysis workflow

Run commands from the SATURN-AI repository with its Python virtual environment activated.

## Inputs and project requirements

The current importer supports the recorded SL1000 CSV format used by the reference shots. It does not provide a general CSV importer.

A saved analysis project contains absolute source-file paths, SHA-256 hashes, a one-based reference sample, a display window, and optional named measurement windows.

Spectrum generation requires at least one measurement window. Each window must fit within the project's display window and be fully covered by the recorded waveform. Selection includes the start boundary and excludes the stop boundary.

Keep source CSV files unchanged and at their saved locations. Project loading rejects changed or missing sources. Current projects use provisional time alignment with zero time correction.

## Generate a spectrum report and viewer

Use your saved measurement project. This example uses the verified reference-shot project on this PC:

```powershell
& {
    $ErrorActionPreference = 'Stop'
    $folder = Join-Path $env:LOCALAPPDATA 'SATURN\projects'
    $project = Join-Path $folder 'neutron-measurement-project-20260930-171348.json'
    $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $report = Join-Path $folder "spectra-$stamp.json"
    $viewer = Join-Path $folder "spectra-$stamp.html"

    python -m data_analysis.spectrum_report --project $project --output $report
    if ($LASTEXITCODE -ne 0) { throw 'Spectrum report failed.' }

    python -m data_analysis.spectrum_viewer --report $report --output $viewer
    if ($LASTEXITCODE -ne 0) { throw 'Spectrum viewer failed.' }

    Start-Process $viewer
}
```

Change the project filename to analyze another saved project. Output files are created at the paths supplied by the caller; the commands do not choose a storage folder automatically. Existing output files are never overwritten.

To redisplay a previously saved report, run only the spectrum_viewer command with a new HTML output filename. Redisplay uses saved spectra and does not reverify the original CSV files.

## Inspect the raw waveform

```powershell
python -m data_analysis.projects open --project "C:\path\project.json" --output "C:\path\raw-viewer.html"
```

This reopens the raw waveform comparison with the project's saved measurement windows. Choose a new output filename each time.

## Processing and provenance

Each selected window is processed separately:

- Subtract its mean voltage.
- Apply a rectangular window with no zero padding.
- Calculate a one-sided power spectral density in V?/Hz.
- Verify that the sum of PSD bins times frequency-bin spacing matches AC RMS squared.

The report records source hashes and paths, time-reference settings, requested window boundaries, sample count, sample interval, sample rate, frequency spacing, removed mean, and processing choices.

The HTML viewer embeds Plotly and the saved report metadata. It displays frequency in MHz on a linear axis and PSD on a logarithmic axis. DC is omitted; zero-power bins appear as gaps. Baseline traces are dashed and candidate-event traces are solid. Matching shot colors repeat when more than three shots are displayed.

Click a legend entry to hide or show a trace. Double-click to isolate one trace. Scroll to zoom.

## Interpretation limits

These are exploratory spectra of recorded voltage. They do not establish neutron origin, correct the instrument response, or implement filtering or event detection.

Integrated spectral power is voltage variance in V?, not electrical power in watts or neutron yield.

Frequency-bin spacing is 1 / (sample count ? sample interval). For the verified 100-sample windows at 0.1 microseconds per sample, spacing is 100 kHz and Nyquist frequency is 5 MHz. A maximum at 0.1 MHz is the first nonzero bin, not by itself evidence of a characteristic oscillation.

Short rectangular windows can produce spectral leakage. Compare raw waveforms, window selection, and repeatability before choosing filters.

## Verification

```powershell
python -m pytest -q tests/test_analysis_spectra.py tests/test_analysis_spectrum_report.py tests/test_analysis_spectrum_viewer.py
```

The reference-shot acceptance check reproduced all six original spectra and processing metadata exactly. The full suite at that checkpoint passed 573 tests with one skipped test.
