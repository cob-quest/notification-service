import pika
import time
import logging
from os import environ
from dotenv import load_dotenv, find_dotenv

# Configure root logger
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load .env from parent directory
load_dotenv(find_dotenv(filename='.env', raise_error_if_not_found=True, usecwd=True))

user = environ.get('rabbitmq_user')
password = environ.get('rabbitmq_password')
hostname = environ.get('rabbitmq_host')
port = environ.get('rabbitmq_port')

logging.info("Env variables =" + hostname + " " + port)

credentials = pika.PlainCredentials(username=user,
                      password=password)
parameters = pika.ConnectionParameters(host=hostname,
                                       port=port,
                                       credentials=credentials)
connected = False
start_time = time.time()

logging.info('Connecting...')

while not connected:
    try:
        connection = pika.BlockingConnection(parameters)
        connected = True
    except pika.exceptions.AMQPConnectionError:
        if time.time() - start_time > 20:
            exit(1)

logging.info('CONNECTED!')

# Create an AMQP topic exchange for Notifications

channel = connection.channel()
exchange_name = "topic.notification"
exchange_type = "topic"
channel.exchange_declare(exchange=exchange_name,
                         exchange_type=exchange_type, durable=True)

# Create a queue for Notifications

queue_name = 'queue.notification.toService'
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchange_name,
                   queue=queue_name, routing_key='notification.toService.*')