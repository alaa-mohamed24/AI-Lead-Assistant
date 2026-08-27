# responsible fpr alerts

import requests
from src.ai_lead_assistant.config import TELEGRAM_BOT_TOKEN

import os
import base64

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from email.mime.text import MIMEText
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]

def get_gmail_credentials():

    creds = None

    if os.path.exists("token.json"):
        from google.oauth2.credentials import Credentials

        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:

            from google.auth.transport.requests import Request

            creds.refresh(Request())

        else :
            flow= InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def send_test_email():
    credentials = get_gmail_credentials()

    service = build(
        "gmail",
        "v1",
        credentials=credentials
    )

    message = MIMEText(
        "Hello from AI Lead Assistant!🚀"
    )

    message["to"]= "wensh0342@gmail.com"
    message["subject"]= "AI Lead Assistant Test"

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    body = {
        "raw": encoded_message
    }

    service.users().messages().send(
        userId= "me",
        body=body
    ).execute()

    return True



def send_email_alert(
        lead,
        score,
        classification
):

    creds = get_gmail_credentials()

    service =build(
        "gmail",
        "v1",
        credentials=creds
    )


    property_val = lead.property_type.value if hasattr(lead.property_type, 'value') else lead.property_type
    finishing_val = lead.finishing.value if hasattr(lead.finishing, 'value') else lead.finishing

    body = f"""
    🔥 HOT LEAD ALERT 

    Name: {lead.name}
    Phone: {lead.phone}

    Property Type: {property_val}
    Location: {lead.location}
    Budget: {lead.budget}
    Bedrooms: {lead.bedrooms}
    Finishing: {finishing_val}

    Timeline: {lead.timeline}
    Intent: {lead.intent}

    Score: {score}
    Classification: {classification.upper()}
    """

    message = MIMEText(body)

    message["to"]= "lily.m.soby24@gmail.com, wensh0342@gmail.com"
    message["subject"]=(
        f"🔥 HOT LEAD - {lead.name}"
    )

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    body ={
        "raw":encoded_message
        }

    service.users().messages().send(
        userId="me",
        body=body
    ).execute()
    return True





# TELEGRAM_CHAT_ID = "1429144331"


# def test_telegram_connection():
#     url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"

#     response= requests.get(url)
#     return response.json()


# def get_chat_id():
#     url= f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"

#     response = requests.get(url)

#     return response.json()


# def send_telegram_message(message):
#     url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

#     data = {
#         "chat_id": TELEGRAM_CHAT_ID,
#         "text": message

#     }

#     response = requests.post(url, data=data)

#     return response.json()


# def create_lead_alert(lead, score, classification):
#     message = f"""
# 🔥 HOT LEAD ALERT 

# Name: {lead.name or "Not provided"}
# Phone: {lead.phone or "Not provided"}
# Property: {lead.property_type.value }
# Location:{lead.location or "Not provided"}
# Budget: {lead.budget or "Not provided"}
# Bedrooms: {lead.bedrooms or "Not provided"}
# Finishing: {lead.finishing or "Not provided"}
# Timeline: {lead.timeline or "Not provided"}
# Intent: {lead.intent or "Not provided"}

# Lead score: {score}
# Status: {classification.upper()}

# """
#     return message 


# def send_lead_alert(lead, score, classification):
#     if classification != "hot":
#         return False

#     message = create_lead_alert(
#         lead,
#         score,
#         classification
#     )

#     result = send_telegram_message(message)
#     return result