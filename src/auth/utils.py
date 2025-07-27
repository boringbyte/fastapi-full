import jwt
import uuid
import logging
from datetime import datetime, timedelta

from src.config import Config
from passlib.context import CryptContext


passwd_context = CryptContext(
    schemes=['bcrypt']
)
ACCESS_TOKEN_EXPIRY = 3600  # This is in seconds

def generate_passwd_hash(password: str) -> str:
    password_hash = passwd_context.hash(password)
    return password_hash

def verify_password(password: str, password_hash: str) -> bool:
    return passwd_context.verify(password, password_hash)

def create_access_token(user_data: dict, expiry: timedelta=None, refresh: bool=False) -> str:
    expire_at = datetime.now() + (expiry or timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload = {'user': user_data,
               'exp': expire_at,
               "jti": str(uuid.uuid4()),
               'refresh': refresh}
    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )
    return token

def decode_token(token: str) -> dict | None:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(f"Failed to decode token with error: {e}")
        return None
