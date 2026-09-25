import pytest

from voice.speech_format import to_speech_text


@pytest.mark.parametrize(
    ("display", "spoken"),
    [
        ("# Forecast\n**Rain** \U0001F327\uFE0F at 2 PM.",
         "Forecast. Rain at 2 PM."),
        ("See [the forecast](https://example.com/radar).",
         "See the forecast."),
        ("Read https://example.com/article for details.",
         "Read for details."),
        ("- Milk\n- Eggs", "Milk. Eggs"),
        ("S.A.T.U.R.N.: 72\u00b0F and 20\u00b0C.",
         "Saturn: 72 degrees Fahrenheit and 20 degrees Celsius."),
        ("3 * 4 = 12", "3 times 4 = 12"),
        ("x^2 + 3\u00d74 = 14",
         "x to the power of 2 + 3 times 4 = 14"),
        ("20% \u00b1 2%",
         "20 percent plus or minus 2 percent"),
        ("\u221a9 = 3", "square root of 9 = 3"),
        ("**Result:** 1/2", "Result: 1/2"),
    ],
)
def test_display_and_speech_differ_without_losing_meaning(
    display, spoken,
):
    assert to_speech_text(display) == spoken


def test_plain_text_remains_plain():
    assert to_speech_text("Your alarm is set for 7:00 AM.") == (
        "Your alarm is set for 7:00 AM."
    )


def test_tts_boundary_uses_spoken_format():
    from voice.text_to_speech import _clean_for_speech

    assert _clean_for_speech(
        "# **Rain** \U0001F327\uFE0F"
    ) == "Rain"
