from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from assistant_tools.list_tool import get_all_lists
from core.saturn_instance import get_saturn


app = FastAPI(
    title="S.A.T.U.R.N. API",
    description="Local API for the S.A.T.U.R.N. assistant.",
    version="0.4.0",
)

# The API may create, view, and cancel alarms, but it must not
# own alarm firing. The voice/runtime SATURN process owns the
# background alarm monitor.
saturn = get_saturn(start_alarm_monitor=False)


PWA_DIR = Path(__file__).resolve().parent.parent / "pwa"

@app.get("/app/service-worker.js")
def service_worker():
    return FileResponse(
        PWA_DIR / "service-worker.js",
        media_type="application/javascript",
        headers={"Service-Worker-Allowed": "/"},
    )


app.mount(
    "/app",
    StaticFiles(directory=PWA_DIR),
    name="app",
)


class QueryRequest(BaseModel):
    text: str
    session_id: str | None = Field(
        default=None,
        max_length=128,
    )


class ListCreateRequest(BaseModel):
    name: str


class ListItemRequest(BaseModel):
    item: str


class AlarmCreateRequest(BaseModel):
    time: str


def _make_json_safe(value):
    """
    Convert subsystem results into JSON-compatible values.

    Some deterministic engines return objects such as SymPy numbers,
    which FastAPI cannot serialize directly.
    """

    if value is None or isinstance(
        value,
        (
            str,
            int,
            float,
            bool,
        ),
    ):
        return value

    if isinstance(value, dict):
        return {
            str(key): _make_json_safe(item)
            for key, item in value.items()
        }

    if isinstance(
        value,
        (
            list,
            tuple,
            set,
        ),
    ):
        return [
            _make_json_safe(item)
            for item in value
        ]

    return str(value)


def run_saturn_query(
    text: str,
    session_id=None,
):
    text = text.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Query text cannot be empty.",
        )

    try:
        result = saturn.handle_query(
            text,
            session_id=session_id,
        )

        return _make_json_safe(result)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"S.A.T.U.R.N. query failed: {exc}",
        ) from exc


@app.get("/")
def root():
    return FileResponse(
        PWA_DIR / "index.html"
    )


@app.get("/api/health")
def health():
    return {
        "success": True,
        "status": "online",
    }


@app.post("/api/query")
def query_saturn(request: QueryRequest):
    result = run_saturn_query(
        request.text,
        session_id=request.session_id,
    )

    return {
        "success": True,
        "query": request.text.strip(),
        "result": result,
    }


# ============================================================
# LISTS API
# ============================================================


@app.get("/api/lists")
def get_lists():
    result = get_all_lists()

    return {
        "success": result.get(
            "success",
            False,
        ),
        "result": result,
    }


@app.post("/api/lists")
def create_list(request: ListCreateRequest):
    result = run_saturn_query(
        f"create a {request.name} list"
    )

    return {
        "success": result.get(
            "success",
            False,
        ),
        "result": result,
    }


@app.get("/api/lists/{list_name}")
def get_list(list_name: str):
    result = run_saturn_query(
        f"show my {list_name} list"
    )

    return {
        "success": result.get(
            "success",
            False,
        ),
        "result": result,
    }


@app.post("/api/lists/{list_name}/items")
def add_list_item(
    list_name: str,
    request: ListItemRequest,
):
    result = run_saturn_query(
        f"add {request.item} to my {list_name} list"
    )

    return {
        "success": result.get(
            "success",
            False,
        ),
        "result": result,
    }


@app.delete("/api/lists/{list_name}/items/{item}")
def remove_list_item(
    list_name: str,
    item: str,
):
    result = run_saturn_query(
        f"remove {item} from my {list_name} list"
    )

    return {
        "success": result.get(
            "success",
            False,
        ),
        "result": result,
    }


@app.delete("/api/lists/{list_name}/items")
def clear_list(list_name: str):
    result = run_saturn_query(
        f"clear my {list_name} list"
    )

    return {
        "success": result.get(
            "success",
            False,
        ),
        "result": result,
    }


@app.delete("/api/lists/{list_name}")
def delete_list(list_name: str):
    result = run_saturn_query(
        f"delete my {list_name} list"
    )

    return {
        "success": result.get(
            "success",
            False,
        ),
        "result": result,
    }


# ============================================================
# ALARMS API
# ============================================================


@app.get("/api/alarms")
def get_alarms():
    result = run_saturn_query(
        "show my alarms"
    )

    return {
        "success": result.get(
            "success",
            False,
        ),
        "result": result,
    }


@app.post("/api/alarms")
def create_alarm(request: AlarmCreateRequest):
    result = run_saturn_query(
        f"set an alarm for {request.time}"
    )

    return {
        "success": result.get(
            "success",
            False,
        ),
        "result": result,
    }


@app.post("/api/alarms/stop")
def stop_ringing_alarm():
    result = run_saturn_query(
        "stop the alarm"
    )

    return {
        "success": result.get(
            "success",
            False,
        ),
        "result": result,
    }


@app.post("/api/alarms/snooze")
def snooze_ringing_alarm():
    result = run_saturn_query(
        "snooze the alarm for 10 minutes"
    )

    return {
        "success": result.get(
            "success",
            False,
        ),
        "result": result,
    }


@app.delete("/api/alarms")
def cancel_all_alarms():
    result = run_saturn_query(
        "cancel all my alarms"
    )

    return {
        "success": result.get(
            "success",
            False,
        ),
        "result": result,
    }


@app.delete("/api/alarms/{alarm_time}")
def cancel_alarm(alarm_time: str):
    result = run_saturn_query(
        f"cancel my {alarm_time} alarm"
    )

    return {
        "success": result.get(
            "success",
            False,
        ),
        "result": result,
    }
