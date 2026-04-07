from fastapi import FastAPI, Body
from ollama import Client

app = FastAPI()
client = Client(host="http://localhost:11434")


@app.get("/")
def index():
    return "Application is working"


@app.post("/chat")
async def chat_answer(message: str = Body(..., description="the message")):
    response = client.chat(
        model="gemma3:270m", messages=[{"role": "user", "content": message}]
    )

    return {"response": response.message.content}
