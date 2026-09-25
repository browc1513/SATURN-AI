"""Prepare a spoken version of SATURN's displayed responses."""

import html
import re


_EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\u2600-\u27BF"
    "\uFE0F\u200D\U0001F3FB-\U0001F3FF]"
)


def to_speech_text(value):
    """Remove display formatting while retaining meaningful speech."""

    text = html.unescape(str(value))
    text = text.replace("S.A.T.U.R.N.", "Saturn")
    text = text.replace("\u00c2\u00b0", "\u00b0")

    text = re.sub(r"!\[([^]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"https?://[^\s)]+", "", text)

    text = re.sub(r"(?m)^\s{0,3}#{1,6}\s+", "", text)
    text = re.sub(
        r"(?m)^\s{0,3}(?:[-*+]\s+|\d+[.)]\s+|>\s*)",
        "",
        text,
    )
    text = re.sub(r"(?m)^\s*(?:```|~~~)[^\n]*$", "", text)

    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"__(.+?)__", r"\1", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\1", text)
    text = re.sub(r"(?<!_)_([^_\n]+)_(?!_)", r"\1", text)
    text = text.replace("`", "").replace("~~", "")

    text = re.sub(
        r"(?<=\w)\s*\*\*\s*(?=\w)",
        " to the power of ",
        text,
    )
    text = re.sub(
        r"(?<=\w)\s*\*\s*(?=\w)",
        " times ",
        text,
    )
    text = re.sub(
        r"(?<=\w)\s*\^\s*(?=\w)",
        " to the power of ",
        text,
    )
    text = text.replace("\u00d7", " times ")
    text = text.replace("\u00f7", " divided by ")
    text = text.replace("\u00b1", " plus or minus ")
    text = text.replace("\u221a", " square root of ")
    text = text.replace("\u00b0F", " degrees Fahrenheit")
    text = text.replace("\u00b0C", " degrees Celsius")
    text = re.sub(r"(?<=\d)\s*%", " percent", text)

    text = _EMOJI.sub("", text).replace("\u20e3", "")
    text = re.sub(r"[#*]+", "", text)
    text = re.sub(r"\s*\n+\s*", ". ", text)
    text = re.sub(r"\.{2,}", ".", text)
    return " ".join(text.split()).strip()
