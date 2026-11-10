import re
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class MessageStatus(str, Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"


class MessageCreate(BaseModel):
    to: str = Field(..., description="Recipient phone number")
    body: str = Field(..., min_length=1, max_length=160)

    @field_validator("to")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        value = value.strip()

        if not re.fullmatch(r"\+[1-9]\d{7,14}", value):
            raise ValueError("Phone number must be in international E.164 format")

        return value

    @field_validator("body")
    @classmethod
    def validate_body(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Message body cannot be empty")

        return value


class MessageResponse(BaseModel):
    id: str
    provider_message_id: str | None = None
    to_phone: str
    body: str
    status: MessageStatus
    created_at: datetime

    model_config = {"from_attributes": True}
