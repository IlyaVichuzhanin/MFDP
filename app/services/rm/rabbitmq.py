import pika
import os
import time
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

class RabbitMQ:
    def __init__(self):
        self.user = os.getenv('RABBITMQ_USER', 'admin')
        self.password = os.getenv('RABBITMQ_PASSWORD', 'admin')
        self.host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
        self.port = int(os.getenv('RABBITMQ_PORT', 5672))
        self.retries = 10
        self.retry_delay = 5
        self.connection = None
        self.channel = None

        # Небольшая пауза перед попыткой подключения
        time.sleep(2)

        self.__connect()

    def __connect(self):
        attempt = 0
        while attempt < self.retries:
            try:
                credentials = pika.PlainCredentials(self.user, self.password)
                parameters = pika.ConnectionParameters(
                    host=self.host,
                    port=self.port,
                    credentials=credentials,
                    heartbeat=30,
                    blocked_connection_timeout=2
                )
                self.connection = pika.BlockingConnection(parameters)
                self.channel = self.connection.channel()
                logging.info("✅ Успешно подключились к RabbitMQ")
                return
            except Exception as e:
                logging.error(f"❌ Ошибка подключения к RabbitMQ (попытка {attempt + 1}/{self.retries}): {e}")
                attempt += 1
                time.sleep(self.retry_delay)

        raise ConnectionError("Не удалось подключиться к RabbitMQ после нескольких попыток")

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
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)  # persistent
        )
        print(f"Sent message to queue {queue_name}: {message}")

    def send_task(self, message: dict):
        queue_name = 'ml_task_queue'
        self.__publish(queue_name=queue_name, message=message)
        self.__close()