from models.user import User
from models.request import Request
from models.response import Response
from mlmodel import MLmodel
from services.crud.request import create_request
from services.crud.response import create_response
from typing import Optional
from datetime import datetime
import pandas as pd
import uuid

class MlRunner:

    def __init__(self):
        self.__mlmodel = MLmodel()

    @property
    def mlmodel(self):
        return self.__mlmodel

    def get_prediction(self, request: Request) -> Optional[Response]:
        # Парсим дату
        pickup_date_time = datetime.strptime(request.pickup_date_time, "%Y-%m-%d %H:%M:%S")

        # Формируем DataFrame для модели
        new_data = pd.DataFrame({
            'cluster': [request.cluster if request.cluster is not None else -1],
            'month': [pickup_date_time.month],
            'day': [pickup_date_time.day],
            'hour': [pickup_date_time.hour],
            'dayofweek': [pickup_date_time.weekday()],  # правильно: вызываем метод
            'is_weekend': [is_weekend(pickup_date_time)],
            'time_of_day_evening': [is_evening(pickup_date_time)],
            'time_of_day_morning': [is_morning(pickup_date_time)],
            'time_of_day_night': [is_night(pickup_date_time)]
        })

        # Делаем предсказание
        outputs = self.__mlmodel.model.predict(new_data)
        print("Предсказанное значение:", outputs[0])

        # Создаём объект ответа
        response = Response(
            id=uuid.uuid4(),
            demand=outputs[0],
            date_time=datetime.now(),  # исправлено: убраны лишние .datetime
            user_id=request.user.id,
            user=request.user,
            request_id=request.id,
            request=request
        )

        return response


# Проверка на выходной день
def is_weekend(date_time: datetime) -> bool:
    return date_time.weekday() >= 5  # True, если суббота или воскресенье


# Проверка на утро
def is_morning(date_time: datetime) -> bool:
    return 5 <= date_time.hour < 12


# Проверка на вечер
def is_evening(date_time: datetime) -> bool:
    return 17 <= date_time.hour < 22


# Проверка на ночь
def is_night(date_time: datetime) -> bool:
    return date_time.hour < 5 or date_time.hour >= 22