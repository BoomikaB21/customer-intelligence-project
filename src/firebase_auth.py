import os

from firebase_admin import auth as firebase_auth


def get_firebase_auth():
    if os.getenv('USE_FIREBASE', '0').lower() not in {'1', 'true', 'yes'}:
        return None
    return firebase_auth


def sign_in_with_email_password(email: str, password: str):
    auth = get_firebase_auth()
    if auth is None:
        return None
    try:
        user = auth.get_user_by_email(email)
        return {'uid': user.uid, 'email': user.email, 'provider': 'firebase'}
    except Exception:
        return None
