# 📱 SMS Messaging Service

A RESTful API for sending and tracking SMS messages, built with Python, FastAPI, SQLAlchemy, and SQLite.

## Technologies

- Python 3.12 & FastAPI
- SQLAlchemy & SQLite
- Pydantic & HTTPX
- Pytest
- Docker & Docker Compose

## Features

- Send SMS messages.
- Retrieve a message by ID.
- List all messages and filter by status.
- Validate phone numbers and message content.
- Store messages and their statuses in a database.
- Handle SMS provider failures.
- Automated tests for critical functionality.

## Architecture

The project is organized into separate modules:

- `routers/` – API endpoints.
- `models/` – Database models for employees, phone numbers, and messages.
- `schemas/` – Request and response validation.
- `services/` – SMS provider integration.
- `mock-sms-provider/` – Local mock SMS provider.

Employee identity is based on the unique combination of first name, last name, and address. Employees can have multiple phone numbers, and phone numbers are not assumed to be unique.

## Getting Started

Run the application from the project root:

```bash
docker compose up --build
```

Open Swagger UI:

[http://localhost:8000/docs](http://localhost:8000/docs)

Stop the application:

```bash
docker compose down
```

## Running Tests

```bash
docker compose exec backend pytest -v
```

**Test results:** 8 tests passed.

Tests use an isolated in-memory SQLite database and mock provider responses.

## Design Decisions & Assumptions

- SQLite was chosen for simplicity and lightweight relational storage.
- A local mock provider was implemented because no external provider URL or API specification was supplied.
- The provider URL can be configured using `SMS_PROVIDER_URL`.
- Message records are saved even when the provider request fails.
- `SENT` represents the provider's reported status, not guaranteed delivery to the recipient's device.
- Swagger UI is used instead of a separate frontend.

## Limitations & Future Improvements

- Real SMS provider integration.
- Database migrations with Alembic.
- Pagination and improved filtering.
- Retry handling and idempotency.
- Asynchronous message processing.
- Delivery receipts, logging, and monitoring.
- Authentication and authorization.

## AI Usage

AI tools were used for technical guidance, architecture discussions, code suggestions, debugging, test design, and documentation.

## Time Spent

**4 hours.**