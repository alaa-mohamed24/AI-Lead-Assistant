import time
from google.genai.errors import ClientError

from src.ai_lead_assistant.ai_assistant import chat
from src.ai_lead_assistant.lead_extractor import extract_lead
from src.ai_lead_assistant.lead_classifier import analyze_lead
from src.ai_lead_assistant.lead_pipline import process_lead


def safe_call(func, *args, **kwargs):
    for attempt in range(3):
        try:
            return func(*args, **kwargs)
        except ClientError as e:
            if "429" in str(e):
                print(f"⚠️ [Rate Limit] Quota hit. Waiting 15s... (Attempt {attempt + 1})")
                time.sleep(15)
            else:
                print(f"❌ [ClientError in {func.__name__}]: {e}")
                break
        except Exception as e:
            print(f"❌ [Error in {func.__name__}]: {e}")
            break
    return None


def handel_message(conversation_history, user_message, existing_lead_id=None):

    # 1. AI Chat Response
    ai_response = safe_call(chat, conversation_history, user_message)

    if not ai_response:
        return (
            "Sorry, I am having trouble processing your request right now. Please try again.",
            None, None, existing_lead_id
        )

    # 2. Extract Lead safely
    time.sleep(2)
    full_history = conversation_history + [{"role": "assistant", "content": ai_response}]
    lead = safe_call(extract_lead, full_history)
    print(f"👉 [DEBUG] Extracted Lead: {lead}")

    # 3. Analyze Lead safely
    analysis = {"score": 0, "classification": "COLD"}
    if lead:
        time.sleep(2)
        extracted_analysis = safe_call(analyze_lead, lead)
        if isinstance(extracted_analysis, dict):
            analysis = extracted_analysis
        print(f"👉 [DEBUG] Analysis: {analysis}")

    # 4. Process Lead (Always attempt DB save if lead object exists)
    lead_id = existing_lead_id
    if lead:
        try:
            score = analysis.get("score", 0)
            classification = analysis.get("classification", "COLD")

            lead_id = process_lead(
                lead=lead,
                score=score,
                classification=classification,
                existing_lead_id=existing_lead_id
            )
            print(f"✅ [SUCCESS] Saved to DB with ID: {lead_id}")

        except Exception as e:
            print(f"❌ [DB Process Error]: {e}")

    return ai_response, lead, analysis, lead_id



