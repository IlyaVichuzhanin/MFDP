from fastapi import APIRouter, Depends, HTTPException, Request
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





