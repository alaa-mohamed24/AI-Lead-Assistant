from src.ai_lead_assistant.ai_assistant import chat

from src.ai_lead_assistant.lead_extractor import extract_lead

from src.ai_lead_assistant.lead_classifier import analyze_lead, is_lead_complelt

from src.ai_lead_assistant.lead_pipline import process_lead

def handel_message(conversation_history, user_message):
    ai_response = chat(
        conversation_history,
        user_message
    )

    print("\n--- HISTORY AFTER CHAT ---")
    print(conversation_history)
    print("--------------------------\n")


    lead= extract_lead(conversation_history)

    if is_lead_complelt(lead):


        analysis = analyze_lead(lead)


        lead_id= process_lead(
            lead=lead,
            score=analysis["score"],
            classification=analysis["classification"]
        )

    else:

        analysis = None
        lead_id = None


    return ai_response, lead, analysis, lead_id



