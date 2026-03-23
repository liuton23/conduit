from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.db.session import get_db
from app.models.request_log import RequestLog
from app.middleware.session import validate_session
from app.constants import UNTAGGED_PROJECT, DATE_FORMAT
from typing import Optional

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
async def get_stats(
    db: AsyncSession = Depends(get_db),
    session: str = Depends(validate_session),
    project: Optional[str] = Query(None)
):
    query = select(
        func.count(RequestLog.id).label("total_requests"),
        func.sum(RequestLog.total_tokens).label("total_tokens"),
        func.sum(RequestLog.cost_usd).label("total_cost"),
        func.avg(RequestLog.latency_ms).label("avg_latency_ms"),
    )

    if project:
        query = query.where(RequestLog.project == project)

    result = await db.execute(query)
    row = result.one()

    return {
        "total_requests": row.total_requests or 0,
        "total_tokens": row.total_tokens or 0,
        "total_cost_usd": round(row.total_cost or 0, 6),
        "avg_latency_ms": round(row.avg_latency_ms or 0, 2),
    }

@router.get("/usage/by-model")
async def usage_by_model(
    db: AsyncSession = Depends(get_db),
    session: str = Depends(validate_session),
):
    result = await db.execute(
        select(
            RequestLog.model,
            func.count(RequestLog.id).label("requests"),
            func.sum(RequestLog.total_tokens).label("tokens"),
            func.sum(RequestLog.cost_usd).label("cost"),
        )
        .group_by(RequestLog.model)
        .order_by(desc("cost"))
    )
    rows = result.all()

    return [
        {
            "model": row.model,
            "requests": row.requests,
            "tokens": row.tokens,
            "cost_usd": round(row.cost, 6),
        }
        for row in rows
    ]

@router.get("/usage/by-project")
async def usage_by_project(
    db: AsyncSession = Depends(get_db),
    session: str = Depends(validate_session),
):
    result = await db.execute(
        select(
            RequestLog.project,
            func.count(RequestLog.id).label("requests"),
            func.sum(RequestLog.total_tokens).label("tokens"),
            func.sum(RequestLog.cost_usd).label("cost"),
        )
        .group_by(RequestLog.project)
        .order_by(desc("cost"))
    )
    rows = result.all()

    return [
        {
            "project": row.project or UNTAGGED_PROJECT,
            "requests": row.requests,
            "tokens": row.tokens,
            "cost_usd": round(row.cost, 6),
        }
        for row in rows
    ]

@router.get("/usage/over-time")
async def usage_over_time(
    db: AsyncSession = Depends(get_db),
    session: str = Depends(validate_session),
):
    result = await db.execute(
        select(
            func.date_trunc("day", RequestLog.created_at).label("date"),
            func.count(RequestLog.id).label("requests"),
            func.sum(RequestLog.total_tokens).label("tokens"),
            func.sum(RequestLog.cost_usd).label("cost"),
        )
        .group_by("date")
        .order_by("date")
    )
    rows = result.all()

    return [
        {
            "date": row.date.strftime(DATE_FORMAT),
            "requests": row.requests,
            "tokens": row.tokens,
            "cost_usd": round(row.cost, 6),
        }
        for row in rows
    ]