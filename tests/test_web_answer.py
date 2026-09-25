from unittest.mock import patch

from core.saturn_personality import SATURN


PAGE_TEXT = (
    "Field reversed configurations are compact plasma configurations "
    "studied for magnetic confinement and fusion research. "
) * 5

RESULTS = [{
    "title": "FRC Research",
    "url": "https://example.org/frc",
    "description": "A research overview",
    "published": "2026-09-20",
}]


class FakeModel:
    model = "test-model"

    def __init__(self, *answers):
        self.answers = iter(answers)
        self.calls = []

    def chat(self, message, **kwargs):
        self.calls.append((message, kwargs))
        return next(self.answers)


def saturn_with_model(*answers):
    saturn = SATURN(start_alarm_monitor=False)
    saturn.personal_memory = None
    saturn.local_model = FakeModel(*answers)
    return saturn


def test_ordinary_question_returns_sourced_answer():
    saturn = saturn_with_model(
        "WEB",
        "FRCs are studied for magnetic confinement [1].",
    )
    with patch("assistant_tools.web_answer.search_web",
               return_value=RESULTS) as search:
        with patch("assistant_tools.web_answer.read_public_page",
                   return_value={
                       "url": RESULTS[0]["url"],
                       "text": PAGE_TEXT,
                   }) as read:
            result = saturn.handle_query(
                "What is the latest research on FRCs?",
                session_id="web-test",
            )

    search.assert_called_once()
    read.assert_called_once_with(RESULTS[0]["url"])
    assert result["success"] is True
    assert result["domain"] == "web"
    assert "[1]" in result["response"]
    assert result["data"]["sources"][0]["url"] == RESULTS[0]["url"]
    assert "Sources include FRC Research" in result["speech_text"]
    assert "https://" not in result["speech_text"]


def test_non_web_question_stays_in_conversation():
    saturn = saturn_with_model("Hello there.")
    with patch("assistant_tools.web_answer.search_web") as search:
        result = saturn.handle_query("Tell me a joke.")
    search.assert_not_called()
    assert result["domain"] == "conversation"
    assert result["response"] == "Hello there."


def test_invalid_citation_is_rejected():
    saturn = saturn_with_model("WEB", "An unsupported claim [9].")
    with patch("assistant_tools.web_answer.search_web",
               return_value=RESULTS):
        with patch("assistant_tools.web_answer.read_public_page",
                   return_value={
                       "url": RESULTS[0]["url"],
                       "text": PAGE_TEXT,
                   }):
            result = saturn.handle_query(
                "What is the latest research on FRCs?"
            )
    assert result["success"] is False
    assert result["domain"] == "web"
    assert "properly sourced" in result["response"]



def test_web_answer_excludes_private_memory_and_history():
    from types import SimpleNamespace

    saturn = saturn_with_model(
        "WEB",
        "FRCs are studied for magnetic confinement [1].",
    )
    saturn.personal_memory = SimpleNamespace(
        format_for_prompt=lambda: "PRIVATE MEMORY MARKER"
    )
    saturn.conversation_memory.add_exchange(
        "web-test", "Earlier question", "PRIVATE HISTORY MARKER"
    )

    with patch("assistant_tools.web_answer.search_web",
               return_value=RESULTS):
        with patch("assistant_tools.web_answer.read_public_page",
                   return_value={
                       "url": RESULTS[0]["url"],
                       "text": PAGE_TEXT,
                   }):
            result = saturn.handle_query(
                "What is the latest research on FRCs?",
                session_id="web-test",
            )

    assert result["success"] is True
    synthesis_message, synthesis_options = saturn.local_model.calls[1]
    assert "PRIVATE MEMORY MARKER" not in synthesis_message
    assert "PRIVATE MEMORY MARKER" not in synthesis_options["system_prompt"]
    assert "PRIVATE HISTORY MARKER" not in synthesis_message
    assert synthesis_options["conversation_history"] == []


def test_unclear_web_decision_does_not_return_unsourced_answer():
    saturn = saturn_with_model("UNCLEAR")
    with patch("assistant_tools.web_answer.search_web") as search:
        result = saturn.handle_query(
            "What is the latest research on FRCs?"
        )

    search.assert_not_called()
    assert result["success"] is False
    assert result["domain"] == "web"
    assert len(saturn.local_model.calls) == 1
