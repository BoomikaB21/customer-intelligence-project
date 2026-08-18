import hashlib
import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except Exception:  # pragma: no cover
    firebase_admin = None
    credentials = None
    firestore = None

DB_PATH = Path(__file__).resolve().parent.parent / 'data' / 'customer_app.db'


def load_env_file():
    env_path = Path(__file__).resolve().parent.parent / '.env'
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


load_env_file()


def backend_mode():
    return 'firebase' if os.getenv('USE_FIREBASE', '0').lower() in {'1', 'true', 'yes'} and os.getenv('FIREBASE_CREDENTIALS_PATH') else 'local'


class LocalBackend:
    def __init__(self, db_path: str | Path = DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._connect()
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                event_type TEXT NOT NULL,
                message TEXT NOT NULL,
                payload TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        admin = conn.execute("SELECT id FROM users WHERE username = 'admin'").fetchone()
        if admin is None:
            conn.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                ('admin', self._hash('admin123'), 'admin@company.com'),
            )
        conn.commit()
        conn.close()

    @staticmethod
    def _hash(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self, username: str, password: str):
        conn = self._connect()
        row = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password_hash = ?",
            (username, self._hash(password)),
        ).fetchone()
        conn.close()
        return dict(row) if row else None

    def save_event(self, username: str, event_type: str, message: str, payload=None):
        conn = self._connect()
        conn.execute(
            "INSERT INTO events (username, event_type, message, payload) VALUES (?, ?, ?, ?)",
            (username, event_type, message, json.dumps(payload) if payload is not None else None),
        )
        conn.commit()
        conn.close()

    def fetch_events(self, limit: int = 10):
        conn = self._connect()
        rows = conn.execute(
            "SELECT username, event_type, message, payload, created_at FROM events ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
        conn.close()
        payload = []
        for row in rows:
            item = dict(row)
            if item.get('payload'):
                item['payload'] = json.loads(item['payload'])
            payload.append(item)
        return payload


class FirebaseBackend:
    def __init__(self, credential_path: str | None = None):
        self.credential_path = credential_path or os.getenv('FIREBASE_CREDENTIALS_PATH')
        self._client = None
        if firebase_admin is not None and self.credential_path:
            if not firebase_admin._apps:
                cred = credentials.Certificate(self.credential_path)
                firebase_admin.initialize_app(cred)
            self._client = firestore.client()

    @staticmethod
    def _hash(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def _ensure_client(self):
        if self._client is None:
            raise RuntimeError('Firebase backend is not configured. Set FIREBASE_CREDENTIALS_PATH or disable Firebase mode.')
        return self._client

    def authenticate(self, username: str, password: str):
        if self._client is None:
            return None
        doc = self._client.collection('users').document(username).get()
        if not doc.exists:
            return None
        user = doc.to_dict()
        if user.get('password_hash') == hashlib.sha256(password.encode()).hexdigest():
            return {'username': username, 'email': user.get('email')}
        return None

    def save_event(self, username: str, event_type: str, message: str, payload=None):
        client = self._ensure_client()
        client.collection('events').add({
            'username': username,
            'event_type': event_type,
            'message': message,
            'payload': payload or {},
            'created_at': datetime.utcnow().isoformat(),
        })

    def fetch_events(self, limit: int = 10):
        client = self._ensure_client()
        docs = client.collection('events').order_by('created_at', direction='DESCENDING').limit(limit).stream()
        return [
            {
                'username': doc.to_dict().get('username'),
                'event_type': doc.to_dict().get('event_type'),
                'message': doc.to_dict().get('message'),
                'payload': doc.to_dict().get('payload'),
                'created_at': doc.to_dict().get('created_at'),
            }
            for doc in docs
        ]


def get_backend():
    if backend_mode() == 'firebase' and firebase_admin is not None and os.getenv('FIREBASE_CREDENTIALS_PATH'):
        return FirebaseBackend()
    return LocalBackend()
