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
from sqlalchemy.orm import Session



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
async def register(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    # Проверяем, существует ли пользователь
    user_exist = UserService.get_user_by_email(email, session)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied email already exists"
        )

    # Создаем нового пользователя
    hashed_password = hash_password.create_hash(password)
    new_user = User(email=email, hashed_password=hashed_password)
    UserService.create_user(new_user, session)

    # Генерируем токен
    access_token = create_access_token(new_user.email)

    # Редиректим на личный кабинет с установкой кук
    redirect_url = "/user/personal_account"
    redirect = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)

    # Устанавливаем куку
    redirect.set_cookie(
        key=settings.COOKIE_NAME,
        value=access_token,
        httponly=True,
        secure=False,  # True, если используете HTTPS
        expires=settings.TIME_EXPIRES,
        path="/",
        domain="localhost"  # или ваш домен
    )

    return redirect


@user_router.post('/login')
async def login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    # Проверяем существование пользователя
    user = UserService.get_user_by_email(email, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )

    # Проверяем пароль
    if not hash_password.verify_hash(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    # Создаем токен
    access_token = create_access_token(user.email)

    # Редиректим с корректным статус-кодом
    redirect_url = "/user/personal_account"
    redirect = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)

    # Устанавливаем куку
    redirect.set_cookie(
        key=settings.COOKIE_NAME,
        value=access_token,
        httponly=True,
        secure=False,  # True, если используете HTTPS
        expires=settings.TIME_EXPIRES,
        path="/",
        domain="localhost"  # или ваш домен
    )

    return redirect

@user_router.get('/personal_account')
def get_personal_account(request: Request, user: dict = Depends(authenticate_cookie)):
    return templates.TemplateResponse("personal_cabinet.html", {"request": request})





