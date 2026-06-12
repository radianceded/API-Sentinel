from datetime import datetime

from pydantic import BaseModel


class SecurityEventOut(BaseModel):
    id: int
    request_log_id: int | None
    user_id: int | None
    event_type: str
    risk_level: str
    source_ip: str | None
    description: str
    created_at: datetime

    class Config:
        from_attributes = True