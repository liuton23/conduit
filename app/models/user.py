from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.db.session import Base
import secrets
import bcrypt

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: secrets.token_hex(16))
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode(), password_hash.encode())

    @staticmethod
    def validate_password(password: str) -> list[str]:
        errors = []
        if len(password) < 8:
            errors.append("Password must be at least 8 characters")
        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one number")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.?" for c in password):
            errors.append("Password must contain at least one special character")
        return errors