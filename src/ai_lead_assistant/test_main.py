from src.ai_lead_assistant.models import Lead, PropertyType, FinishingType
from src.ai_lead_assistant.database import create_table, save_lead, update_lead, get_lead_by_id


# 1. Create table
create_table()


# 2. Create first lead
lead = Lead(
    name="Ahmed",
    phone="01012345678",
    property_type=PropertyType.APARTMENT,
    location="Sheikh Zayed",
    budget=4000000,
    bedrooms=3,
    finishing=FinishingType.FINISHED,
    timeline="immediate",
    intent="buy"
)


# 3. Save lead for the first time
lead_id = save_lead(
    lead=lead,
    score=75,
    classification="warm"
)

print("Created Lead ID:", lead_id)


# 4. Update the same lead
lead.budget = 6000000
lead.bedrooms = 4

updated_id = update_lead(
    lead_id=lead_id,
    lead=lead,
    score=90,
    classification="hot"
)

print("Updated Lead ID:", updated_id)


# 5. Read lead from database
saved_lead = get_lead_by_id(updated_id)

print("\n--- SAVED LEAD ---")
print(saved_lead)