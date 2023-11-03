import logging
from config.mq import channel

logging.info("App started!")
queue_name = 'queue.notification.toService'

def callback(channel, method, properties, body):
    try:
        logging.info(f"Received message {body}")
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error(f"Failed to process message:{e}")

channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=False)

logging.info("Application started!")
channel.start_consuming()