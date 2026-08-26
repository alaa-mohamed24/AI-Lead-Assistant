import time
from src.ai_lead_assistant.ai_assistant import chat
from src.ai_lead_assistant.lead_classifier import analyze_lead, is_lead_complelt
from src.ai_lead_assistant.lead_extractor import extract_lead
from src.ai_lead_assistant.lead_pipline import process_lead


def handel_message(conversation_history, user_message):

    # 1. Get AI response
    ai_response = chat(
        conversation_history,
        user_message
    )

    # If Gemini failed, stop here
    if ai_response is None:
        return (
            "Sorry, I am having trouble processing your request right now. "
            "Please try again in a few seconds.",
            None,
            None,
            None
        )

    # Small delay to avoid sending requests too quickly
    time.sleep(2)

    # Default values
    lead = None
    analysis = None
    lead_id = None

    # 2. Extract lead
    try:
        lead = extract_lead(conversation_history)

    except Exception as e:
        print(f"[Warning] Extraction skipped/failed: {e}")
        return ai_response, None, None, None

    # 3. Check if lead is complete
    if lead and is_lead_complelt(lead):

        time.sleep(2)

        # 4. Analyze lead
        try:
            analysis = analyze_lead(lead)

        except Exception as e:
            print(f"[Warning] Analysis skipped/failed: {e}")
            return ai_response, lead, None, None

        # 5. Process lead
        try:
            lead_id = process_lead(
                lead=lead,
                score=analysis.get("score", 0),
                classification=analysis.get(
                    "classification",
                    "Unclassified"
                )
            )

        except Exception as e:
            print(f"[Warning] Processing skipped/failed: {e}")

    # 6. Return everything
    return ai_response, lead, analysis, lead_id



