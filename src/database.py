from backend import get_backend

_backend = get_backend()


def init_db():
    if hasattr(_backend, '_init_db'):
        _backend._init_db()


def verify_login(username: str, password: str):
    return _backend.authenticate(username, password)


def log_event(username: str, event_type: str, message: str, payload: dict | None = None):
    _backend.save_event(username, event_type, message, payload)


def get_recent_events(limit: int = 10):
    return _backend.fetch_events(limit)
