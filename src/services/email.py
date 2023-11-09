import logging
import requests
import sys

sys.path.append('/app/src/services')

from config.env import SMTP_API_KEY

url = "https://api.smtp2go.com/v3/email/send"
headers = {"Content-Type": "application/json"}

# Configure root logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def send_email(attempt: object):
    """
    Send an email to the participant with the details of the challenge.
    """
    challenge_name = attempt["challengeName"]
    creator_name = attempt["creatorName"]
    participant = attempt["participant"]
    token = attempt["token"]

    with open("src/services/template.html", "r") as f:
        html_template = f.read()
    logging.info(html_template)
    html_template = html_template.replace("INSERT_CHALLENGE_HERE", challenge_name)
    html_template = html_template.replace("INSERT_CREATOR_HERE", creator_name)
    html_template = html_template.replace("INSERT_TOKEN_HERE", token)
    logging.info(html_template)
    message = f"Hello, you have been invited to participate in the {challenge_name} challenge by {creator_name}. This is your token: {token}."
    receiver_arr = [f"Participant <{participant}>"]

    data = {}
    data["api_key"] = SMTP_API_KEY
    data["to"] = receiver_arr
    data["sender"] = "Team Cobbers <cobbers@cob.quest>"
    data["subject"] = "Assessment Details"
    data["html_body"] = html_template


    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        logging.info("Email sent successfully!")
        logging.info(response.json())
    else:
        logging.info("Failed to send the email.")
        logging.info(response.text)
        raise Exception("Failed to send the email.")