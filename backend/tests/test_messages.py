def test_create_message(client, monkeypatch):
    def fake_send_sms(to, body):
        return {
            "id": "provider-123",
            "status": "SENT",
        }

    monkeypatch.setattr(
        "app.routers.messages.send_sms",
        fake_send_sms,
    )

    response = client.post(
        "/messages",
        json={
            "to": "+972548559208",
            "body": "Hello!",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "SENT"
    assert data["provider_message_id"] == "provider-123"
    assert data["to_phone"] == "+972548559208"


def test_get_message(client, monkeypatch):
    monkeypatch.setattr(
        "app.routers.messages.send_sms",
        lambda to, body: {
            "id": "provider-456",
            "status": "SENT",
        },
    )

    create_response = client.post(
        "/messages",
        json={
            "to": "+972548559208",
            "body": "Hello!",
        },
    )

    message_id = create_response.json()["id"]

    monkeypatch.setattr(
        "app.routers.messages.get_sms_status",
        lambda provider_id: {
            "id": provider_id,
            "status": "SENT",
        },
    )

    response = client.get(f"/messages/{message_id}")

    assert response.status_code == 200
    assert response.json()["id"] == message_id


def test_message_not_found(client):
    response = client.get("/messages/unknown-id")

    assert response.status_code == 404


def test_filter_messages_by_status(client, monkeypatch):
    monkeypatch.setattr(
        "app.routers.messages.send_sms",
        lambda to, body: {
            "id": "provider-789",
            "status": "SENT",
        },
    )

    client.post(
        "/messages",
        json={
            "to": "+972548559208",
            "body": "Hello!",
        },
    )

    response = client.get("/messages?status=SENT")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["status"] == "SENT"


def test_provider_failure(client, monkeypatch):
    import httpx

    def failing_provider(to, body):
        raise httpx.ConnectError("Provider unavailable")

    monkeypatch.setattr(
        "app.routers.messages.send_sms",
        failing_provider,
    )

    response = client.post(
        "/messages",
        json={
            "to": "+972548559208",
            "body": "Hello!",
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "FAILED"


def test_invalid_phone_number(client):
    response = client.post(
        "/messages",
        json={
            "to": "12345",
            "body": "Hello!",
        },
    )

    assert response.status_code == 422


def test_empty_message_body(client):
    response = client.post(
        "/messages",
        json={
            "to": "+972548559208",
            "body": "   ",
        },
    )

    assert response.status_code == 422


def test_message_body_too_long(client):
    response = client.post(
        "/messages",
        json={
            "to": "+972548559208",
            "body": "A" * 161,
        },
    )

    assert response.status_code == 422
