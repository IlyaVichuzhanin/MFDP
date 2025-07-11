from fastapi import APIRouter, Body, HTTPException, status, Depends, File, UploadFile, Form, Request, Response
from database.database import get_session
from services.crud.request import create_request
import os
from services.rm.rabbitmq import RabbitMQ
import json
import uuid
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.request import Request as MLRequest
from database.config import get_settings
from auth.authanticate import authenticate_cookie
from services.crud import user as UserService
from fastapi import APIRouter, HTTPException
import pandas as pd
import joblib
import os
from datetime import datetime



ml_router=APIRouter()
templates = Jinja2Templates(directory="view")
templates = Jinja2Templates(directory="view")
settings=get_settings()
date_format = "%Y-%m-%d %H:%M:%S"



@ml_router.get('/get_prediction')
async def get_prediction(
    request:Request,
    claster_number: int, 
    trip_date_time: datetime,
    session=Depends(get_session)
    ):
    token=request.cookies.get(settings.COOKIE_NAME)
    user_email = await authenticate_cookie(token)
    if token:
        if user_email:
            user = UserService.get_user_by_email(user_email,session)
            if(user):
                try:
                    data = {
                        'claster': [claster_number],
                        'trip_date_time': [trip_date_time]
                    }

                    new_request = MLRequest(id=uuid.uuid4(), claster=claster_number, pickup_date_time=trip_date_time, user_id=user.id)
                    create_request(new_request=new_request, session=session)
                    rabbitmq = RabbitMQ()
                    message = json.dumps(
                        {
                            "request_id": str(new_request.id), 
                        }
                    )
                    rabbitmq.send_task(message=message)
                    return templates.TemplateResponse("personal_cabinet.html", {"request": request})


                    return {"predicted_quality": int(prediction[0])}
                    
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))





