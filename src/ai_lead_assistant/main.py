import time
from src.ai_lead_assistant.ai_assistant import chat
from src.ai_lead_assistant.lead_classifier import analyze_lead, is_lead_complete
from src.ai_lead_assistant.lead_extractor import extract_lead
from src.ai_lead_assistant.lead_pipline import process_lead
from src.ai_lead_assistant.alerts import send_email_alert


def handel_message(conversation_history, user_message):

    
    ai_response = chat(
        conversation_history,
        user_message
    )

    if ai_response is None:
        return (
            "Sorry, I am having trouble processing your request right now. "
            "Please try again in a few seconds.",
            None,
            None,
            None
        )

    time.sleep(1)

    lead = None
    analysis = None
    lead_id = None

    
    try:
        lead = extract_lead(conversation_history)
        print(f"👉 [DEBUG] Extracted Lead: {lead}")
    except Exception as e:
        print(f"[Warning] Extraction skipped/failed: {e}")
        

    
    if lead:
        try:
            analysis = analyze_lead(lead)
            print(f"👉 [DEBUG] Analysis: {analysis}")
        except Exception as e:
            print(f"[Warning] Analysis skipped/failed: {e}")
            analysis = {"score": 0, "classification": "COLD"}

    
    if lead and is_lead_complete(lead) and analysis:
        try:
            score = analysis.get("score", 0) if isinstance(analysis, dict) else 0
            classification = analysis.get("classification", "Unclassified") if isinstance(analysis, dict) else "Unclassified"
            
            
            lead_id = process_lead(
                lead=lead,
                score=score,
                classification=classification
            )
            print(f"✅ [SUCCESS] Saved to DB & Google Sheets with ID: {lead_id}")

        except Exception as e:
            print(f"[Warning] Processing skipped/failed: {e}")

    return ai_response, lead, analysis, lead_id



