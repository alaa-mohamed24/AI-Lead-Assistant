from src.ai_lead_assistant.sheets import save_lead_to_sheet, setup_worksheet
from src.ai_lead_assistant.models import Lead

# lead = Lead(
#     name="Ahmed",
#     phone="01012345678",
#     property_type="apartment",
#     location="Sheikh Zayed",
#     budget=4000000,
#     bedrooms=3,
#     finishing="finished",
#     timeline="within_1_month",
#     intent="buy"
# )


# result = save_lead_to_sheet(

# lead= lead,
# score=100,
# classification= "hot",
# lead_id=1,
# created_at="2026-08-21 00:30:00"
# )

# print("Lead added to google sheets: ", result)

result= setup_worksheet()
print("worksheet setup:" ,result)