from src.ai_lead_assistant.lead_extractor import extract_lead

# message = """
# i want a 3 bedroom apartment in sheikh zayed.
# my budget is 4 million.
# i want to buy within month
# i prefer a finished apartment
# """


# lead =extract_lead(message)
# print(lead)

# print("\nProperty Type:", lead.property_type)
# print("Location:", lead.location)
# print("Budget:", lead.budget)
# print("Bedrooms:", lead.bedrooms)
# print("Finishing:", lead.finishing)
# print("Timeline:", lead.timeline)
# print("Intent:", lead.intent)

# error test


message = """
I want a villa in New Cairo.
My budget is around 8 million
"""


lead =extract_lead(message)
print(lead)

print("\nProperty Type:", lead.property_type)
print("Location:", lead.location)
print("Budget:", lead.budget)
print("Bedrooms:", lead.bedrooms)
print("Finishing:", lead.finishing)
print("Timeline:", lead.timeline)
print("Intent:", lead.intent)