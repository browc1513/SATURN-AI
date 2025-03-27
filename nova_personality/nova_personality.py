import json
import random
from datetime import datetime

class NOVA:
    def __init__(self, config_path="nova_config.json"):
        with open(config_path, "r") as f:
            self.config = json.load(f)
        self.mode = "science"  # default mode
        self.name = self.config["name"]

    def set_mode(self, mode_name):
        if mode_name in self.config["modes"]:
            self.mode = mode_name
            description = self.config["modes"][mode_name]["description"]
            print(f"{self.name} is now in {mode_name.capitalize()} Mode: {description}")
        else:
            print(f"Unknown mode: {mode_name}")

    def speak(self, message):
        # Add random quote or lyric if triggered
        if random.random() < self.config["pop_culture_references"]["settings"]["quote_probability"]:
            reference = random.choice(self._get_all_references())
            message += f" (As they say in {reference}...)"
        print(f"{self.name}: {message}")

    def _get_all_references(self):
        all_refs = []
        for category, items in self.config["pop_culture_references"].items():
            if category != "settings":
                all_refs.extend(items)
        return all_refs

    def react_to_task(self, task_type):
        if task_type == "math":
            self.set_mode("science")
            self.speak("Let’s crunch some numbers and solve this thing.")
        elif task_type == "art":
            self.set_mode("creative")
            self.speak("Let’s get weird and make something beautiful.")
        elif task_type == "chill":
            self.set_mode("chill")
            self.speak("Time to take it slow. I’ve got your back.")
        else:
            self.speak("I'm not sure what we're doing, but I'm here for it!")
