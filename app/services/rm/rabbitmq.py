import pika
import os

class RabbitMQ:
    def __init__(self):
        self.user = os.getenv('RABBITMQ_USER', 'rabbitmq')
        self.password = os.getenv('RABBITMQ_PASSWORD', 'strongpassword')
        self.host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
        self.port = int(os.getenv('RABBITMQ_PORT', 5672))
        self.connection = None
        self.channel = None
        self.heartbeat=30
        self.blocked_connection_timeout=2
        self.__connect()

    def __connect(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials, heartbeat=self.heartbeat, blocked_connection_timeout=self.blocked_connection_timeout)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def __close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()

    def consume(self, queue_name, callback):
        if not self.channel:
            raise Exception("Connection is not established.")
    
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def __publish(self, queue_name, message):
        if not self.channel:
            raise Exception("Connection is not established.")
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_publish(exchange='',
                                   routing_key=queue_name,
                                   body=message,
                                   properties=pika.BasicProperties(
                                       delivery_mode=2,  # make message persistent
                                   ))
        print(f"Sent message to queue {queue_name}: {message}")

    def send_task(self, message:dict):
        queue_name = 'ml_task_queue'

        self.__publish(queue_name=queue_name, message=message)
        self.__close()






































# import pika
# from fastapi import APIRouter, Body, HTTPException, status, Depends
# from database.database import get_session
# from models.request import Request, CreateRequest
# from sqlmodel import Session

# connection_params=pika.ConnectionParameters(
#     host='rabbitmq',
#     port=5672,
#     virtual_host='/',
#     credentials=pika.PlainCredentials(
#         username='rabbitmq',
#         password='strongpassword'
#     ),
#     heartbeat=30,
#     blocked_connection_timeout=2
# )

# def send_task(message:str|bytes):
    
#     connection=pika.BlockingConnection(connection_params)
#     channel=connection.channel()

#     queue_name='ml_task_queue'

#     channel.queue_declare(queue=queue_name)

#     channel.basic_publish(
#         exchange='',
#         routing_key=queue_name,
#         body=message
#     )

#     connection.close()