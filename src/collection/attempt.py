import logging
import sys

sys.path.append("/app/src/db")

def get_attempt_by_challenge_and_creator_and_participant(collection, challenge_name: str, creator_name: str, participant: str):
    """
    Find all attempts with a given challengeName, creatorName and participant.
    """
    try:
        attempt = collection.find_one({
            "challengeName": challenge_name,
            "creatorName": creator_name,
            "participant": participant
        })
        return attempt
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None