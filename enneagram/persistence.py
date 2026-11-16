"""Lightweight, file-backed session persistence.

Streamlit's session_state lives only in the live connection's memory - a
browser refresh, a dropped websocket, or a Cloud reconnect can spin up a
fresh session with everything lost. To make an in-progress assessment
survive that, we tag the browser URL with an opaque session token and
mirror the answerable state to a small JSON file on disk, keyed by that
token. On reconnect, the token is still in the URL, so we can restore from
disk even though session_state itself started over.
"""

import json
import os
import time

SESSIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".sessions")

PERSISTED_KEYS = [
    "stage", "client_name", "client_notes", "authed", "lang",
    "type_answers", "instinct_answers", "functioning_answers",
    "type_page", "instinct_page", "functioning_page",
    "type_order", "instinct_order",
]


def _path(token):
    safe = "".join(c for c in token if c.isalnum() or c in "-_")
    return os.path.join(SESSIONS_DIR, f"{safe}.json")


def save_session(token, state):
    os.makedirs(SESSIONS_DIR, exist_ok=True)
    data = {k: state[k] for k in PERSISTED_KEYS if k in state}
    data["_saved_at"] = time.time()
    # Session-state dict keys for answers are ints from Streamlit widgets; JSON needs string keys.
    tmp = _path(token) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f)
    os.replace(tmp, _path(token))


def delete_session(token):
    path = _path(token)
    if os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            pass


def load_session(token):
    path = _path(token)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

    for dict_key in ("type_answers", "instinct_answers", "functioning_answers"):
        if dict_key in data:
            data[dict_key] = {int(k): v for k, v in data[dict_key].items()}
    return data
