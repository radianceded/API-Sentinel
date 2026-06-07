from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.request_log import RequestLogOut
from app.db.session import get_db
from app.models.request_log import RequestLog


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/request-logs", response_model=list[RequestLogOut])
def list_request_logs(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    logs = (
        db.query(RequestLog)
        .order_by(RequestLog.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return logs

    