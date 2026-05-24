from datetime import datetime
from sqlalchemy import func
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True,index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255),nullable=False)
    role: Mapped[str] = mapped_column(String(20),nullable=False,default="MEMBER")
    is_active: Mapped[bool] = mapped_column(default=True,nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False,server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=False,server_default=func.now(), onupdate=func.now())