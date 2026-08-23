import time
from src.ai_lead_assistant.ai_assistant import chat
from src.ai_lead_assistant.lead_classifier import analyze_lead, is_lead_complelt
from src.ai_lead_assistant.lead_extractor import extract_lead
from src.ai_lead_assistant.lead_pipline import process_lead


def handel_message(conversation_history, user_message):
    ai_response = chat(conversation_history, user_message)

    time.sleep(2)

    lead = None
    analysis = None
    lead_id = None

    try:
        lead = extract_lead(conversation_history)
    except Exception as e:
        print(f"[Warning] Extraction skipped/failed: {e}")

    if lead and is_lead_complelt(lead):
        time.sleep(2)  # مهلة بين الاستخراج والتحليل
        try:
            analysis = analyze_lead(lead)
            lead_id = process_lead(
                lead=lead,
                score=analysis.get("score", 0),
                classification=analysis.get("classification", "Unclassified"),
            )
        except Exception as e:
            print(f"[Warning] Analysis skipped/failed: {e}")

    return ai_response, lead, analysis, lead_id



