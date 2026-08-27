from src.ai_lead_assistant.models import Lead, PropertyType, FinishingType
from src.ai_lead_assistant.database import create_table, save_lead, update_lead, get_lead_by_id
from src.ai_lead_assistant.sheets import save_lead_to_sheet

# 1. Create table in Database
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

# 3. Save lead to Database (INSERT)
lead_id = save_lead(
    lead=lead,
    score=75,
    classification="warm"
)
print("Created Lead ID in DB:", lead_id)

# 🧪 TEST 1: Save new Lead to Google Sheets
saved_lead = get_lead_by_id(lead_id)
created_at = saved_lead["created_at"] if saved_lead else "N/A"

try:
    save_lead_to_sheet(
        lead=lead,
        score=75,
        classification="warm",
        lead_id=lead_id,
        created_at=created_at
    )
    print("✅ [Test 1 Passed] Lead added to Google Sheets successfully.")
except Exception as e:
    print("❌ [Test 1 Failed] Google Sheets Error:", e)


# 4. Update the same lead in Database
lead.budget = 6000000
lead.bedrooms = 4

updated_id = update_lead(
    lead_id=lead_id,
    lead=lead,
    score=90,
    classification="hot"
)
print("Updated Lead ID in DB:", updated_id)

# 🧪 TEST 2: Update same Lead in Google Sheets
try:
    save_lead_to_sheet(
        lead=lead,
        score=90,
        classification="hot",
        lead_id=updated_id,
        created_at=created_at
    )
    print("✅ [Test 2 Passed] Lead updated in Google Sheets successfully.")
except Exception as e:
    print("❌ [Test 2 Failed] Google Sheets Update Error:", e)


# 5. Read lead from database
final_lead = get_lead_by_id(updated_id)
print("\n--- FINAL SAVED LEAD IN DB ---")
print(final_lead)