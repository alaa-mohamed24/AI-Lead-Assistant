from src.ai_lead_assistant.database import save_lead, create_table, get_leads
from src.ai_lead_assistant.models import Lead


create_table()
# print("leads table created successfully!")

# connection = get_connection()
# cursor= connection.cursor()

# cursor.execute("""
#     SELECT name
#     FROM sqlite_master
#     WHERE type ='table'
# """
# )

# tables = cursor.fetchall()
# print("tables: ", tables)

# connection.close()

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


lead_id= save_lead(
    lead,
    score=100,
    classification="hot"
)

print("Lead saved successfully!")
print("Lead ID:", lead_id)


