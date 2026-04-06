"""
Few shot prompting - (Widely used)
The instructions are given to the model along with some examples.

In few shot prompting, we can bind the output with rules.
Add Rule in prompt.
"""

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

system_prompt = """
You should only and only answer the coding related questions.
Do not answer anything else. 
Your name is Alexa.
If user asks something rather than coding, just say sorry.

Rule:
 - Strictly follow the output in JSON format

Output Format:
{{
    "code" : "string" or None,
    "isCodingQuestion": boolean
}}

Examples:
Q: Can you explain the a + b wh ole square?
A: {{ "code": None, "isCodingQuestion": false }}

Q: Hey,  write a code in python for adding two numbers
A: {{ "code": "def add (a, b):
        return a + b", "isCodingQuestion": true }}
        
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Give me prime number or not code in swift"},
    ],
)


print(response.choices[0].message.content)
