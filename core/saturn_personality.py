import json
import random
import os
import re
import threading
import time


class SATURN:
    def __init__(
        self,
        config_path="saturn_config.json",
        start_alarm_monitor=True,
    ):
        self.name = "S.A.T.U.R.N."
        self.mode = "science"
        self.voice_enabled = False

        self.load_config(config_path)

        # Alarm monitoring is enabled by default so existing SATURN
        # interfaces retain their current behavior. Interfaces that
        # should not own alarm firing, such as the API process, can
        # explicitly disable it.
        self._alarm_monitor_running = False
        self._alarm_monitor_thread = None

        if start_alarm_monitor:
            self._alarm_monitor_running = True

            self._alarm_monitor_thread = threading.Thread(
                target=self._alarm_monitor_loop,
                daemon=True,
                name="SATURNAlarmMonitor",
            )

            self._alarm_monitor_thread.start()

    # ============================================================
    # CONFIGURATION
    # ============================================================

    def load_config(self, config_path):
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"S.A.T.U.R.N. config not found at: {config_path}"
            )

        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        self.name = config.get(
            "name",
            "S.A.T.U.R.N."
        )

        self.mode = config.get(
            "mode",
            "science"
        )

        self.personality_traits = config.get(
            "personality_traits",
            {}
        )

        self.references = config.get(
            "pop_culture_references",
            {}
        )

        self.reference_frequency = config.get(
            "reference_frequency",
            "occasional"
        )

    # ============================================================
    # PERSONALITY / OUTPUT
    # ============================================================

    def speak(self, message):
        """
        Temporary speech/output method.

        Later this can be connected to the TTS system.
        """

        print(
            f"{self.name}: {message}"
        )

    def react_to_task(self, task_type):
        task_type = task_type.lower()

        if task_type in [
            "math",
            "physics",
            "science",
        ]:
            self.set_mode("science")

        elif task_type in [
            "art",
            "film",
            "music",
            "writing",
        ]:
            self.set_mode("creative")

        elif task_type in [
            "relax",
            "chill",
            "vibe",
        ]:
            self.set_mode("chill")

    def set_mode(self, mode_name):
        mode_name = mode_name.lower()

        valid_modes = [
            "science",
            "creative",
            "chill",
        ]

        if mode_name in valid_modes:
            self.mode = mode_name

            self.speak(
                f"Switched to {mode_name.capitalize()} Mode!"
            )

        else:
            self.speak(
                f"I don't recognize '{mode_name}' as a valid mode."
            )

    def random_reference(self):
        sources = []

        for key, value in self.references.items():
            if isinstance(value, list):
                sources.extend(value)

        if sources:
            return random.choice(
                sources
            )

        return None

    def say(self, message):
        reference = self.random_reference()

        if reference:
            return (
                f"{self.name}: "
                f"{message} "
                f"(btw, remember {reference})"
            )

        return (
            f"{self.name}: {message}"
        )

    # ============================================================
    # BACKGROUND ALARM MONITOR
    # ============================================================

    def _alarm_monitor_loop(self):
        """
        Check once per second for alarms that have become due.

        check_due_alarms() marks returned alarms as fired, so each
        alarm is triggered only once.
        """

        while self._alarm_monitor_running:
            try:
                from assistant_tools.alarm_tool import (
                    check_due_alarms,
                    play_alarm_sound,
                )

                due_alarms = check_due_alarms(
                    mark_fired=True
                )

                for alarm in due_alarms:
                    trigger_at = alarm.get(
                        "trigger_at",
                        "",
                    )

                    print(
                        "\n"
                        "S.A.T.U.R.N. ALARM: "
                        f"Alarm due at {trigger_at}"
                    )

                    # Run the Windows sound in its own daemon thread
                    # so SATURN stays responsive while the alarm plays.
                    threading.Thread(
                        target=play_alarm_sound,
                        kwargs={
                            "repetitions": 5,
                        },
                        daemon=True,
                        name="SATURNAlarmSound",
                    ).start()

            except Exception as error:
                print(
                    "S.A.T.U.R.N. alarm monitor warning: "
                    f"{error}"
                )

            time.sleep(
                1
            )

    def stop_alarm_monitor(self):
        """
        Stop the background alarm monitor cleanly.
        """

        self._alarm_monitor_running = False

    # ============================================================
    # CENTRAL LANGUAGE USER INTERFACE
    # ============================================================

    def handle_query(self, text):
        """
        Main Language User Interface entry point.

        Every user-facing interface should eventually send its
        raw natural-language input here:

            GUI
            CLI
            Voice
            Raspberry Pi
            Future mobile/web interfaces

        SATURN determines which subsystem should handle the query.

        Returns:
            {
                "success": bool,
                "domain": str,
                "response": str,
                "data": object
            }
        """

        text = str(text).strip()

        if not text:
            return {
                "success": False,
                "domain": "unknown",
                "response": "I didn't receive a query.",
                "data": None,
            }

        domain = self._detect_domain(
            text
        )

        if domain == "math":
            return self._handle_math_query(
                text
            )

        if domain == "veterinary":
            return self._handle_veterinary_query(
                text
            )

        if domain == "time":
            return self._handle_time_query(
                text
            )

        if domain == "weather":
            return self._handle_weather_query(
                text
            )

        if domain == "lists":
            return self._handle_list_query(
                text
            )

        if domain == "alarms":
            return self._handle_alarm_query(
                text
            )

        return {
            "success": False,
            "domain": "unknown",
            "response": (
                "I'm not sure which subsystem should handle "
                "that request yet. Right now I can automatically "
                "route mathematical, veterinary, time, weather, list, and alarm queries."
            ),
            "data": None,
        }

    # ============================================================
    # DOMAIN ROUTER
    # ============================================================

    def _detect_domain(self, text):
        """
        Determine which SATURN subsystem should receive a query.

        Version 1 uses deterministic keyword and structural
        recognition.

        Later this can be expanded with a dedicated natural-language
        intent classifier without changing the GUI.
        """

        normalized = (
            str(text)
            .lower()
            .strip()
        )

        # --------------------------------------------------------
        # Time / date routing
        # --------------------------------------------------------

        time_patterns = [
            r"\bwhat\s+time\s+is\s+it\b",
            r"\bwhat'?s\s+the\s+time\b",
            r"\bcurrent\s+time\b",
            r"\btime\s+right\s+now\b",
            r"\bwhat\s+time\s+is\s+it\s+in\b",
            r"\bwhat'?s\s+today'?s\s+date\b",
            r"\bwhat\s+is\s+today'?s\s+date\b",
            r"\bwhat\s+date\s+is\s+it\b",
            r"\bwhat\s+day\s+is\s+it\b",
            r"\btoday'?s\s+date\b",
        ]

        if any(
            re.search(
                pattern,
                normalized,
            )
            for pattern in time_patterns
        ):
            return "time"

        # --------------------------------------------------------
        # Veterinary routing
        # --------------------------------------------------------

        veterinary_keywords = [
            "vet",
            "veterinary",
            "diagnosis",
            "clinical sign",
            "clinical signs",
            "disease",
            "animal",

            # Species
            "cattle",
            "cow",
            "bovine",
            "calf",

            "horse",
            "equine",
            "foal",

            "dog",
            "canine",
            "puppy",

            "cat",
            "feline",
            "kitten",

            "sheep",
            "ovine",
            "lamb",

            "goat",
            "caprine",

            "pig",
            "swine",
            "porcine",

            "chicken",
            "poultry",
        ]

        if self._contains_any_keyword(
            normalized,
            veterinary_keywords,
        ):
            return "veterinary"

        # --------------------------------------------------------
        # Weather routing
        # --------------------------------------------------------

        weather_keywords = [
            "weather",
            "forecast",
            "temperature",
            "outside",
            "rain",
            "raining",
            "snow",
            "snowing",
            "humidity",
            "wind",
            "windy",
        ]

        if self._contains_any_keyword(
            normalized,
            weather_keywords,
        ):
            return "weather"

        # --------------------------------------------------------
        # Alarm routing
        # --------------------------------------------------------

        alarm_keywords = [
            "alarm",
            "alarms",
            "wake me",
            "wake me up",
        ]

        alarm_patterns = [
            r"\bset\s+(?:an\s+|a\s+)?alarm\b",
            r"\bcancel\s+(?:my\s+)?alarm\b",
            r"\bdelete\s+(?:my\s+)?alarm\b",
            r"\bshow\s+(?:me\s+)?(?:my\s+)?alarms?\b",
            r"\blist\s+(?:my\s+)?alarms?\b",
        ]

        if (
            self._contains_any_keyword(
                normalized,
                alarm_keywords,
            )
            or any(
                re.search(
                    pattern,
                    normalized,
                )
                for pattern in alarm_patterns
            )
        ):
            return "alarms"

        # --------------------------------------------------------
        # List routing
        # --------------------------------------------------------

        list_keywords = [
            "list",
            "lists",
            "grocery list",
            "shopping list",
            "todo list",
            "to-do list",
            "checklist",
        ]

        list_action_patterns = [
            r"\bcreate\s+(?:a\s+|my\s+)?[a-z0-9 _-]*list\b",
            r"\bmake\s+(?:a\s+|my\s+)?[a-z0-9 _-]*list\b",
            r"\bshow\s+(?:me\s+)?(?:my\s+)?[a-z0-9 _-]*list\b",
            r"\badd\b.+\bto\b.+\blist\b",
            r"\bremove\b.+\bfrom\b.+\blist\b",
            r"\bdelete\b.+\bfrom\b.+\blist\b",
            r"\bclear\b.+\blist\b",
        ]

        if (
            self._contains_any_keyword(
                normalized,
                list_keywords,
            )
            or any(
                re.search(
                    pattern,
                    normalized,
                )
                for pattern in list_action_patterns
            )
        ):
            return "lists"

        # --------------------------------------------------------
        # Math routing
        # --------------------------------------------------------

        math_keywords = [
            # General
            "math",
            "calculate",
            "calculation",
            "solve",
            "equation",
            "formula",

            # Arithmetic
            "add",
            "sum",
            "plus",
            "subtract",
            "difference",
            "minus",
            "multiply",
            "product",
            "times",
            "divide",
            "divided by",
            "quotient",
            "percentage",
            "percent",

            # Algebra
            "algebra",
            "factor",
            "simplify",
            "expand",
            "polynomial",
            "squared",
            "cubed",
            "power",
            "powers",

            # Calculus
            "calculus",
            "derivative",
            "differentiate",
            "integral",
            "integrate",
            "limit",
            "riemann",
            "extrema",
            "maximum",
            "minimum",

            # Geometry
            "geometry",
            "area",
            "volume",
            "radius",
            "diameter",
            "circumference",
            "perimeter",

            # Trigonometry
            "trigonometry",
            "trig",
            "sin",
            "sine",
            "cos",
            "cosine",
            "tan",
            "tangent",
            "arcsin",
            "arcsine",
            "arccos",
            "arccosine",
            "arctan",
            "arctangent",

            # Linear algebra
            "matrix",
            "determinant",
            "vector",
            "rref",
            "eigenvalue",
            "eigenvector",

            # Statistics
            "mean",
            "average",
            "standard deviation",
        ]

        if self._contains_any_keyword(
            normalized,
            math_keywords,
        ):
            return "math"

        # --------------------------------------------------------
        # Mathematical notation detection
        # --------------------------------------------------------
        #
        # Examples:
        #
        # 17 + 28
        # 10 / 2
        # x + 4
        # 4*x - 7 = 21
        # x^2
        #
        # --------------------------------------------------------

        math_patterns = [
            r"\d+\s*[\+\-\*/\^=]\s*\d+",
            r"[a-zA-Z]\s*[\+\-\*/\^=]\s*\d+",
            r"\d+\s*[\+\-\*/\^=]\s*[a-zA-Z]",
            r"[a-zA-Z]\s*[\+\-\*/\^=]\s*[a-zA-Z]",
        ]

        for pattern in math_patterns:
            if re.search(
                pattern,
                normalized,
            ):
                return "math"

        return "unknown"

    def _contains_any_keyword(
        self,
        text,
        keywords,
    ):
        """
        Check for whole-word or whole-phrase keyword matches.

        This prevents accidental substring matches.

        Example:
            'calculate' should not match veterinary keyword 'cat'.
        """

        for keyword in keywords:
            pattern = (
                r"\b"
                + re.escape(keyword)
                + r"\b"
            )

            if re.search(
                pattern,
                text,
            ):
                return True

        return False

    # ============================================================
    # MATH SUBSYSTEM
    # ============================================================

    def _handle_math_query(self, text):
        """
        Send a natural-language mathematical request through
        SATURN's deterministic math pipeline.
        """

        from math_engine.math_pipeline import (
            interpret_and_execute_math,
        )

        try:
            result = interpret_and_execute_math(
                text
            )

        except Exception as error:
            return {
                "success": False,
                "domain": "math",
                "response": (
                    "Something went wrong while processing "
                    "the mathematical request:\n"
                    f"{error}"
                ),
                "data": None,
            }

        if not result.get(
            "success",
            False,
        ):
            return {
                "success": False,
                "domain": "math",
                "response": (
                    "I couldn't complete that calculation.\n\n"
                    f"{result.get('error', 'Unknown math error.')}"
                ),
                "data": result,
            }

        response = self._format_math_response(
            result
        )

        return {
            "success": True,
            "domain": "math",
            "response": response,
            "data": result,
        }

    def _format_math_response(
        self,
        result,
    ):
        """
        Convert the structured math pipeline result into
        chat-friendly text.

        The raw structured result remains available in the
        'data' field returned by handle_query().
        """

        lines = []

        operation = result.get(
            "operation"
        )

        exact_result = result.get(
            "exact_result"
        )

        decimal_result = result.get(
            "decimal_result"
        )

        steps = result.get(
            "steps",
            [],
        )

        warnings = result.get(
            "warnings",
            [],
        )

        if operation == "expression":
            if exact_result is not None:
                lines.append(
                    f"Expression: {exact_result}"
                )

        else:
            if operation:
                lines.append(
                    f"Operation: {operation}"
                )

            if exact_result is not None:
                lines.append(
                    f"Result: {exact_result}"
                )

        if (
            decimal_result is not None
            and str(decimal_result)
            != str(exact_result)
        ):
            lines.append(
                f"Decimal: {decimal_result}"
            )

        if steps:
            lines.append("")
            lines.append("Steps:")

            for step in steps:
                lines.append(
                    f"  {step}"
                )

        if warnings:
            lines.append("")

            for warning in warnings:
                lines.append(
                    f"Warning: {warning}"
                )

        if not lines:
            return (
                "The calculation completed, but there was "
                "no formatted result to display."
            )

        return "\n".join(
            lines
        )

    # ============================================================
    # ALARM SUBSYSTEM
    # ============================================================

    def _handle_alarm_query(
        self,
        text,
    ):
        """
        Send a natural-language alarm request through SATURN's
        persistent local alarm tool.
        """

        from assistant_tools.alarm_tool import (
            handle_alarm_query,
        )

        try:
            result = handle_alarm_query(
                text
            )

        except Exception as error:
            return {
                "success": False,
                "domain": "alarms",
                "response": (
                    "Something went wrong while working with "
                    f"your alarms:\n{error}"
                ),
                "data": None,
            }

        return {
            "success": result.get(
                "success",
                False,
            ),
            "domain": "alarms",
            "response": result.get(
                "response",
                "I couldn't complete that alarm request.",
            ),
            "data": result,
        }

    # ============================================================
    # LIST SUBSYSTEM
    # ============================================================

    def _handle_list_query(
        self,
        text,
    ):
        """
        Send a natural-language list request through SATURN's
        persistent local list tool.
        """

        from assistant_tools.list_tool import (
            handle_list_query,
        )

        try:
            result = handle_list_query(
                text
            )

        except Exception as error:
            return {
                "success": False,
                "domain": "lists",
                "response": (
                    "Something went wrong while working with "
                    f"your lists:\n{error}"
                ),
                "data": None,
            }

        return {
            "success": result.get(
                "success",
                False,
            ),
            "domain": "lists",
            "response": result.get(
                "response",
                "I couldn't complete that list request.",
            ),
            "data": result,
        }

    # ============================================================
    # WEATHER SUBSYSTEM
    # ============================================================

    def _handle_weather_query(
        self,
        text,
    ):
        """
        Send a natural-language weather request through SATURN's
        live weather tool.
        """

        from assistant_tools.weather_tool import (
            handle_weather_query,
        )

        try:
            result = handle_weather_query(
                text
            )

        except Exception as error:
            return {
                "success": False,
                "domain": "weather",
                "response": (
                    "Something went wrong while checking "
                    f"the weather:\n{error}"
                ),
                "data": None,
            }

        return {
            "success": result.get(
                "success",
                False,
            ),
            "domain": "weather",
            "response": result.get(
                "response",
                "I couldn't retrieve the weather.",
            ),
            "data": result,
        }

    # ============================================================
    # TIME / DATE SUBSYSTEM
    # ============================================================

    def _handle_time_query(
        self,
        text,
    ):
        """
        Send a natural-language time/date request through SATURN's
        deterministic time tool.
        """

        from assistant_tools.time_tool import (
            handle_time_query,
        )

        try:
            result = handle_time_query(
                text
            )

        except Exception as error:
            return {
                "success": False,
                "domain": "time",
                "response": (
                    "Something went wrong while checking "
                    f"the time or date:\n{error}"
                ),
                "data": None,
            }

        return {
            "success": result.get(
                "success",
                False,
            ),
            "domain": "time",
            "response": result.get(
                "response",
                "I couldn't determine the requested time or date.",
            ),
            "data": result,
        }

    # ============================================================
    # VETERINARY SUBSYSTEM
    # ============================================================

    def _handle_veterinary_query(
        self,
        text,
    ):
        """
        Send a veterinary query through SATURN's clinical
        veterinary database.
        """

        from veterinary_subsystem.clinical_search import (
            search_veterinary_database,
            format_veterinary_results,
        )

        database_path = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            ),
            "data",
            "Pathophysiology Guide.xlsx",
        )

        species = self._detect_species(
            text
        )

        structured_filters = None

        if species:
            structured_filters = {
                "host_species": species
            }

        try:
            results = search_veterinary_database(
                database_path,
                text,
                structured_filters=structured_filters,
            )

            response = format_veterinary_results(
                results
            )

            return {
                "success": True,
                "domain": "veterinary",
                "response": response,
                "data": results,
            }

        except Exception as error:
            return {
                "success": False,
                "domain": "veterinary",
                "response": (
                    "Something went wrong while searching "
                    "the veterinary database:\n"
                    f"{error}"
                ),
                "data": None,
            }

    def _detect_species(self, text):
        """
        Detect a veterinary species mentioned in the query and
        convert common names into the species labels used by the
        veterinary database.
        """

        normalized = (
            str(text)
            .lower()
            .strip()
        )

        species_map = {
            # Cattle
            "cattle": "cattle",
            "cow": "cattle",
            "bovine": "cattle",
            "calf": "cattle",

            # Horse
            "horse": "horse",
            "equine": "horse",
            "foal": "horse",

            # Dog
            "dog": "dog",
            "canine": "dog",
            "puppy": "dog",

            # Cat
            "cat": "cat",
            "feline": "cat",
            "kitten": "cat",

            # Sheep
            "sheep": "sheep",
            "ovine": "sheep",
            "lamb": "sheep",

            # Goat
            "goat": "goat",
            "caprine": "goat",

            # Pig
            "pig": "pig",
            "swine": "pig",
            "porcine": "pig",

            # Chicken
            "chicken": "chicken",
            "poultry": "chicken",
        }

        for keyword, species in species_map.items():
            pattern = (
                r"\b"
                + re.escape(keyword)
                + r"\b"
            )

            if re.search(
                pattern,
                normalized,
            ):
                return species

        return None