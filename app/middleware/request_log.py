import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.db.session import SessionLocal
from app.models.request_log import RequestLog
from app.core.security import decode_access_token
from app.models.user import User


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        latency_ms = (time.time() - start_time) * 1000

        db = SessionLocal()
        try:
            user_id = None

            authorization = request.headers.get("Authorization")
            if authorization and authorization.startswith("Bearer "):
                token = authorization.replace("Bearer ", "")
                payload = decode_access_token(token)

                if payload:
                    sub = payload.get("sub")
                    if sub:
                        try:
                            user_id = int(sub)
                            user = db.query(User).filter(User.id == user_id).first()
                            if user is None:
                                user_id = None
                        except ValueError:
                            user_id = None

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
            db.commit()

        except Exception:
            db.rollback()
        finally:
            db.close()

        return response