from src.ai_lead_assistant.models import Lead
from src.ai_lead_assistant.lead_classifier import analyze_lead


lead = Lead(
    name="Ahmed",
    phone="01012345678",
    property_type="apartment",
    location="Sheikh Zayed",
    budget=4000000,
    bedrooms=3,
    finishing="finished",
    timeline="within_1_month",
    intent="buy"
    
)


result = analyze_lead(lead)

print("score: ", result["score"])
print("classification: ", result["classification"])