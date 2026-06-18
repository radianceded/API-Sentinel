import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.security_detector import detect_login_bruteforce
from app.db.session import SessionLocal
from app.models.request_log import RequestLog
from app.core.security import decode_access_token
from app.models.user import User


def _get_user_id_from_authorization(authorization: str | None, db) -> int | None:
    if not authorization:
        return None

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None

    payload = decode_access_token(token.strip())
    if not payload:
        return None

    sub = payload.get("sub")
    if not sub:
        return None

    try:
        user_id = int(sub)
    except (TypeError, ValueError):
        return None

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return None

    return user_id


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        latency_ms = (time.time() - start_time) * 1000

        db = SessionLocal()
        try:
            user_id = _get_user_id_from_authorization(
                authorization=request.headers.get("Authorization"),
                db=db,
            )

            client_host = request.client.host if request.client else None

            log = RequestLog(
                user_id=user_id,
                ip_address=client_host,
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                latency_ms=latency_ms,
            )

            db.add(log)
            db.flush()
            detect_login_bruteforce(
                db=db,
                ip_address=client_host,
            )
            db.commit()

        except Exception:
            db.rollback()
        finally:
            db.close()

        return response
