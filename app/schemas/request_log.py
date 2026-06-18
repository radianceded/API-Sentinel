from datetime import datetime
from pydantic import BaseModel, ConfigDict


class RequestLogOut(BaseModel):
    id: int
    user_id: int | None
    ip_address: str | None
    method: str
    path: str
    status_code: int
    latency_ms: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
