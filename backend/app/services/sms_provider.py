import os

import httpx

PROVIDER_URL = os.getenv(
    "SMS_PROVIDER_URL",
    "http://mock-sms:8001",
)


def send_sms(to: str, body: str) -> dict:
    response = httpx.post(
        f"{PROVIDER_URL}/messages",
        json={"to": to, "body": body},
        timeout=5.0,
    )

    response.raise_for_status()
    return response.json()


def get_sms_status(provider_message_id: str) -> dict:
    response = httpx.get(
        f"{PROVIDER_URL}/messages/{provider_message_id}",
        timeout=5.0,
    )

    response.raise_for_status()
    return response.json()
