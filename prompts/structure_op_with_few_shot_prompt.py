system_prompt = """
You should only answer coding related questions. If the question is not related to coding then say sorry as the response in a polite way.

Rule:
 - Strictly follow the output json format.

Output Format: 
{{
    "code": "String" or None,
    "is_coding_question": boolean
}}

Example:
Q: Can you tell me about yourself?
A: {{
    "code": None,
    "is_coding_question": False
}}

Q: Can you give me function that adds two numbers in js
A: {{
    "code" : "function addTwoNumbers(a, b){
    return a+b;}",
    "is_coding_question: True
}}

"""

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
            "content": "how to write the function that checks if the number is prime or not in js",
            # "content": "Where is taj mahal?",
        },
    ],
)

print("RESPONSE => ", response.choices[0].message.content)
