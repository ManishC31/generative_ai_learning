"""
System prompt is when we provide the content with the role system where
we specify what we want the model to do.
"""

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are an expert in Maths and only and only answers maths related questions.",
        },  # this is the system role where we define the behaviour of the model.
        # {"role": "user", "content": "Why the color of the sky is blue"},
        {"role": "user", "content": "What is the value of pi and how its derived"},
    ],
)

print(response.choices[0].message.content)
