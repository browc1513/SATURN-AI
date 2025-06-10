import json
import random
import os

class NOVA:
    def __init__(self, config_path="nova_config.json"):
        self.name = "N.O.V.A."
        self.mode = "science"
        self.voice_enabled = False  # You can add TTS later
        self.load_config(config_path)

    def load_config(self, config_path):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"N.O.V.A. config not found at: {config_path}")
        
        with open(config_path, "r") as f:
            config = json.load(f)

        self.name = config.get("name", "N.O.V.A.")
        self.mode = config.get("mode", "science")
        self.personality_traits = config.get("personality_traits", {})
        self.references = config.get("pop_culture_references", {})
        self.reference_frequency = config.get("reference_frequency", "occasional")

    def speak(self, message):
        print(f"{self.name}: {message}")

    def react_to_task(self, task_type):
        task_type = task_type.lower()
        if task_type in ["math", "physics", "science"]:
            self.set_mode("science")
        elif task_type in ["art", "film", "music", "writing"]:
            self.set_mode("creative")
        elif task_type in ["relax", "chill", "vibe"]:
            self.set_mode("chill")

    def set_mode(self, mode_name):
        mode_name = mode_name.lower()
        valid_modes = ["science", "creative", "chill"]
        if mode_name in valid_modes:
            self.mode = mode_name
            self.speak(f"Switched to {mode_name.capitalize()} Mode!")
        else:
            self.speak(f"I don’t recognize '{mode_name}' as a valid mode.")

    def random_reference(self):
        sources = []
        for key, value in self.references.items():
            if isinstance(value, list):
                sources.extend(value)
        if sources:
            return random.choice(sources)
        return None

    def say(self, message):
        reference = self.random_reference()
        if reference:
            return f"{self.name}: {message} (btw, remember {reference})"
        return f"{self.name}: {message}"
