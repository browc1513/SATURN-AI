import os
import sys


# Add the SATURN-AI project root to Python's import path.
PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(
        0,
        PROJECT_ROOT,
    )


from voice.text_to_speech import get_available_voices


voices = get_available_voices()

if not voices:
    print("No voices were detected.")

else:
    print("Installed SATURN-compatible voices:\n")

    for voice in voices:
        print(
            f"[{voice['index']}] "
            f"{voice['name']}"
        )

        print(
            f"    ID: {voice['id']}"
        )

        print(
            f"    Gender: {voice['gender']}"
        )

        print(
            f"    Age: {voice['age']}"
        )

        print()