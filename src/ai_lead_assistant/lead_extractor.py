# data_extraction_officer

import time
from google import genai
from google.genai.errors import ClientError
from src.ai_lead_assistant.config import GOOGLE_API_KEY
from src.ai_lead_assistant.models import Lead

client = genai.Client(api_key=GOOGLE_API_KEY)

def extract_lead(conversation_history):

    conversation_text = ""

    for message in conversation_history:
        role = message["role"]
        text = message["parts"][0]["text"]

        conversation_text += f"{role}: {text}\n"


    prompt = f"""
Extract the real estate lead information from the following customer message.
customer conversation :
{conversation_text}

return the extracted information according to the Lead model.
if a piece of information is not mentioned, leave it empty.
do not invet any information.
"""

    # انتظار بسيط لحماية الـ Quota بين الطلبات المتتالية
    time.sleep(2)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": Lead
            }
        )
    except ClientError as e:
        if e.code == 429:
            print("\n[Notice] Rate limit hit in extract_lead, waiting 15 seconds before retry...")
            time.sleep(15)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": Lead
                }
            )
        else:
            raise e

    return Lead.model_validate_json(response.text)
