from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.request_log import RequestLog


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/request-logs")
def list_request_logs(db: Session = Depends(get_db)):
    logs = (
        db.query(RequestLog)
        .order_by(RequestLog.id.desc())
        .limit(50)
        .all()
    )

    return logs