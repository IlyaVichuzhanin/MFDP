from models.user import User
from models.request import Request
from models.response import Response
from services.crud.balance import get_balance_by_user_id, decrease_user_balance
from services.crud.price import get_current_price
from mlmodel import MLmodel
from services.crud.request import create_request
from services.crud.response import create_response
from typing import Optional
from io import BytesIO
import PIL.Image as Image
import torch
import datetime
from sqlmodel import Session
import io
import uuid

class MlRunner:

    def __init__(self):
        self.__mlmodel =MLmodel()

    @property
    def mlmodel(self):
        return self.__mlmodel
    
    def get_prediction(self, request:Request)->Optional[Response]:
        
        request_image = Image.open(request.image).convert('RGB')
        inputs = self.__mlmodel.image_processor(request_image, return_tensors="pt")
        outputs = self.__mlmodel.model.generate(**inputs)
        image_description=self.__mlmodel.image_processor.decode(outputs[0], skip_special_tokens=True)
        response = Response(
            id=uuid.uuid4(),
            response=image_description,
            date_time=datetime.datetime.now(),
            user_id=request.user.id,
            user=request.user,
            request_id=request.id,
            request=request
            )

        return response


    





    