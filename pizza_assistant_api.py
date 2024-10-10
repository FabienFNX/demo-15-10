from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pizza_assistant import PizzaAssistant

class Message(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    conversation: List[Message]

app = FastAPI()

@app.post("/call")
def call_pizza_assistant(conversation: Conversation):
    try:
        assistant = PizzaAssistant(model="gpt-4o-mini")
        conversation_list = [message.model_dump() for message in conversation.conversation]
        response = assistant.call(conversation_list)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

# Example usage:
# POST request to /call with JSON body:
# {
#     "conversation": [
#         {"role": "user", "content": "What is on the menu?"}
#     ]
# }
