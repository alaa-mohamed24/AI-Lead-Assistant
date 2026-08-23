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


    prompt = prompt = f"""
Extract the real estate lead information from the entire customer conversation below.

Customer conversation:
{conversation_text}

Important instructions:

1. Analyze the entire conversation, not only the last message.
2. Combine information provided by the customer across different messages.
3. If the customer mentioned a piece of information earlier in the conversation,
    keep it in the final Lead.
4. Do not remove previously provided information just because it is not mentioned
    in the latest message.
5. Only extract information that the customer actually provided.
6. Do not invent or assume any information.
7. If a piece of information was never provided, leave it empty.

Return the extracted information according to the Lead model.
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
                model="gemini-1.5-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": Lead
                }
            )
        else:
            raise e

    return Lead.model_validate_json(response.text)