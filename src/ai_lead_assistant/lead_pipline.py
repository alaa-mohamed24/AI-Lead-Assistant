from src.ai_lead_assistant.models import Lead
from src.ai_lead_assistant.database import save_lead, get_lead_by_id
from src.ai_lead_assistant.sheets import save_lead_to_sheet
from src.ai_lead_assistant.alerts import send_email_alert


def process_lead(
        lead: Lead,
        score: int,
        classification: str
):
    # 1-save lead to database
    lead_id= save_lead(
        lead =lead,
        score=score,
        classification =classification
    )

    #  2- get saved lead data

    saved_lead = get_lead_by_id(lead_id)

    #  3- get created_at from database

    created_at= saved_lead["created_at"]

    #  4- save lead to google sheets

    save_lead_to_sheet(
        lead=lead,
        score=score,
        classification=classification,
        lead_id=lead_id,
        created_at= created_at
    )

    # 5- send email if lead is hot

    if classification.lower()== "hot":
        send_email_alert(
            lead=lead,
            score=score,
            classification=classification
        )
        
    return lead_id