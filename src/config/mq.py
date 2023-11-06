import pika
import time
import logging
import sys

sys.path.append("/app/src/config")

from env import AMQP_HOSTNAME, AMQP_USERNAME, AMQP_PASSWORD

# Configure root logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info(
    f"Connecting to RabbitMQ at {AMQP_HOSTNAME}:5672 with user {AMQP_USERNAME} and password {AMQP_PASSWORD}..."
)

credentials = pika.PlainCredentials(username=AMQP_USERNAME, password=AMQP_PASSWORD)
parameters = pika.ConnectionParameters(
    host=AMQP_HOSTNAME, port=5672, credentials=credentials
)
connected = False
start_time = time.time()

logging.info("Connecting...")

while not connected:
    try:
        connection = pika.BlockingConnection(parameters)
        connected = True
    except pika.exceptions.AMQPConnectionError:
        if time.time() - start_time > 20:
            exit(1)

logging.info("CONNECTED!")

# Create an AMQP topic exchange for Notifications

channel = connection.channel()
exchange_name = "topic.notification"
exchange_type = "topic"
channel.exchange_declare(
    exchange=exchange_name, exchange_type=exchange_type, durable=True
)

# Create a queue for Notifications

queue_name = "queue.notification.toService"
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(
    exchange=exchange_name, queue=queue_name, routing_key="notification.toService.*"
)
