# run this to make code work: pip install google-generativeai

import google.generativeai as genai


genai.configure(api_key="AIzaSyC8OjyoyM3UUU9G8gTs3jzSSnfwYjiei6M")

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-pro",  safety_settings=safety_settings)
chat = model.start_chat(history=[])
instruction = "In this chat, respond as if you are talking to a student."

while True:
    question = input("You: ")
    response = chat.send_message(question)
    if question.strip() == "Stop":
        break
    print('\n')
    print(f"Bot: {response.text}")
    print('\n')