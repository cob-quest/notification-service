import sys
import logging


sys.path.append("/app/src/services")

from config.db import get_collection
from collection.attempt import get_attempt_by_challenge_and_creator_and_participant
from services.email import send_email

def process_participants(message_data: object):
    participants = message_data["participants"]
    challenge_name = message_data["challengeName"]
    creator_name = message_data["creatorName"]
    response = message_data.copy()
    response["event"] = "emailSend"

    collection = get_collection()
    for email in participants:
        logging.info(email)
        attempt = get_attempt_by_challenge_and_creator_and_participant(collection, challenge_name, creator_name, email)
        logging.info(f"Attempt: {attempt}")
        try:
            send_email(attempt)
        except Exception as e:
            response["eventStatus"] = "emailSendFailed"
            return response
        
    response["eventStatus"] = "emailSent"
    return response



