import time
import logging
import sys

sys.path.append('/app/src/config')

from pymongo import ASCENDING, DESCENDING, IndexModel, MongoClient, errors
from env import MONGODB_HOSTNAME, MONGODB_USERNAME, MONGODB_PASSWORD, MONGODB_PORT

MONGOURI = f'mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOSTNAME}:{MONGODB_PORT}'

# Configure root logger
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info(MONGOURI)
client = MongoClient(MONGOURI)

def get_collection():
    """Get database connection

    Returns:
        Collection: A MongoClient collection
    """
    retry_timer = 2

    while True:
        try:
            logging.info("Connecting to MongoDB...")
            db = client.get_database("cob")
            attempt_collection = db['attempt']

            attempt_collection.create_index([("token", ASCENDING)], unique=True)
            attempt_collection.create_index(
                [("challengeName", ASCENDING),
                ("creatorName", ASCENDING),
                ("participant", ASCENDING)],
                unique=True
            )

            logging.info("Connected to MongoDB SUCCESS!")
            return attempt_collection

        except errors.ServerSelectionTimeoutError:
            logging.info(f"Failed to connect to MongoDB... Retrying in {retry_timer} seconds")
            time.sleep(retry_timer)
            retry_timer += 2