import logging
import sys
import json
import time

import pika

sys.path.append('/app/src')

from config.mq import create_channel, init
from db import get_collection
from services.queue import process_participants

# Configure root logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

QUEUE_NAME = 'queue.notification.toService'
EXCHANGE_NAME = 'topic.router'
ROUTING_KEY = 'notification.fromService.emailSent'

def callback(channel, method, properties, body):
    try:
        logging.info(f"Received message {body}")
        message_data = json.loads(body.decode('utf-8'))
        logging.info(f"Message data: {message_data}")
        response = process_participants(message_data)

        # Before acknowledging the received message, publish it to another exchange
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=ROUTING_KEY,
            body=json.dumps(response),
        )
        logging.info("Message published to topic.router")

        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error(f"Failed to process message:{e}")

def consume():

    channel = create_channel()

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=False)

    logging.info("Application started!")
    channel.start_consuming()

init()

while True:
    try:
        consume()
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Connection was closed, retrying...: {e}")
        time.sleep(5)  # Wait for 5 seconds before the next attempt
