from fastapi import FastAPI, Request
from pydantic import BaseModel

import assistant

app = FastAPI()

class Question(BaseModel):
    question: str

@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}

@app.post("/assistant")
def ask_assistant(question: Question):
    return assistant.ask(question.question)