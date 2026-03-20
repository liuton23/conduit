import hashlib
import secrets

def generate_api_key() -> tuple[str, str]:
    """Returns (raw_key, hashed_key)"""
    raw_key = f"cdt-{secrets.token_urlsafe(32)}"
    hashed = hashlib.sha256(raw_key.encode()).hexdigest()
    return raw_key, hashed

def hash_api_key(raw_key: str) -> str:
    return hashlib.sha256(raw_key.encode()).hexdigest()