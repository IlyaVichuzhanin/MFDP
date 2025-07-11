from fastapi import APIRouter, Body, Depends, Request, Form
from database.database import get_session
from services.crud import user as UserService
from services.crud import response as ResponseService
from auth.hash_password import HashPassword
from fastapi.templating import Jinja2Templates
from database.config import get_settings
from auth.authanticate import authenticate_cookie



response_router = APIRouter(tags=['Response'])
hash_password = HashPassword() 
templates = Jinja2Templates(directory="view")
settings=get_settings()

@response_router.get("/get_user_predictions")
async def get_user_predictions(request: Request, session=Depends(get_session)):
    token=request.cookies.get(settings.COOKIE_NAME)
    user_email = await authenticate_cookie(token)
    if token:
        if user_email:
            user = UserService.get_user_by_email(user_email,session)
            if(user):
                responses = ResponseService.get_user_responses(user.id,session)
                context={
                    "responses": responses,
                    "request": request
                }
                return templates.TemplateResponse("prediction_hystory.html", context) 
    
    return templates.TemplateResponse("signup.html", context)
