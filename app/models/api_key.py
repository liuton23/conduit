from sqlalchemy import Column, ForeignKey, String, Boolean, DateTime, Float, Integer
from sqlalchemy.sql import func
from app.db.session import Base
from app.models.enums import SpendLimitAction
import secrets

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(String, primary_key=True, default=lambda: secrets.token_hex(16))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    key_hash = Column(String, unique=True, index=True)
    name = Column(String)
    project = Column(String, nullable=False)  # required, one key per project
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_used_at = Column(DateTime(timezone=True), nullable=True)

    # spend limits
    spend_limit_usd = Column(Float, nullable=True)
    spend_limit_action = Column(String, default=SpendLimitAction.WARN.value)
    webhook_url = Column(String, nullable=True)

    # rate limits
    rate_limit_requests = Column(Integer, nullable=True)
    rate_limit_window = Column(Integer, nullable=True)