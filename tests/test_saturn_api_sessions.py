from unittest.mock import patch

import pytest
from pydantic import ValidationError

from api.saturn_api import (
    QueryRequest,
    query_saturn,
    run_saturn_query,
)


def successful_result(response="Test response"):
    return {
        "success": True,
        "domain": "conversation",
        "response": response,
        "data": {
            "provider": "ollama",
            "model": "test-model",
        },
    }


def test_run_query_forwards_session_id():
    expected = successful_result()

    with patch(
        "api.saturn_api.saturn.handle_query",
        return_value=expected,
    ) as mocked_handle_query:
        result = run_saturn_query(
            "  Hello SATURN  ",
            session_id="phone-a",
        )

    assert result == expected
    mocked_handle_query.assert_called_once_with(
        "Hello SATURN",
        session_id="phone-a",
    )


def test_run_query_remains_backward_compatible():
    expected = successful_result()

    with patch(
        "api.saturn_api.saturn.handle_query",
        return_value=expected,
    ) as mocked_handle_query:
        result = run_saturn_query(
            "Hello SATURN"
        )

    assert result == expected
    mocked_handle_query.assert_called_once_with(
        "Hello SATURN",
        session_id=None,
    )


def test_query_endpoint_forwards_request_session():
    expected = successful_result(
        "Session response"
    )
    request = QueryRequest(
        text="Remember this",
        session_id="phone-b",
    )

    with patch(
        "api.saturn_api.run_saturn_query",
        return_value=expected,
    ) as mocked_run_query:
        response = query_saturn(request)

    assert response == {
        "success": True,
        "query": "Remember this",
        "result": expected,
    }
    mocked_run_query.assert_called_once_with(
        "Remember this",
        session_id="phone-b",
    )


def test_query_request_rejects_long_session_id():
    with pytest.raises(ValidationError):
        QueryRequest(
            text="Hello",
            session_id="x" * 129,
        )


def test_run_query_converts_non_json_numbers():
    class SpecialNumber:
        def __str__(self):
            return "5"

    with patch(
        "api.saturn_api.saturn.handle_query",
        return_value={
            "success": True,
            "domain": "math",
            "response": "Result: 5",
            "data": {
                "result": SpecialNumber(),
            },
        },
    ):
        result = run_saturn_query(
            "What is 20 divided by 4?"
        )

    assert result["data"]["result"] == "5"
