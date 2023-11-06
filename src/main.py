import logging
import sys
import json

sys.path.append('/app/src')

from config.mq import channel
from db import get_collection

logging.info("App started!")
queue_name = 'queue.notification.toService'

def callback(channel, method, properties, body):
    try:
        logging.info(f"Received message {body}")
        message_data = json.loads(body.decode('utf-8'))
        logging.info(f"Message data: {message_data}")
        logging.info(f"Challenge Name: {message_data['challengeName']}")
        logging.info(f"Creator Name: {message_data['creatorName']}")

        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error(f"Failed to process message:{e}")

channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=False)

logging.info("Application started!")
channel.start_consuming()