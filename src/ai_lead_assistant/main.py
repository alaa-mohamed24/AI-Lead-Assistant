import time
from google.genai.errors import ClientError

from src.ai_lead_assistant.ai_assistant import chat
from src.ai_lead_assistant.lead_extractor import extract_lead
from src.ai_lead_assistant.lead_classifier import analyze_lead
from src.ai_lead_assistant.lead_pipline import process_lead


def safe_call(func, *args, **kwargs):
    """دالة لضمان إعادة المحاولة تلقائياً عند الوصول للـ Rate Limit"""
    for attempt in range(3):
        try:
            return func(*args, **kwargs)
        except ClientError as e:
            if "429" in str(e):
                print(f"⚠️ [Rate Limit] Quota hit. Waiting 15s... (Attempt {attempt + 1})")
                time.sleep(15)  # انتظار الـ 15 ثانية اللي طلبها سيرفر جوجل في الإيرور
            else:
                raise e
        except Exception as e:
            print(f"❌ Error in {func.__name__}: {e}")
            break
    return None


def handel_message(conversation_history, user_message, existing_lead_id=None):

    # 1. Get AI response
    ai_response = safe_call(chat, conversation_history, user_message)

    if ai_response is None:
        return (
            "Sorry, I am receiving too many requests right now. Please wait a few seconds and try again.",
            None,
            None,
            None
        )

    # 2. Extract lead
    time.sleep(2)  # مسافة بين الاستدعاءات
    full_history = conversation_history + [{"role": "assistant", "content": ai_response}]
    lead = safe_call(extract_lead, full_history)
    print(f"👉 [DEBUG] Extracted Lead: {lead}")

    # 3. Analyze lead
    analysis = None
    if lead:
        time.sleep(2)
        analysis = safe_call(analyze_lead, lead)
        print(f"👉 [DEBUG] Analysis: {analysis}")

    if not analysis:
        analysis = {"score": 0, "classification": "COLD"}

    # 4. Process Lead (Save to SQLite & Sheets)
    lead_id = existing_lead_id
    if lead:
        try:
            score = analysis.get("score", 0) if isinstance(analysis, dict) else 0
            classification = analysis.get("classification", "Unclassified") if isinstance(analysis, dict) else "Unclassified"

            lead_id = process_lead(
                lead=lead,
                score=score,
                classification=classification,
                existing_lead_id=existing_lead_id
            )
            print(f"✅ [SUCCESS] Lead processed with ID: {lead_id}")

        except Exception as e:
            print(f"[Warning] Processing skipped/failed: {e}")

    return ai_response, lead, analysis, lead_id



