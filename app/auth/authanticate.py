from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.jwt_handler import verify_access_token
from services.auth.cookieauth import OAuth2PasswordBearerWithCookie
from fastapi import Request, HTTPException
from auth.jwt_handler import decode_access_token
from database.config import get_settings
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
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

async def authenticate_cookie(request: Request):
    logger.debug("Checking for cookie...")
    cookie_value = request.cookies.get(settings.COOKIE_NAME)
    if not cookie_value:
        logger.warning("Cookie not found")
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        # Здесь предполагается декодирование JWT
        decoded_token = decode_access_token(cookie_value)  # Замените на реальный метод декодирования
        logger.debug(f"Decoded token: {decoded_token}")
        return decoded_token
    except Exception as e:
        logger.error(f"Error decoding token: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")