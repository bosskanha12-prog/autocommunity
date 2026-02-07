import os, openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_poll_post(question, options):
    text = f"🗳️ {question}\n\n"
    for opt in options:
        text += f"{opt}\n"
    text += "\n👇 Comment your choice!"
    return text
