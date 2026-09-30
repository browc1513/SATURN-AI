"""Read-only validation of Yokogawa SL1000 single-trace CSV exports."""

import csv
import hashlib
import io
import math
from dataclasses import asdict, dataclass
from pathlib import Path


class SL1000FormatError(ValueError):
    """The file does not match the supported SL1000 export format."""


@dataclass(frozen=True)
class ShotSummary:
    filename: str
    sha256: str
    model: str
    trace_name: str
    recorded_date: str
    recorded_time: str
    voltage_unit: str
    time_unit: str
    sample_interval_seconds: float
    declared_samples: int
    actual_samples: int
    duration_seconds: float
    min_voltage: float
    max_voltage: float

    def to_dict(self):
        return asdict(self)


def inspect_sl1000(path, *, max_samples=10_000_000):
    """Stream a file once, validating metadata, values and its SHA-256 digest.

    This reader assumes consecutive samples beginning at file-relative t=0.
    The instrument trigger position and any event-relative time are unknown.
    """
    path = Path(path)
    digest = hashlib.sha256()
    count = 0
    minimum = math.inf
    maximum = -math.inf

    with path.open("rb") as raw:
        with io.TextIOWrapper(io.BufferedReader(HashingReaderIO(raw, digest)),
                              encoding="utf-8-sig", newline="") as stream:
            rows = csv.reader(stream)
            expected = ("Model", "BlockNumber", "TraceName", "BlockSize",
                        "Date", "Time", "VUnit", "HResolution", "HUnit")
            metadata = {}
            for key in expected:
                row = next(rows, None)
                if row is None or len(row) < 2 or row[0] != key:
                    raise SL1000FormatError(f"Expected {key} metadata row.")
                metadata[key] = row[1].strip()

            if metadata["Model"] != "SL1000" or metadata["BlockNumber"] != "1":
                raise SL1000FormatError("Only single-block SL1000 exports are supported.")
            if metadata["VUnit"] != "V" or metadata["HUnit"] != "s":
                raise SL1000FormatError("Expected volts and seconds; conversion is not configured.")
            try:
                declared = int(metadata["BlockSize"])
                interval = float(metadata["HResolution"])
            except ValueError as error:
                raise SL1000FormatError("Invalid sample count or interval.") from error
            if not (0 < declared <= max_samples and math.isfinite(interval) and interval > 0):
                raise SL1000FormatError("Sample count or interval outside supported limits.")

            for row in rows:
                if len(row) < 2 or row[0].strip():
                    raise SL1000FormatError(f"Malformed sample row {count + 1}.")
                try:
                    value = float(row[1])
                except ValueError as error:
                    raise SL1000FormatError(f"Invalid sample {count + 1}.") from error
                if not math.isfinite(value):
                    raise SL1000FormatError(f"Nonfinite sample {count + 1}.")
                count += 1
                if count > declared:
                    raise SL1000FormatError("More samples than BlockSize declares.")
                minimum = min(minimum, value)
                maximum = max(maximum, value)

    if count != declared:
        raise SL1000FormatError(f"Expected {declared} samples; found {count}.")
    return ShotSummary(
        filename=path.name, sha256=digest.hexdigest(), model=metadata["Model"],
        trace_name=metadata["TraceName"], recorded_date=metadata["Date"],
        recorded_time=metadata["Time"], voltage_unit=metadata["VUnit"],
        time_unit=metadata["HUnit"], sample_interval_seconds=interval,
        declared_samples=declared, actual_samples=count,
        duration_seconds=(count - 1) * interval,
        min_voltage=minimum, max_voltage=maximum,
    )


class HashingReaderIO(io.RawIOBase):
    def __init__(self, source, digest):
        self.source = source
        self.digest = digest

    def readable(self):
        return True

    def readinto(self, buffer):
        count = self.source.readinto(buffer)
        if count:
            self.digest.update(memoryview(buffer)[:count])
        return count
