import os
import re
import sqlite3
import threading
import time
import uuid
from contextlib import contextmanager
from datetime import datetime
from datetime import timezone
from pathlib import Path


DEFAULT_MAX_MEMORY_LENGTH = 1000
DEFAULT_PROMPT_MEMORY_LIMIT = 20


class PersonalMemoryError(Exception):
    """
    Base exception for personal-memory operations.
    """


class SensitiveMemoryError(PersonalMemoryError):
    """
    Raised when a memory appears to contain a secret.
    """


class PersonalMemoryStore:
    """
    Store user-approved persistent memories in SQLite.

    The public interface intentionally hides SQLite-specific details
    so a future PostgreSQL backend can implement the same operations.
    Every operation opens a short-lived connection, allowing SATURN's
    API and voice processes to share the database safely.
    """

    def __init__(
        self,
        database_path=None,
        max_memory_length=DEFAULT_MAX_MEMORY_LENGTH,
        prompt_memory_limit=DEFAULT_PROMPT_MEMORY_LIMIT,
    ):
        if database_path is None:
            database_path = os.environ.get(
                "SATURN_MEMORY_DATABASE",
                "",
            ).strip()

        if not database_path:
            database_path = (
                Path(__file__).resolve().parent.parent
                / "data"
                / "saturn_memory.db"
            )

        self.database_path = Path(
            database_path
        ).expanduser().resolve()

        if (
            not isinstance(max_memory_length, int)
            or max_memory_length <= 0
        ):
            raise ValueError(
                "max_memory_length must be a positive integer."
            )

        if (
            not isinstance(prompt_memory_limit, int)
            or prompt_memory_limit <= 0
        ):
            raise ValueError(
                "prompt_memory_limit must be a positive integer."
            )

        self.max_memory_length = max_memory_length
        self.prompt_memory_limit = prompt_memory_limit
        self._lock = threading.RLock()

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize_database()

    def _connect(self):
        connection = sqlite3.connect(
            self.database_path,
            timeout=10,
        )
        connection.row_factory = sqlite3.Row

        connection.execute(
            "PRAGMA busy_timeout = 10000"
        )
        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        return connection

    @contextmanager
    def _connection(self):
        """
        Yield a transactional SQLite connection and always close it.

        sqlite3.Connection context management commits or rolls back,
        but it does not close the file handle. Explicit closure is
        required so Windows can release, move, back up, or migrate
        the database file safely.
        """

        connection = self._connect()

        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def _initialize_database(self):
        """
        Initialize the shared database with bounded lock retries.

        SQLite can briefly lock PRAGMA journal_mode while another
        SATURN process or store instance initializes the same file.
        Retrying that short race preserves WAL mode for concurrent
        API and voice access.
        """

        deadline = time.monotonic() + 10

        while True:
            try:
                with self._lock:
                    with self._connection() as connection:
                        connection.execute(
                            "PRAGMA journal_mode = WAL"
                        )
                        connection.execute(
                            """
                            CREATE TABLE IF NOT EXISTS memories (
                                memory_id TEXT PRIMARY KEY,
                                content TEXT NOT NULL,
                                normalized_content TEXT NOT NULL UNIQUE,
                                category TEXT NOT NULL,
                                source TEXT NOT NULL,
                                created_at TEXT NOT NULL,
                                updated_at TEXT NOT NULL
                            )
                            """
                        )
                        connection.execute(
                            """
                            CREATE INDEX IF NOT EXISTS
                            idx_memories_updated_at
                            ON memories(updated_at DESC)
                            """
                        )

                return
            except sqlite3.OperationalError as error:
                database_locked = (
                    "locked"
                    in str(error).casefold()
                )

                if (
                    not database_locked
                    or time.monotonic() >= deadline
                ):
                    raise

                time.sleep(0.05)

    def remember(
        self,
        content,
        *,
        category="personal",
        source="explicit",
    ):
        content = self._normalize_content(
            content
        )
        category = self._normalize_label(
            category,
            "category",
        )
        source = self._normalize_label(
            source,
            "source",
        )

        self._reject_sensitive_content(
            content
        )

        normalized_content = (
            self._comparison_text(
                content
            )
        )
        now = self._utc_now()

        with self._lock:
            with self._connection() as connection:
                existing = connection.execute(
                    """
                    SELECT *
                    FROM memories
                    WHERE normalized_content = ?
                    """,
                    (
                        normalized_content,
                    ),
                ).fetchone()

                if existing is not None:
                    result = self._row_to_dict(
                        existing
                    )
                    result["status"] = "existing"
                    return result

                memory_id = str(
                    uuid.uuid4()
                )

                connection.execute(
                    """
                    INSERT INTO memories (
                        memory_id,
                        content,
                        normalized_content,
                        category,
                        source,
                        created_at,
                        updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        memory_id,
                        content,
                        normalized_content,
                        category,
                        source,
                        now,
                        now,
                    ),
                )

                created = connection.execute(
                    """
                    SELECT *
                    FROM memories
                    WHERE memory_id = ?
                    """,
                    (
                        memory_id,
                    ),
                ).fetchone()

        result = self._row_to_dict(
            created
        )
        result["status"] = "created"
        return result

    def list_memories(
        self,
        *,
        limit=None,
    ):
        limit = self._normalize_limit(
            limit
        )

        query = """
            SELECT *
            FROM memories
            ORDER BY updated_at DESC, memory_id ASC
        """
        parameters = ()

        if limit is not None:
            query += " LIMIT ?"
            parameters = (
                limit,
            )

        with self._lock:
            with self._connection() as connection:
                rows = connection.execute(
                    query,
                    parameters,
                ).fetchall()

        return [
            self._row_to_dict(row)
            for row in rows
        ]

    def search(
        self,
        query,
        *,
        limit=None,
    ):
        query = self._normalize_content(
            query
        )
        limit = self._normalize_limit(
            limit
        )

        escaped = (
            query.replace(
                "\\",
                "\\\\",
            )
            .replace(
                "%",
                "\\%",
            )
            .replace(
                "_",
                "\\_",
            )
        )

        sql = """
            SELECT *
            FROM memories
            WHERE content LIKE ? ESCAPE '\\'
            ORDER BY updated_at DESC, memory_id ASC
        """
        parameters = [
            f"%{escaped}%"
        ]

        if limit is not None:
            sql += " LIMIT ?"
            parameters.append(
                limit
            )

        with self._lock:
            with self._connection() as connection:
                rows = connection.execute(
                    sql,
                    tuple(parameters),
                ).fetchall()

        return [
            self._row_to_dict(row)
            for row in rows
        ]

    def forget_exact(
        self,
        content,
    ):
        normalized_content = (
            self._comparison_text(
                self._normalize_content(
                    content
                )
            )
        )

        with self._lock:
            with self._connection() as connection:
                cursor = connection.execute(
                    """
                    DELETE FROM memories
                    WHERE normalized_content = ?
                    """,
                    (
                        normalized_content,
                    ),
                )

                return cursor.rowcount > 0

    def forget_by_id(
        self,
        memory_id,
    ):
        memory_id = str(
            memory_id
        ).strip()

        if not memory_id:
            raise ValueError(
                "memory_id is required."
            )

        with self._lock:
            with self._connection() as connection:
                cursor = connection.execute(
                    """
                    DELETE FROM memories
                    WHERE memory_id = ?
                    """,
                    (
                        memory_id,
                    ),
                )

                return cursor.rowcount > 0

    def clear(self):
        with self._lock:
            with self._connection() as connection:
                cursor = connection.execute(
                    "DELETE FROM memories"
                )

                return cursor.rowcount

    def count(self):
        with self._lock:
            with self._connection() as connection:
                row = connection.execute(
                    """
                    SELECT COUNT(*) AS memory_count
                    FROM memories
                    """
                ).fetchone()

        return int(
            row["memory_count"]
        )

    def format_for_prompt(
        self,
        *,
        limit=None,
    ):
        if limit is None:
            limit = self.prompt_memory_limit

        memories = self.list_memories(
            limit=limit,
        )

        if not memories:
            return ""

        lines = [
            "User-approved persistent facts:",
        ]

        for memory in reversed(memories):
            lines.append(
                f"- {memory['content']}"
            )

        return "\n".join(
            lines
        )

    def _normalize_content(
        self,
        content,
    ):
        if content is None:
            raise ValueError(
                "Memory content is required."
            )

        normalized = re.sub(
            r"\s+",
            " ",
            str(content),
        ).strip()

        if not normalized:
            raise ValueError(
                "Memory content is required."
            )

        if len(normalized) > self.max_memory_length:
            raise ValueError(
                "Memory content cannot exceed "
                f"{self.max_memory_length} characters."
            )

        return normalized

    @staticmethod
    def _comparison_text(
        content,
    ):
        normalized = content.casefold().strip()

        return re.sub(
            r"[.!?]+$",
            "",
            normalized,
        ).strip()

    @staticmethod
    def _normalize_label(
        value,
        field_name,
    ):
        normalized = re.sub(
            r"\s+",
            " ",
            str(value),
        ).strip().lower()

        if not normalized:
            raise ValueError(
                f"{field_name} is required."
            )

        if len(normalized) > 64:
            raise ValueError(
                f"{field_name} cannot exceed 64 characters."
            )

        return normalized

    @staticmethod
    def _normalize_limit(
        limit,
    ):
        if limit is None:
            return None

        if (
            not isinstance(limit, int)
            or limit <= 0
        ):
            raise ValueError(
                "limit must be a positive integer."
            )

        return limit

    @staticmethod
    def _reject_sensitive_content(
        content,
    ):
        sensitive_patterns = [
            r"\bpassword\s+(?:is|=|:)\s*\S+",
            r"\bpasscode\s+(?:is|=|:)\s*\S+",
            r"\bpin\s+(?:is|=|:)\s*\d+",
            r"\bapi[\s_-]*key\s+(?:is|=|:)\s*\S+",
            r"\baccess[\s_-]*token\s+(?:is|=|:)\s*\S+",
            r"\bsecret\s+(?:is|=|:)\s*\S+",
            r"\b\d{3}-\d{2}-\d{4}\b",
        ]

        if any(
            re.search(
                pattern,
                content,
                flags=re.IGNORECASE,
            )
            for pattern in sensitive_patterns
        ):
            raise SensitiveMemoryError(
                "SATURN will not store passwords, PINs, "
                "tokens, API keys, secrets, or Social "
                "Security numbers in personal memory."
            )

    @staticmethod
    def _utc_now():
        return datetime.now(
            timezone.utc
        ).isoformat()

    @staticmethod
    def _row_to_dict(
        row,
    ):
        return {
            "memory_id": row["memory_id"],
            "content": row["content"],
            "category": row["category"],
            "source": row["source"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }
