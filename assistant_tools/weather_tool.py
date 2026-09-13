"""
S.A.T.U.R.N. Weather Tool

Live weather lookup using the free Open-Meteo APIs.

No API key is required.

Flow:
    natural-language query
        -> location extraction
        -> Open-Meteo geocoding
        -> Open-Meteo forecast/current weather
        -> structured SATURN result
"""

import json
import os
import re
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


DEFAULT_WEATHER_LOCATION = os.environ.get(
    "SATURN_WEATHER_LOCATION",
    "Haslett, Michigan",
)

GEOCODING_URL = (
    "https://geocoding-api.open-meteo.com/v1/search"
)

FORECAST_URL = (
    "https://api.open-meteo.com/v1/forecast"
)

USER_AGENT = "SATURN-AI/1.0"


WEATHER_CODE_DESCRIPTIONS = {
    0: "clear skies",
    1: "mostly clear skies",
    2: "partly cloudy skies",
    3: "overcast skies",
    45: "fog",
    48: "freezing fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "heavy drizzle",
    56: "light freezing drizzle",
    57: "heavy freezing drizzle",
    61: "light rain",
    63: "moderate rain",
    65: "heavy rain",
    66: "light freezing rain",
    67: "heavy freezing rain",
    71: "light snow",
    73: "moderate snow",
    75: "heavy snow",
    77: "snow grains",
    80: "light rain showers",
    81: "moderate rain showers",
    82: "heavy rain showers",
    85: "light snow showers",
    86: "heavy snow showers",
    95: "thunderstorms",
    96: "thunderstorms with light hail",
    99: "thunderstorms with heavy hail",
}


def _fetch_json(base_url, params):
    """
    Make a GET request and decode a JSON response.
    """

    url = (
        base_url
        + "?"
        + urlencode(params)
    )

    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
        },
    )

    try:
        with urlopen(
            request,
            timeout=12,
        ) as response:
            return json.loads(
                response.read().decode(
                    "utf-8"
                )
            )

    except HTTPError as error:
        raise RuntimeError(
            f"Weather service returned HTTP {error.code}."
        ) from error

    except URLError as error:
        raise RuntimeError(
            "Could not connect to the weather service."
        ) from error


def extract_weather_location(
    text,
    default_location=DEFAULT_WEATHER_LOCATION,
):
    """
    Extract a location from common weather phrasing.

    Examples:
        "weather in Tokyo" -> "Tokyo"
        "forecast for East Lansing" -> "East Lansing"
        "temperature in London today" -> "London"

    If no location is supplied, SATURN uses its configured
    default weather location.
    """

    original = str(text).strip()

    patterns = [
        r"\b(?:weather|forecast|temperature|humidity|wind)"
        r"\s+(?:in|for|at)\s+(.+)$",

        r"\b(?:rain|raining|snow|snowing)"
        r".*?\s+(?:in|for|at)\s+(.+)$",

        r"\b(?:in|for|at)\s+"
        r"([A-Za-z][A-Za-z .,'-]+?)"
        r"(?:\s+(?:today|tomorrow|tonight|right now|now))?"
        r"[?.!]*$",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            original,
            flags=re.IGNORECASE,
        )

        if not match:
            continue

        location = match.group(1).strip(
            " ?!.,"
        )

        # Remove trailing weather-time words if the broader
        # first/second patterns captured them.
        location = re.sub(
            r"\s+\b(?:today|tomorrow|tonight|right now|now)\b\s*$",
            "",
            location,
            flags=re.IGNORECASE,
        ).strip()

        if location:
            return location

    return default_location


def _geocode_location(location):
    """
    Convert a user-facing place name into coordinates.
    """

    data = _fetch_json(
        GEOCODING_URL,
        {
            "name": location,
            "count": 1,
            "language": "en",
            "format": "json",
        },
    )

    results = data.get(
        "results",
        [],
    )

    if not results:
        return None

    best = results[0]

    return {
        "name": best.get(
            "name",
            location,
        ),
        "admin1": best.get(
            "admin1"
        ),
        "country": best.get(
            "country"
        ),
        "latitude": best.get(
            "latitude"
        ),
        "longitude": best.get(
            "longitude"
        ),
        "timezone": best.get(
            "timezone"
        ),
    }


def _format_location(location_data):
    """
    Build a compact display name such as:
        Haslett, Michigan
        Tokyo, Japan
    """

    parts = []

    for value in (
        location_data.get("name"),
        location_data.get("admin1"),
        location_data.get("country"),
    ):

        if (
            value
            and value not in parts
        ):
            parts.append(
                str(value)
            )

    # Usually city + state is enough inside the US.
    if (
        location_data.get("country") == "United States"
        and len(parts) >= 2
    ):
        return ", ".join(
            parts[:2]
        )

    # For other countries, city + country is generally cleaner.
    if len(parts) >= 3:
        return ", ".join(
            (
                parts[0],
                parts[-1],
            )
        )

    return ", ".join(parts)


def _get_forecast(location_data):
    """
    Retrieve current conditions and a three-day daily forecast.
    """

    return _fetch_json(
        FORECAST_URL,
        {
            "latitude": location_data["latitude"],
            "longitude": location_data["longitude"],

            "current": ",".join(
                (
                    "temperature_2m",
                    "apparent_temperature",
                    "relative_humidity_2m",
                    "precipitation",
                    "weather_code",
                    "wind_speed_10m",
                )
            ),

            "daily": ",".join(
                (
                    "weather_code",
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_probability_max",
                )
            ),

            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "precipitation_unit": "inch",
            "timezone": "auto",
            "forecast_days": 3,
        },
    )


def _weather_description(code):
    """
    Convert an Open-Meteo WMO weather code into plain English.
    """

    try:
        code = int(code)
    except (TypeError, ValueError):
        return "unknown conditions"

    return WEATHER_CODE_DESCRIPTIONS.get(
        code,
        "unknown conditions",
    )


def _detect_weather_intent(text):
    """
    Return one of:
        current
        forecast
        rain
        snow
    """

    normalized = str(text).lower()

    if re.search(
        r"\b(?:rain|raining|umbrella)\b",
        normalized,
    ):
        return "rain"

    if re.search(
        r"\b(?:snow|snowing)\b",
        normalized,
    ):
        return "snow"

    if re.search(
        r"\b(?:forecast|tomorrow|next few days)\b",
        normalized,
    ):
        return "forecast"

    return "current"


def _daily_value(daily, key, index=0):
    """
    Safely retrieve an item from an Open-Meteo daily array.
    """

    values = daily.get(
        key,
        [],
    )

    if (
        isinstance(values, list)
        and len(values) > index
    ):
        return values[index]

    return None


def handle_weather_query(
    text,
    default_location=DEFAULT_WEATHER_LOCATION,
):
    """
    Handle a natural-language weather request.

    Returns a structured dictionary for SATURN.handle_query().
    """

    requested_location = extract_weather_location(
        text,
        default_location=default_location,
    )

    location_data = _geocode_location(
        requested_location
    )

    if location_data is None:
        return {
            "success": False,
            "response": (
                "I couldn't find that location."
            ),
            "requested_location": requested_location,
            "error": "Location could not be geocoded.",
        }

    weather = _get_forecast(
        location_data
    )

    current = weather.get(
        "current",
        {},
    )

    daily = weather.get(
        "daily",
        {},
    )

    display_location = _format_location(
        location_data
    )

    intent = _detect_weather_intent(
        text
    )

    temperature = current.get(
        "temperature_2m"
    )

    feels_like = current.get(
        "apparent_temperature"
    )

    humidity = current.get(
        "relative_humidity_2m"
    )

    wind_speed = current.get(
        "wind_speed_10m"
    )

    current_precipitation = current.get(
        "precipitation"
    )

    description = _weather_description(
        current.get(
            "weather_code"
        )
    )

    high = _daily_value(
        daily,
        "temperature_2m_max",
        0,
    )

    low = _daily_value(
        daily,
        "temperature_2m_min",
        0,
    )

    precipitation_probability = _daily_value(
        daily,
        "precipitation_probability_max",
        0,
    )

    if intent == "rain":

        response = (
            f"In {display_location}, the current conditions are "
            f"{description}. Today's maximum precipitation chance is "
            f"{precipitation_probability}%."
        )

        if current_precipitation is not None:
            response += (
                f" Current precipitation is "
                f"{current_precipitation} in."
            )

    elif intent == "snow":

        response = (
            f"In {display_location}, the current conditions are "
            f"{description}. Today's precipitation chance is "
            f"{precipitation_probability}%."
        )

    elif intent == "forecast":

        tomorrow_high = _daily_value(
            daily,
            "temperature_2m_max",
            1,
        )

        tomorrow_low = _daily_value(
            daily,
            "temperature_2m_min",
            1,
        )

        tomorrow_code = _daily_value(
            daily,
            "weather_code",
            1,
        )

        tomorrow_precip = _daily_value(
            daily,
            "precipitation_probability_max",
            1,
        )

        tomorrow_description = _weather_description(
            tomorrow_code
        )

        response = (
            f"Current weather in {display_location}: "
            f"{temperature}°F with {description}. "
            f"Today's high is {high}°F and the low is {low}°F. "
            f"Tomorrow: {tomorrow_description}, with a high of "
            f"{tomorrow_high}°F, a low of {tomorrow_low}°F, and a "
            f"{tomorrow_precip}% precipitation chance."
        )

    else:

        response = (
            f"In {display_location}, it is {temperature}°F with "
            f"{description}. It feels like {feels_like}°F. "
            f"Today's high is {high}°F and the low is {low}°F."
        )

        if humidity is not None:
            response += (
                f" Humidity is {humidity}%."
            )

        if wind_speed is not None:
            response += (
                f" Wind is {wind_speed} mph."
            )

    return {
        "success": True,
        "intent": intent,
        "requested_location": requested_location,
        "location": location_data,
        "display_location": display_location,
        "current": current,
        "daily": daily,
        "response": response,
        "source": "Open-Meteo",
        "error": None,
    }
