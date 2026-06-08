from datetime import datetime
from pydantic import BaseModel


class RequestLogOut(BaseModel):
    id: int
    user_id: int | None
    ip_address: str | None
    method: str
    path: str
    status_code: int
    latency_ms: float
    created_at: datetime

    class Config:
        from_attributes = True