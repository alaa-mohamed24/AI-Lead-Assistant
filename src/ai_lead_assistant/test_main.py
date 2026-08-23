from src.ai_lead_assistant.main import handel_message

conversation_history =[]


messages=  [
    "I want an apartment in Sheikh Zayed.",
    "My budget is 4 million.",
    
]
for message in messages: 
    ai_response, lead, analysis, lead_id = handel_message(
            conversation_history,
            message
        )

    print("\nUser:")
    print(message)

    print("\nAI:")
    print(ai_response)

    print("\nLead:")
    print(lead)

    print("\nAnalysis:")
    print(analysis)