from src.ai_lead_assistant.models import Lead

# lead= Lead(
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

# print(lead)

# test error



lead = Lead(
    name="Ahmed",
    phone="01012345678",
    property_type="car",
    location="Sheikh Zayed",
    budget=4000000,
    bedrooms=3,
    finishing="finished",
    timeline="within_1_month",
    intent="buy"
)

print(lead)