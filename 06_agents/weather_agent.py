from openai import OpenAI
from dotenv import load_dotenv
import requests
import json
from pydantic import BaseModel, Field
from typing import Optional

load_dotenv()


client = OpenAI()


def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city.lower()} is {response.text}"

    return "Something went wrong"


available_tools = {"get_weather": get_weather}


system_prompt = """
You are an expert AI assistant in resolving user queries using chain of thought.
You work in START, PLAN, TOOL and output steps.
You need to first PLAN what needs to be done. The PLAN can be of multiple steps.
Once you think enough PLAN has been done,  finally you can give an OUTPUT.
You can also call a tool if required from the list of available tools.
For every tool call wait for the OBSERVE step which is the output from the called tool.

Rules:
 - Strictly Follow the given JSON output format
 - Only run one step at a time
 - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times), TOOL if required to use and finally OUTPUT (which is going to be displayed to the user).

 Output JSON format:
 {"step": "START" | "PLAN" | "TOOL" | "OBSERVE" | "OUTPUT", "content": "string", "tool": "string", "input": "string", "content" : "string"}

 Available Tools:
 - get_weather: Takes city name as an input string and returns the weather information about the city.

Example 1: 
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

EXAMPLE 2:
 START: Hey, what is the weather of berlin?
 PLAN: {"step": "PLAN", "content": "Seems like the user is interested in getting weather of berlin Germany"}
 PLAN: {"step": "PLAN", "content": "Lets see if we have available tool from the list of avaiable tools" }
 PLAN: {"step": "PLAN", "content": "Great, we have get_weather tool available for this query"}
 PLAN: {"step": "PLAN", "content": "I need to call get_weather tool for berlin as input for city"}
 PLAN: {"step": "TOOL", "tool": "get_weather", "input" : "berlin"}
 PLAN: {"step": "OBSERVE", "tool": "get_weather", "output" : "The temperature of berlin is cloudy with 10 degree celcius"}
 PLAN: {"step": "PLAN", "content" : "Great, I got the weather information of berlin"}
 OUTPUT: {"step": "OUTPUT", "content": "The current weather in berlin is 10 degree celcius with some cloudy sky"}
"""


class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The ID of the step.")
    content: Optional[str] = Field(
        None, description="The optional string content for the step."
    )
    tool: Optional[str] = Field(None, description="The ID of the tool to call.")
    input: Optional[str] = Field(None, description="The input params for the tool")


message_history = [
    {"role": "system", "content": system_prompt},
]

user_input = input(">>> ")
message_history.append({"role": "user", "content": user_input})

print("\n\n")

while True:
    response = client.chat.completions.parse(
        model="gpt-4o-mini",
        response_format=MyOutputFormat,
        messages=message_history,
    )
    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})

    parsed_result = response.choices[0].message.parsed

    if parsed_result.step == "START":
        print("STEP RESULT -->", parsed_result.content)
        continue

    if parsed_result.step == "PLAN":
        print("PLANNED RESULT -->", parsed_result.content)
        continue

    if parsed_result.step == "TOOL":
        print(
            "USED TOOL -->",
            f"{parsed_result.tool} is used with input {parsed_result.input}",
        )

        tool_response = available_tools[parsed_result.tool](parsed_result.input)
        message_history.append(
            {
                "role": "developer",
                "content": json.dumps(
                    {
                        "step": "OBSERVE",
                        "tool": parsed_result.tool,
                        "input": parsed_result.input,
                        "output": tool_response,
                    }
                ),
            }
        )
        continue

    if parsed_result.step == "OBSERVE":
        print(
            "OBSERVATION -->",
            f"{parsed_result.tool} gave observation as {parsed_result.output}",
        )
        continue

    if parsed_result.step == "OUTPUT":
        print("OUTPUT RESULT -->", parsed_result.content)
        break


print("\n\n")
