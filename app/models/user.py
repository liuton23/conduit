from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.db.session import Base
import secrets
import hashlib

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: secrets.token_hex(16))
    access_key_hash = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    @staticmethod
    def hash_access_key(access_key: str) -> str:
        return hashlib.sha256(access_key.encode()).hexdigest()