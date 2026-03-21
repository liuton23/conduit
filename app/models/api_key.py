from sqlalchemy import Column, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from app.db.session import Base
from app.models.enums import SpendLimitAction
import secrets

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(String, primary_key=True, default=lambda: secrets.token_hex(16))
    key_hash = Column(String, unique=True, index=True)
    name = Column(String)
    project = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_used_at = Column(DateTime(timezone=True), nullable=True)

    # spend limits
    spend_limit_usd = Column(Float, nullable=True)
    spend_limit_action = Column(String, default=SpendLimitAction.WARN) # warn or block
    webhook_url = Column(String, nullable=True)