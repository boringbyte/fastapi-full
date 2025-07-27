from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .utils import decode_token


class AccessTokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)
        if not self.is_valid_token(token):
            HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                          detail="Invalid or expired token")
        if token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token"
            )
        return token_data

    def is_valid_token(self, token: str) -> bool:
        token_data = decode_token(token)
        return token_data is not None
