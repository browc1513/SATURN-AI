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

RENAME_TARGETS = {}

RENAME_TARGETS = {
    "saturn_config.json": "saturn_config.json",
    "saturn_instance.py": "saturn_instance.py",
    "saturn_personality.py": "saturn_personality.py",
    "saturn_gui.py": "saturn_gui.py",
}


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def replace_text_in_files():
    print("\n=== UPDATING FILE CONTENTS ===")

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
            path.write_text(updated_text, encoding="utf-8")
            print(f"Updated: {path.relative_to(PROJECT_ROOT)}")


def rename_files():
    print("\n=== RENAMING FILES ===")

    paths_to_rename = []

    for path in PROJECT_ROOT.rglob("*"):
        if should_skip(path):
            continue

        if path.is_file() and path.name in RENAME_TARGETS:
            paths_to_rename.append(path)

    for path in paths_to_rename:
        new_name = RENAME_TARGETS[path.name]
        new_path = path.with_name(new_name)

        if new_path.exists():
            raise FileExistsError(
                f"Cannot rename {path} because {new_path} already exists."
            )

        path.rename(new_path)

        print(
            f"Renamed: {path.relative_to(PROJECT_ROOT)}"
            f" -> {new_path.relative_to(PROJECT_ROOT)}"
        )


def main():
    print("Starting SATURN -> SATURN migration")
    print(f"Project root: {PROJECT_ROOT}")

    replace_text_in_files()
    rename_files()

    print("\nMIGRATION COMPLETE")


if __name__ == "__main__":
    main()