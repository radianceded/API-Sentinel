from passlib.context import CryptContext
from datetime import datetime,timedelta,timezone
from typing import Any
from jose import jwt,JWTError
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#加密密码
def hash_password(password:str)->str:
    return pwd_context.hash(password)
#验证密码
def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)
#发放登录凭证
def create_access_token(subject: str|Any)->str:
    expire = datetime.now(timezone.utc)+ timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload ={
        "sub": str(subject),
        "exp": expire,
    }
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
#验证登录凭证
def decode_access_token(token:str)->dict[str,Any]|None:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError:
        return None