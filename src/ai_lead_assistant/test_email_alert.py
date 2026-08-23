from src.ai_lead_assistant.models import Lead
from src.ai_lead_assistant.alerts import send_email_alert

lead = Lead(
    name="Ahmed",
    phone="01119202829",
    property_type="apartment",
    location="Sheikh Zayed",
    budget=4000000,
    bedrooms=3,
    finishing="finished",
    timeline="immediate",
    intent="buy"
)


result = send_email_alert(
    lead=lead,
    score=95,
    classification="hot"
)

print("Email alert sent:", result)