import threading
from collections import defaultdict, deque


class ConversationMemory:
    """
    Store bounded conversational history by session.

    Each session retains only its most recent exchanges, preventing
    prompts from growing without limit and keeping devices separate.
    """

    def __init__(
        self,
        max_turns=6,
    ):
        if (
            not isinstance(max_turns, int)
            or max_turns <= 0
        ):
            raise ValueError(
                "max_turns must be a positive integer."
            )

        self.max_turns = max_turns
        self.max_messages = max_turns * 2
        self._histories = defaultdict(
            lambda: deque(
                maxlen=self.max_messages
            )
        )
        self._lock = threading.RLock()

    def get_history(
        self,
        session_id=None,
    ):
        session_key = self._normalize_session_id(
            session_id
        )

        with self._lock:
            return [
                dict(message)
                for message in self._histories[
                    session_key
                ]
            ]

    def add_exchange(
        self,
        session_id,
        user_message,
        assistant_message,
    ):
        session_key = self._normalize_session_id(
            session_id
        )
        user_message = self._normalize_message(
            user_message,
            "user",
        )
        assistant_message = self._normalize_message(
            assistant_message,
            "assistant",
        )

        with self._lock:
            history = self._histories[
                session_key
            ]

            history.append(
                {
                    "role": "user",
                    "content": user_message,
                }
            )
            history.append(
                {
                    "role": "assistant",
                    "content": assistant_message,
                }
            )

    def clear(
        self,
        session_id=None,
    ):
        session_key = self._normalize_session_id(
            session_id
        )

        with self._lock:
            self._histories.pop(
                session_key,
                None,
            )

    @staticmethod
    def _normalize_session_id(
        session_id,
    ):
        if session_id is None:
            return "default"

        session_key = str(session_id).strip()

        if not session_key:
            return "default"

        if len(session_key) > 128:
            raise ValueError(
                "session_id cannot exceed 128 characters."
            )

        return session_key

    @staticmethod
    def _normalize_message(
        message,
        role,
    ):
        if message is None:
            raise ValueError(
                f"{role} message is required."
            )

        normalized = str(message).strip()

        if not normalized:
            raise ValueError(
                f"{role} message is required."
            )

        return normalized
