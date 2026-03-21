from sqlalchemy import Column, String, Integer, Float, DateTime, Text
from sqlalchemy.sql import func
from app.db.session import Base

class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, index=True)
    model = Column(String)
    provider = Column(String)
    input_tokens = Column(Integer)
    output_tokens = Column(Integer)
    total_tokens = Column(Integer)
    cost_usd = Column(Float)
    latency_ms = Column(Float)
    status_code = Column(Integer)
    project = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())