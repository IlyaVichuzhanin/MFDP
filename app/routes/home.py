from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from auth.hash_password import HashPassword
from database.config import get_settings
from auth.authanticate import authenticate_cookie
from services.crud import user as UserService
from database.database import get_session


settings=get_settings()
home_router=APIRouter(tags=['Home'])
hash_password=HashPassword()
templates = Jinja2Templates(directory="view")



@home_router.get("/", response_class=HTMLResponse)
async def index(request: Request, session=Depends(get_session)):
    return templates.TemplateResponse("index.html", {"request": request})
            
 
    

    