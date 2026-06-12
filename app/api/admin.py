from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.models.security_event import SecurityEvent
from app.schemas.security_event import SecurityEventOut
from app.api.deps import get_current_admin_user
from app.db.session import get_db
from app.models.request_log import RequestLog
from app.models.user import User
from app.schemas.request_log import RequestLogOut


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/request-logs", response_model=list[RequestLogOut])
def list_request_logs(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    logs = (
        db.query(RequestLog)
        .order_by(RequestLog.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return logs

@router.get("/security-events", response_model=list[SecurityEventOut])
def list_security_events(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    events = (
        db.query(SecurityEvent)
        .order_by(SecurityEvent.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return events