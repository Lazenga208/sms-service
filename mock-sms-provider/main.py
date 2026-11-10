from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI(
    title="Mock SMS Provider",
    description="A simulated SMS provider",
    version="1.0.0",
)


# Temporary in-memory storage for simulated messages
messages = {}


class SmsRequest(BaseModel):
    to: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)


class SmsResponse(BaseModel):
    id: str
    status: str


@app.post(
    "/messages",
    response_model=SmsResponse,
    status_code=status.HTTP_201_CREATED,
)
def send_sms(request: SmsRequest):
    message_id = str(uuid4())

    messages[message_id] = {
        "id": message_id,
        "to": request.to,
        "body": request.body,
        "status": "SENT",
    }

    return SmsResponse(
        id=message_id,
        status="SENT",
    )


@app.get("/messages/{message_id}")
def get_sms_status(message_id: str):
    message = messages.get(message_id)

    if message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found",
        )

    return {
        "id": message["id"],
        "status": message["status"],
    }
