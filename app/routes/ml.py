from fastapi import APIRouter, Depends, HTTPException, Request, Form
from datetime import datetime
from models.request import Request as MLRequest
from services.crud.request import create_request
from database.database import get_session
from services.rm.rabbitmq import RabbitMQ
from models.user import User
from services.crud import user as UserService
import json
import uuid
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from database.config import get_settings
from auth.authanticate import authenticate_cookie



ml_router = APIRouter()
date_format = "%Y-%m-%d %H:%M:%S"
ml_router=APIRouter()
templates = Jinja2Templates(directory="view")
templates = Jinja2Templates(directory="view")
settings=get_settings()
date_format = "%Y-%m-%d %H:%M:%S"


@ml_router.get('/get_prediction')
async def get_prediction(
    request: Request,
    cluster_number: int, 
    trip_date_time: datetime,  
    session: Session = Depends(get_session)
):

    token=request.cookies.get(settings.COOKIE_NAME)
    user_email = await authenticate_cookie(token)
    if token:
        if user_email:
            user = UserService.get_user_by_email(user_email,session)
            if(user):
                try:
                    new_request = MLRequest(id=uuid.uuid4(), cluster=cluster_number, pickup_date_time=trip_date_time, user_id=user.id)
                    create_request(new_request=new_request, session=session)
                    rabbitmq = RabbitMQ()
                    message = json.dumps(
                        {
                            "request_id": str(new_request.id), 
                        }
                    )
                    rabbitmq.send_task(message=message)
                    return templates.TemplateResponse("personal_cabinet.html", {"request": request})
                    
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))


@ml_router.post('/get_prediction')
async def post_prediction(
    request: Request,
    cluster_number: int = Form(...),
    trip_date: str = Form(...),
    trip_time: str = Form(...),
    session: Session = Depends(get_session)
):
    try:
        user_payload = await authenticate_cookie(request)
        user_email = user_payload.get('user') if user_payload else None
    except Exception:
        return templates.TemplateResponse("personal_cabinet.html", {"request": request, "error": "Ошибка авторизации"}, status_code=403)
    if user_email:
        user = UserService.get_user_by_email(user_email, session)
        if user:
            try:
                trip_date_time = datetime.strptime(f"{trip_date} {trip_time}", "%Y-%m-%d %H:%M")
                new_request = MLRequest(id=uuid.uuid4(), cluster=cluster_number, pickup_date_time=trip_date_time, user_id=user.id)
                create_request(new_request=new_request, session=session)
                rabbitmq = RabbitMQ()
                message = json.dumps({"request_id": str(new_request.id)})
                rabbitmq.send_task(message=message)
                return templates.TemplateResponse("personal_cabinet.html", {"request": request, "success": True})
            except Exception as e:
                return templates.TemplateResponse("personal_cabinet.html", {"request": request, "error": str(e)})
    return templates.TemplateResponse("personal_cabinet.html", {"request": request, "error": "Ошибка авторизации"}, status_code=403)





