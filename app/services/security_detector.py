from datetime import datetime,timedelta

from sqlalchemy.orm import Session

from app.models.request_log import RequestLog
from app.models.security_event import SecurityEvent


def detect_login_bruteforce(
    db: Session,
    ip_address: str | None,
) -> None:
    if ip_address is None:
        return

    window_start = datetime.utcnow() - timedelta(minutes=5)

    failed_count = (
        db.query(RequestLog)
        .filter(RequestLog.ip_address == ip_address)
        .filter(RequestLog.path == "/auth/login")
        .filter(RequestLog.method == "POST")
        .filter(RequestLog.status_code == 401)
        .filter(RequestLog.created_at >= window_start)
        .count()
    )

    if failed_count < 5:
        return

    existing_event = (
        db.query(SecurityEvent)
        .filter(SecurityEvent.source_ip == ip_address)
        .filter(SecurityEvent.event_type == "LOGIN_BRUTE_FORCE")
        .filter(SecurityEvent.created_at >= window_start)
        .first()
    )

    if existing_event:
        return

    event = SecurityEvent(
        request_log_id=None,
        user_id=None,
        event_type="LOGIN_BRUTE_FORCE",
        risk_level="MEDIUM",
        source_ip=ip_address,
        description=f"IP {ip_address} failed login {failed_count} times within 5 minutes.",
    )

    db.add(event)