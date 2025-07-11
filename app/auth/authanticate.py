from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.jwt_handler import verify_access_token
from services.auth.cookieauth import OAuth2PasswordBearerWithCookie
from fastapi import Request, HTTPException
from auth.jwt_handler import decode_access_token
from database.config import get_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/signin")
settings = get_settings()


async def authenticate(token:str=Depends(oauth2_scheme))-> str:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sign in for access"
        )
    decoded_token=verify_access_token(token)
    return decoded_token["user"]

oauth2_scheme_cookie=OAuth2PasswordBearerWithCookie(tokenUrl="/home/token")

def authenticate_cookie(request: Request):
    token = request.cookies.get(settings.COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=403, detail="Not authenticated")

    try:
        payload = decode_access_token(token)
        email = payload.get("user")
        if not email:
            raise HTTPException(status_code=403, detail="Invalid authentication")
    except Exception as e:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

    return {"email": email}