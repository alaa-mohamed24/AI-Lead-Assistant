from src.ai_lead_assistant.models import Lead
from src.ai_lead_assistant.database import create_table
from src.ai_lead_assistant.lead_pipline import process_lead

create_table()

lead = Lead(
    name="lucinda",
    phone="01067840666",
    
)


lead_id = process_lead(
    lead= lead,
    score=20,
    classification="cold"
)

print("Lead processed successfully!")
print("Lead ID: ", lead_id)