from fastapi import FastAPI, Depends
from pydantic import BaseModel

import assistant
import auth

app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}


class Question(BaseModel):
    question: str

@app.post("/assistant", dependencies=[Depends(auth.verify_api_key)])
def ask_assistant(question: Question):
    return assistant.ask(question.question)