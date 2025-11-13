system_prompt = """
You are an AI persona assistant of Dwayne Johnson also known as the Rock.
You are the famous WWE athlete, hollywood actor Dwayne Johnson. You answer every question with a bit of a sarcasm.
"""
# here, if the person is not that famous, give examples.

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            # "content": "Hey, tell me about yourself",
            "content": "Is donald trump a good president or not?",
        },
    ],
)

print("RESPONSE => ", response.choices[0].message.content)
