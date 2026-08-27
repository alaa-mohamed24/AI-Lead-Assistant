from src.ai_lead_assistant.models import Lead
from src.ai_lead_assistant.database import save_lead, get_lead_by_id
from src.ai_lead_assistant.sheets import save_lead_to_sheet
from src.ai_lead_assistant.alerts import send_email_alert


from src.ai_lead_assistant.models import Lead
from src.ai_lead_assistant.database import save_or_update_lead, get_lead_by_id
from src.ai_lead_assistant.sheets import save_lead_to_sheet
from src.ai_lead_assistant.alerts import send_email_alert
from src.ai_lead_assistant.lead_classifier import is_lead_complete

def process_lead(
        lead: Lead,
        score: int,
        classification: str
):
    
    complete = is_lead_complete(lead)
    status = "COMPLETED" if complete else "IN_PROGRESS"

    
    lead_id = save_or_update_lead(
        lead=lead,
        score=score,
        classification=classification,
        status=status
    )

    
    saved_lead = get_lead_by_id(lead_id)
    created_at = saved_lead["created_at"] if saved_lead else "N/A"

    if complete:
        try:
            save_lead_to_sheet(
                lead=lead,
                score=score,
                classification=classification,
                lead_id=lead_id,
                created_at=created_at
            )
            print(f"📊 [Google Sheets] Exported completed lead ID: {lead_id}")
        except Exception as e:
            print(f"❌ [Google Sheets Error]: {e}")

        
        if str(classification).lower() == "hot":
            try:
                send_email_alert(
                    lead=lead,
                    score=score,
                    classification=classification
                )
                print(f"📧 [Email Alert] Sent hot lead alert for ID: {lead_id}")
            except Exception as alert_err:
                print(f"❌ [Email Alert Error]: {alert_err}")

    return lead_id