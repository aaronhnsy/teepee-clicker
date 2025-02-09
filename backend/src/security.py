import itsdangerous
import passlib.context

from src.types import SessionData


__all__ = [
    "AUTHENTICATION_SIGNER",
    "PASSWORD_CONTEXT",
    "sign_session_id",
    "unsign_session_id",
    "hash_password",
    "verify_password",
]


AUTHENTICATION_SIGNER = itsdangerous.URLSafeTimedSerializer(
    "X0KeOqRa2Hsc3u3bf6DdT2pmr3tbGRwhdVq4wBJrETWU7EdDalLJzjuJdlsqQtWE"
    "wGJOBEhOSwQ3a6Vbdvaa7Oy8ASGs0Oneas7RdyWrz0xuGkBrRZ8NzGDJqRKakbW7",
    salt="authentication"
)
PASSWORD_CONTEXT = passlib.context.CryptContext(schemes=["argon2"])
MAX_SESSION_AGE: int = 60 * 60 * 24 * 31


def sign_session_id(data: SessionData) -> str:
    return AUTHENTICATION_SIGNER.dumps(data)


def unsign_session_id(session_id: str) -> SessionData:
    return AUTHENTICATION_SIGNER.loads(session_id, max_age=MAX_SESSION_AGE)


def hash_password(password: str) -> str:
    return PASSWORD_CONTEXT.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return PASSWORD_CONTEXT.verify(password, hashed_password)
