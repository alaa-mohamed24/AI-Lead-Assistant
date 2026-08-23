from src.ai_lead_assistant.models import Lead
from src.ai_lead_assistant.database import create_table, save_lead, get_lead_by_id
from src.ai_lead_assistant.sheets import save_lead_to_sheet

create_table()

lead = Lead(
    name="Mona",
    phone="01234567890",
    property_type="apartment",
    location="New Cairo",
    budget=5000000,
    bedrooms=3,
    finishing="finished",
    timeline="immediate",
    intent="buy"
)
score = 90
classification = "hot"

lead_id = save_lead(
    lead,
    score,
    classification
)

saved_lead= get_lead_by_id(lead_id)

created_at = saved_lead["created_at"]

result = save_lead_to_sheet(
    lead= lead,
    score = score,
    classification = classification,
    lead_id= lead_id,
    created_at= created_at
)

print("lead ID: ", lead_id)
print("created at: ", created_at)
print("saved to Google Sheets: ", result)