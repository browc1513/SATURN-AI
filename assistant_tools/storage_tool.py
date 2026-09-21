"""
Shared persistent JSON storage for SATURN.

Provides cross-process locking and atomic JSON writes.
"""

import json
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path

from filelock import FileLock


@contextmanager
def storage_transaction(path, timeout=10):
    """
    Hold a cross-process lock for an entire read-modify-write
    transaction. Callers must load, modify, and save while
    inside this context.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lock = FileLock(str(path) + ".lock", timeout=timeout)

    with lock:
        yield


def atomic_save_json(path, data):
    """
    Write JSON to a temporary file, then atomically replace
    the destination. Call while holding storage_transaction.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=path.name + ".",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = temporary_file.name

            json.dump(
                data,
                temporary_file,
                indent=2,
                ensure_ascii=False,
            )

            temporary_file.write("\n")
            temporary_file.flush()
            os.fsync(temporary_file.fileno())

        os.replace(temporary_path, path)

    finally:
        if temporary_path is not None:
            try:
                os.unlink(temporary_path)
            except FileNotFoundError:
                pass
