from src.ai_lead_assistant.alerts import send_lead_alert
from src.ai_lead_assistant.lead_classifier import analyze_lead
from src.ai_lead_assistant.models import Lead

# # result = test_telegram_connection()
# result = get_chat_id()
# print(result)


# result = send_telegram_message(
#     "🚀 Hello from AI Lead Assistant!"
# )

# print(result)

lead = Lead(
    name="Ahmed",
    phone="01012345678",
    property_type="apartment",
    location="Sheikh Zayed",
    # budget=4000000,
    # bedrooms=3,
    # finishing="finished",
    timeline="within_1_month",
    intent="buy"

)

result= analyze_lead(lead)

score = result["score"]
classification = result["classification"]

print("score: ", score)
print("classification: ", classification)

telegram_result = send_lead_alert(
    lead,
    score,
    classification
)

print("Telegram Result: ", telegram_result)