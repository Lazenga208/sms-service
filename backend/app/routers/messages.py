import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.message import Message
from app.schemas.message import (
    MessageCreate,
    MessageResponse,
    MessageStatus,
)
from app.services.sms_provider import get_sms_status, send_sms

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
):
    message = Message(
        to_phone=message_data.to,
        body=message_data.body,
        status=MessageStatus.PENDING.value,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    try:
        provider_response = send_sms(
            message.to_phone,
            message.body,
        )

        message.provider_message_id = provider_response["id"]
        message.status = MessageStatus(provider_response["status"]).value

    except (httpx.HTTPError, KeyError, ValueError):
        message.status = MessageStatus.FAILED.value

    db.commit()
    db.refresh(message)

    return message


@router.get("/{message_id}", response_model=MessageResponse)
def get_message(
    message_id: str,
    db: Session = Depends(get_db),
):
    message = db.query(Message).filter(Message.id == message_id).first()

    if message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found",
        )

    if message.provider_message_id:
        try:
            provider_response = get_sms_status(message.provider_message_id)

            message.status = MessageStatus(provider_response["status"]).value

            db.commit()
            db.refresh(message)

        except (httpx.HTTPError, KeyError, ValueError):
            pass

    return message


@router.get("", response_model=list[MessageResponse])
def list_messages(
    message_status: MessageStatus | None = Query(
        default=None,
        alias="status",
    ),
    db: Session = Depends(get_db),
):
    query = db.query(Message)

    if message_status is not None:
        query = query.filter(Message.status == message_status.value)

    return query.order_by(Message.created_at.desc()).all()
