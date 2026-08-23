from google import genai
from src.ai_lead_assistant.ai_assistant import chat



# response = ask_gemini("i waant an apartment in sheikh zayed.")

# print(response)

# conversation= [
#     {

#         "role": "user",
#         "parts":[{"text":"i went an apartment in sheikh zayed" }]
#     },
#     {
#         "role": "model",
#         "parts":[{"text":"geart! what is your budget"}]
#     },
#     {
#         "role": "user",
#         "parts": [{"text": "my budget is 5 million"}]
#     }
# ]

# response = ask_gemini(conversation)
# print("AI", response)

conversation_history =[]

while True:
    user_message = input("you: ")
    if user_message.lower()== "exit":
        break

    response = chat(
        conversation_history,
        user_message
    )

    print("AI: ", response)