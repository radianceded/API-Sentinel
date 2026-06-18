from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SecurityEventOut(BaseModel):
    id: int
    request_log_id: int | None
    user_id: int | None
    event_type: str
    risk_level: str
    source_ip: str | None
    description: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
