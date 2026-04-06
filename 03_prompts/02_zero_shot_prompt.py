"""
Zero shot prompting - Instructions given directly to the model without any prior examples.
"""

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

system_prompt = """
You should only and only answer the coding related question.
Do not answer anything else.
Your name is Alexa.
If user asks something else, tell them sorry politely.
"""


response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "can you give me palindrome code in csharp"},
    ],
)


print(response.choices[0].message.content)
