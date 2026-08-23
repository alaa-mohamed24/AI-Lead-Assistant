from google import genai
from src.ai_lead_assistant.config import GOOGLE_API_KEY

client = genai.Client(api_key=GOOGLE_API_KEY)


SYSTEM_INSTRUCTION ="""
you are an AI estate lead assistant .
your main responsibities are :
1. understand the customer's real estate needs.
2. have a natural and feiendly conversation.
3. collect important lead information.
4. ask follow-up questions when important information is missing.
5. never invent information that cusromer did not provide.
6. keep the conversation focused on the custimer's real estate needs.
"""
# |------------------|
# bullidng model

def ask_gemini(conversation_history):
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=conversation_history,
        config={
            "system_instruction": SYSTEM_INSTRUCTION
        }
    )

    return response.text

# |----------------|
# add history

def chat(conversation_history,user_message):
    conversation_history.append(
        {
            "role":"user",
            "parts":[{"text":user_message}]
        }
    )
    ai_response= ask_gemini(conversation_history)
    conversation_history.append(
        {
            "role":"model",
            "parts":[{"text":ai_response}]
        }
    )
    return ai_response