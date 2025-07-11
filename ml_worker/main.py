from services.crud.user import get_user_by_id
from services.crud.request import get_request_by_id
from services.crud.response import create_response
from services.crud.balance import decrease_user_balance
import json
from mlrunner import MlRunner
from fastapi import Depends
from services.rm.rabbitmq import RabbitMQ
from sqlmodel import SQLModel, Session, create_engine
from database.config import get_settings


ml_runner = MlRunner()
rabbitmq = RabbitMQ()
engine = create_engine(url=get_settings().DATABASE_URL_psycopg, echo=True,pool_size=5, max_overflow=10)


def process_message(ch, method, properties, body):

    data_for_request=json.loads(body)
    request_id = data_for_request['request_id']
    
    with Session(engine) as session: 
        new_request = get_request_by_id(id=request_id, session=session)
        response=ml_runner.get_prediction(request=new_request)
        if response:
            create_response(new_response=response,session=session)
            decrease_user_balance(user_id=response.user_id,session=session)


rabbitmq.consume(queue_name="ml_task_queue", callback=process_message)










