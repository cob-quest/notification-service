import sys

sys.path.append('/app/src/config')

from dotenv import load_dotenv
from os import environ

# Define the path to your .env file
dotenv_path = '/app/secrets/.env'

# Load the environment variables from the specified path
load_dotenv(dotenv_path=dotenv_path)

AMQP_USERNAME = environ.get('AMQP_USERNAME')
AMQP_PASSWORD = environ.get('AMQP_PASSWORD')
AMQP_HOSTNAME = environ.get('AMQP_HOSTNAME')
MONGODB_HOSTNAME = environ.get("MONGODB_HOSTNAME")
MONGODB_USERNAME = environ.get("MONGODB_USERNAME")
MONGODB_PASSWORD = environ.get("MONGODB_PASSWORD")
MONGODB_PORT = 27017
SMTP_API_KEY = environ.get("SMTP_API_KEY")