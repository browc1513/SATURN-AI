from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".pytest_cache",
}

TEXT_EXTENSIONS = {
    ".py",
    ".json",
    ".md",
    ".txt",
    ".csv",
}

REPLACEMENTS = [
    ("get_nova", "get_saturn"),
    ("NOVA", "SATURN"),
    ("nova", "saturn"),
]

RENAME_TARGETS = {
    "nova_config.json": "saturn_config.json",
    "nova_instance.py": "saturn_instance.py",
    "nova_personality.py": "saturn_personality.py",
    "nova_gui.py": "saturn_gui.py",
}


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def preview_file_renames():
    print("\n=== FILE RENAME PREVIEW ===")

    for path in PROJECT_ROOT.rglob("*"):
        if should_skip(path):
            continue

        if path.is_file() and path.name in RENAME_TARGETS:
            new_name = RENAME_TARGETS[path.name]
            new_path = path.with_name(new_name)

            print(f"{path.relative_to(PROJECT_ROOT)}")
            print(f"  -> {new_path.relative_to(PROJECT_ROOT)}")


def preview_text_replacements():
    print("\n=== TEXT REPLACEMENT PREVIEW ===")

    for path in PROJECT_ROOT.rglob("*"):
        if should_skip(path):
            continue

        if not path.is_file():
            continue

        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue

        try:
            original_text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        updated_text = original_text

        for old, new in REPLACEMENTS:
            updated_text = updated_text.replace(old, new)

        if updated_text != original_text:
            print(path.relative_to(PROJECT_ROOT))


def main():
    print("SATURN migration dry run")
    print(f"Project root: {PROJECT_ROOT}")

    preview_file_renames()
    preview_text_replacements()

    print("\nDRY RUN COMPLETE")
    print("No files were changed.")


if __name__ == "__main__":
    main()