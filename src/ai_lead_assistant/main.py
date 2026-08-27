
import time

from src.ai_lead_assistant.ai_assistant import chat
from src.ai_lead_assistant.lead_extractor import extract_lead
from src.ai_lead_assistant.lead_classifier import analyze_lead
from src.ai_lead_assistant.lead_pipline import process_lead


def handel_message(conversation_history, user_message):

    # 1. Get AI response
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

    # 2. Extract lead from conversation history
    lead = None

    try:
        lead = extract_lead(conversation_history)

        print(f"👉 [DEBUG] Extracted Lead: {lead}")

    except Exception as e:
        print(f"[Warning] Extraction skipped/failed: {e}")

    # 3. Analyze lead
    analysis = None

    if lead:

        try:
            analysis = analyze_lead(lead)

            print(f"👉 [DEBUG] Analysis: {analysis}")

        except Exception as e:

            print(f"[Warning] Analysis skipped/failed: {e}")

    # 4. Save / update lead
    lead_id = None

    if lead and analysis:

        try:

            score = analysis.get("score", 0)
            classification = analysis.get(
                "classification",
                "Unclassified"
            )

            lead_id = process_lead(
                lead=lead,
                score=score,
                classification=classification
            )

            print(
                f"✅ [SUCCESS] Lead processed with ID: {lead_id}"
            )

        except Exception as e:

            print(
                f"[Warning] Processing skipped/failed: {e}"
            )

    return ai_response, lead, analysis, lead_id



