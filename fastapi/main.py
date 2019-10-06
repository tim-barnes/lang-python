from fastapi import FastAPI
from pydantic import BaseModel, Schema
from starlette.responses import JSONResponse

class Message(BaseModel):
    message: str = Schema(None, title="the message", description="A message from the server")


app = FastAPI()
count = 0


@app.get("/", response_model=Message, responses={
    404: {"model": Message, "description": "A less cheery message"}
})
def root() -> Message:
    """
    Cheery welcome message
    """
    global count
    if count % 2:
        m = Message(message="Hello world")
    else:
        m = JSONResponse(status_code=404, content=Message(message="Goodbye cruel world!").dict())
    count = count + 1
    return m
