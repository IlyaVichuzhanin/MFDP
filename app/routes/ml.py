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



@ml_router.get('/get_prediction')
def get_prediction(
    claster_number: int, 
    trip_date_time: datetime):

    try:
        data = {
            'claster number': [claster_number],
            'trip date time': [trip_date_time]
        }

        df = pd.DataFrame(data)
        model_path = 'shared_data/xgboost_model.pkl.pkl'
        
        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail="Model file not found")

        with open(model_path, 'rb') as file:
            model = joblib.load(file)

        prediction = model.predict(df)
        return {"predicted_quality": int(prediction[0])}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





