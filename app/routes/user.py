from fastapi import APIRouter, Body, HTTPException, status, Depends, Response, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from database.database import get_session
from models.user import User
from services.crud import user as UserService
from services.crud import response as ResponseService
from typing import List
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from forms.usersignupform import UserSignUpForm
from fastapi.templating import Jinja2Templates
from database.config import get_settings
from fastapi.responses import RedirectResponse
from auth.authanticate import authenticate_cookie



user_router = APIRouter(tags=['User'])
hash_password = HashPassword() 
templates = Jinja2Templates(directory="view")
settings=get_settings()

@user_router.post('/signin')
def signin(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

@user_router.post('/logout')
def logout(request: Request):
    request.cookies.clear()
    return templates.TemplateResponse("index.html", {"request": request})

@user_router.post('/signup')
def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request}) 

@user_router.post('/personal_account')
def get_personal_account(request: Request):
    return templates.TemplateResponse("personal_cabinet.html", {"request": request}) 
    
 
@user_router.post('/register')
async def register(response: Response, email: str = Form(...), password: str = Form(...), session=Depends(get_session)):
    user_exist=UserService.get_user_by_email(email, session)    
    if user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with supplied username exists")
    
    user_exist=UserService.get_user_by_email(email, session)
    if user_exist is None:
        hashed_password=hash_password.create_hash(password)
        new_user=User(email=email, hashed_password=hashed_password)
        UserService.create_user(new_user, session)
        access_token=create_access_token(new_user.email)
        redirect=RedirectResponse(url="/user/personal_account")
        redirect.set_cookie(key=settings.COOKIE_NAME, value=access_token, httponly=True, expires=settings.TIME_EXPIRES)
    return redirect


@user_router.post('/login')
async def login(response: Response, email: str = Form(...), password: str = Form(...), session=Depends(get_session)):
    user_exist=UserService.get_user_by_email(email, session)
    if user_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    if hash_password.verify_hash(password, user_exist.hashed_password):
        access_token=create_access_token(user_exist.email)
        redirect=RedirectResponse(url="/user/personal_account")
        redirect.set_cookie(key=settings.COOKIE_NAME, value=access_token, httponly=True, expires=settings.TIME_EXPIRES)
    return redirect





