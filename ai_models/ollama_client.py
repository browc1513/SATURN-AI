import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class OllamaError(RuntimeError):
    """Raised when SATURN cannot obtain a valid Ollama response."""


class OllamaClient:
    """
    Minimal client for Ollama's local chat API.

    Keeping this behind a small interface allows SATURN to change
    models or inference engines without changing its core router.
    """

    def __init__(
        self,
        model,
        base_url="http://127.0.0.1:11434",
        timeout=60,
    ):
        model = str(model).strip()
        base_url = str(base_url).strip().rstrip("/")

        if not model:
            raise ValueError("An Ollama model name is required.")

        if not base_url:
            raise ValueError("An Ollama base URL is required.")

        self.model = model
        self.base_url = base_url
        self.timeout = timeout

    def chat(
        self,
        user_message,
        system_prompt=None,
    ):
        if user_message is None:
            raise ValueError("A user message is required.")

        user_message = str(user_message).strip()

        if not user_message:
            raise ValueError("A user message is required.")

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": str(system_prompt).strip(),
                }
            )

        messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }

        request = Request(
            f"{self.base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(
                request,
                timeout=self.timeout,
            ) as response:
                response_data = json.loads(
                    response.read().decode("utf-8")
                )
        except (
            HTTPError,
            URLError,
            TimeoutError,
            OSError,
            json.JSONDecodeError,
        ) as error:
            raise OllamaError(
                f"Ollama request failed: {error}"
            ) from error

        message = response_data.get("message")

        if not isinstance(message, dict):
            raise OllamaError(
                "Ollama response did not contain a message."
            )

        content = str(
            message.get("content", "")
        ).strip()

        if not content:
            raise OllamaError(
                "Ollama returned an empty response."
            )

        return content
