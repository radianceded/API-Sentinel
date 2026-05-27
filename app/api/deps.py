from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.core.security import decode_access_token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(token:str=Depends(oauth2_scheme)):
    payload=decode_access_token(tokenURL="/auth/login")
    return payload