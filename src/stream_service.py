import threading
import time
from collections import deque
from datetime import datetime

STREAM_BUFFER = deque(maxlen=100)
_LOCK = threading.Lock()


def push_stream_event(event_type: str, message: str, payload: dict | None = None):
    item = {
        'timestamp': datetime.utcnow().isoformat(),
        'event_type': event_type,
        'message': message,
        'payload': payload or {},
    }
    with _LOCK:
        STREAM_BUFFER.append(item)
    return item


def stream_snapshot():
    with _LOCK:
        return list(STREAM_BUFFER)


def generate_live_stream():
    while True:
        push_stream_event(
            'sales_stream',
            'New transaction batch received',
            {
                'customers': 14,
                'revenue': 5200,
                'segment': 'VIP',
                'region': 'North America',
            },
        )
        time.sleep(3)


def start_live_stream():
    global _STREAM_THREAD
    if '_STREAM_THREAD' in globals() and _STREAM_THREAD.is_alive():
        return
    _STREAM_THREAD = threading.Thread(target=generate_live_stream, daemon=True)
    _STREAM_THREAD.start()
