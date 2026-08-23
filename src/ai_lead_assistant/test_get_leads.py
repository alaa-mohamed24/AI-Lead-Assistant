from src.ai_lead_assistant.database import get_lead_by_id


# leads = get_leads()


# for lead in leads:
#     print(lead)

lead = get_lead_by_id(1)

print(lead)