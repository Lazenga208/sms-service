import uuid
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, String, Text

from app.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    provider_message_id = Column(
        String,
        nullable=True,
    )

    to_phone = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    status = Column(String, nullable=False, default="PENDING")

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
