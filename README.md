# SMS Messaging Service

## 1. Overview

This project implements a REST API for sending and tracking SMS messages to employees.

The service is built with Python, FastAPI, SQLAlchemy, and SQLite. It communicates with an SMS provider through a dedicated service layer and persists message information in a relational database.

The project focuses on clear separation of responsibilities, input validation, persistence, error handling, and automated testing.

## 2. Technologies

- **Python 3.12** – Backend programming language.
- **FastAPI** – REST API framework.
- **SQLAlchemy** – ORM and database access.
- **SQLite** – Relational database.
- **Pydantic** – Request validation and response schemas.
- **HTTPX** – HTTP communication with the SMS provider.
- **Pytest** – Automated testing.
- **Docker & Docker Compose** – Local development and execution.

## 3. Project Structure

```text
SMS_service/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── employee.py
│   │   │   ├── message.py
│   │   │   └── __init__.py
│   │   ├── routers/
│   │   │   ├── messages.py
│   │   │   └── __init__.py
│   │   ├── schemas/
│   │   │   ├── message.py
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   ├── sms_provider.py
│   │   │   └── __init__.py
│   │   ├── database.py
│   │   └── main.py
│   ├── tests/
│   │   ├── conftest.py
│   │   └── test_messages.py
│   ├── Dockerfile
│   └── requirements.txt
├── mock-sms-provider/
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 4. Architecture and Main Components

The application is divided into separate modules, each with a specific responsibility.

### API Layer – `routers/`

`messages.py` contains the message endpoints and coordinates the application flow.

It handles incoming requests, interacts with the database, and calls the SMS provider service when necessary.

### Data Models – `models/`

The project uses SQLAlchemy models:

- `Employee` – Represents an employee.
- `EmployeePhone` – Represents phone numbers associated with employees.
- `Message` – Represents an SMS message and its current status.

Employee identity is defined by the combination of first name, last name, and address. This combination has a unique database constraint.

An employee can have multiple phone numbers, and phone numbers are not assumed to be unique.

Messages store the destination phone number directly. The system does not identify an employee based on a phone number alone.

### Schemas – `schemas/`

Pydantic schemas define the API request and response structures.

They are responsible for input validation and ensuring consistent API responses.

### Provider Integration – `services/`

`sms_provider.py` isolates HTTP communication with the SMS provider.

This separation keeps provider-specific communication outside the API routing logic and makes it easier to replace or extend the provider integration.

### Database – `database.py`

SQLAlchemy manages database connections and sessions.

SQLite was selected because the project has a relatively simple relational data model and does not require a separate database server.

### Mock SMS Provider – `mock-sms-provider/`

A local mock provider simulates the external SMS provider's POST and GET operations.

It allows the application to be developed and tested without depending on an external service.

## 5. Running the Application

Docker Compose is used to run the backend and mock SMS provider together.

From the project root directory, execute:

```bash
docker compose up --build
```

The services will be available at:

| Service | URL |
|---|---|
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| OpenAPI schema | http://localhost:8000/openapi.json |
| Backend health check | http://localhost:8000/health |
| Mock SMS Provider | http://localhost:8001 |

To stop the services:

```bash
docker compose down
```

The SQLite database is stored in a Docker named volume to preserve message data across container restarts.

## 6. API Endpoints

### 6.1 Send an SMS

**POST `/messages`**

Creates a message, stores it in the database, and attempts to send it through the configured SMS provider.

Request body:

```json
{
  "to": "+972548512345",
  "body": "Hello!"
}
```

A successful API request returns HTTP `201 Created` and the created message, including its application ID and status.

### 6.2 Retrieve a Message

**GET `/messages/{message_id}`**

Retrieves a message by its application ID.

When a provider message ID exists, the service attempts to retrieve the latest status from the provider and update the stored status.

Returns HTTP `404 Not Found` if the message does not exist.

### 6.3 List Messages

**GET `/messages`**

Returns all stored messages, ordered by creation time, newest first.

### 6.4 Filter Messages by Status

**GET `/messages?status=SENT`**

Returns messages matching the requested status.

Supported statuses:

- `PENDING`
- `SENT`
- `FAILED`

Invalid status values are rejected by request validation.

## 7. Validation Rules

The API validates incoming message data:

- Phone numbers must follow the international E.164 format.
- Message bodies must not be empty or contain only whitespace.
- Message bodies are limited to 160 characters.

These validation rules are explicit implementation assumptions. A production integration should also account for the actual provider's restrictions and SMS encoding/segmentation rules.

## 8. Message Statuses

The application uses three statuses:

| Status | Meaning |
|---|---|
| `PENDING` | The message has been created and is awaiting provider processing. |
| `SENT` | The provider accepted the message and returned a successful status. |
| `FAILED` | The provider request failed or its response could not be processed. |

`SENT` represents the provider's reported status. It does not guarantee that the SMS was delivered to the recipient's device.

## 9. Design Decisions and Assumptions

### Database Choice

SQLite was selected because it provides relational data storage without requiring a separate database server.

### Employee Identification

The assignment specifies that employees do not have employee numbers.

Therefore, employee identity is based on a unique combination of first name, last name, and address.

Phone numbers are stored separately because an employee may have multiple phone numbers and a phone number is not guaranteed to uniquely identify an employee.

### SMS Provider Assumption

The assignment refers to a mock SMS provider but did not provide an accessible provider URL or API specification.

As a result, a local mock provider was implemented to simulate the required POST and GET operations.

This is a development substitute, not an integration with an externally supplied provider.

The backend communicates with the provider through a dedicated service module. The provider URL is configurable through the `SMS_PROVIDER_URL` environment variable.

The local mock provider stores messages in memory. Its data is therefore reset when the provider process restarts.

### Provider Failure Handling

If the provider request fails or returns a response that cannot be processed, the application retains the message in the database and marks it as `FAILED`.

When retrieving a message, a provider status lookup failure does not overwrite the last successfully stored status.

### User Interface

FastAPI's Swagger UI provides an interface for exploring and testing the API endpoints.

## 10. Automated Tests

Automated tests are implemented using Pytest and FastAPI TestClient.

The test suite covers:

1. Successful message creation.
2. Message retrieval.
3. Handling requests for non-existent messages.
4. Filtering messages by status.
5. Provider failure handling.
6. Invalid phone number validation.
7. Empty message body validation.
8. Message body length validation.

The tests use an isolated in-memory SQLite database and mock provider calls where appropriate, avoiding dependency on an external SMS service.

To run the tests:

```bash
docker compose exec backend pytest -v
```

Current result: **8 tests passed.**

## 11. Limitations and Future Improvements

The implementation intentionally focuses on the requirements of the assignment.

If additional development time were available, I would consider:

- Integrating a real SMS provider.
- Adding database migrations with Alembic.
- Adding pagination to the messages listing endpoint.
- Implementing retry handling for temporary provider failures.
- Supporting delivery receipts and additional message statuses.
- Adding idempotency support to prevent duplicate messages.
- Introducing asynchronous message processing for high-volume campaigns.
- Adding structured logging, metrics, and monitoring.
- Adding authentication and authorization if required.

## 12. AI Usage

AI tools were used during development for technical guidance, architecture discussions, code suggestions, debugging, test design, and documentation assistance.

## 13. Time Spent

Total time spent on the assignment: 4 Hours.

