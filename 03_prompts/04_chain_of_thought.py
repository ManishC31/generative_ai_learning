"""
Chain of thoughts

"""

from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

system_prompt = """
You are an expert AI assistant in resolving user queries using chain of thoughts.
You work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT.

Rules:
 - Strictly follow the given JSON output format
 - Only run one step at a time.
 - The sequence of steps is START (where user gives an input), PLAN (that can be multiple times) and finally OUTPUT (which is going to be displayed to the user).

 Output JSON format:
 {"step": "START" | "PLAN" | "OUTPUT", "content" : "string"}

 Example: 
 START: Hey, can you solve 2 + 3 * 5 / 10
 PLAN: {"step": "PLAN", "content": "Seems like the user is interested in math problem"}
 PLAN: {"step": "PLAN", "content": "looking at the problem, we should solve this using BODMAS method" }
 PLAN: {"step": "PLAN", "content": "Yes, the BODMAS is correct thing to be done here"}
 PLAN: {"step": "PLAN", "content": "First we must multiply 3 * 5 which is 15"}
 PLAN: {"step": "PLAN", "content" : "Now the new equation is 2 + 15 /10"}
 PLAN: {"step": "PLAN", "content" : "We must perform divide that is 15 / 10 = 1.5"}
 PLAN: {"step": "PLAN", "content" : "Now the new equation is 2 + 1.5"}
 PLAN: {"step": "PLAN", "content" : "Now finally lets perform the add 3.5"}
 PLAN: {"step": "PLAN", "content" : "Great, we have solved and finally left with 3.5 as answer"}
 OUTPUT: {"step": "OUTPUT", "content": "Great, we have solved and the answer is 3.5"}
"""


message_history = [
    {"role": "system", "content": system_prompt},
]

user_input = input(">>> ")
message_history.append({"role": "user", "content": user_input})

print("\n\n\n")

while True:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=message_history,
    )
    raw_result = response.choices[0].message.content
    parsed_result = json.loads(raw_result)
    message_history.append({"role": "assistant", "content": raw_result})

    if parsed_result.get("step") == "START":
        print("STEP RESULT -->", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "PLAN":
        print("PLANNED RESULT -->", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("OUTPUT RESULT -->", parsed_result.get("content"))
        break


print("\n\n\n")
