from fastapi.testclient import TestClient


def create_open_ticket(client: TestClient, created_by: int, **overrides) -> dict:
    payload = {
        "title": "Test ticket",
        "description": "Test description",
        "priority": "Medium",
        "createdBy": created_by,
        **overrides,
    }
    response = client.post("/api/tickets", json=payload)
    assert response.status_code == 201
    return response.json()


def transition_ticket(client: TestClient, ticket_id: int, status: str):
    return client.post(
        f"/api/tickets/{ticket_id}/transitions",
        json={"status": status},
    )


def ticket_in_status(client: TestClient, created_by: int, status: str) -> dict:
    ticket = create_open_ticket(client, created_by)
    paths: dict[str, list[str]] = {
        "Open": [],
        "In Progress": ["In Progress"],
        "Resolved": ["In Progress", "Resolved"],
        "Closed": ["In Progress", "Resolved", "Closed"],
        "Cancelled": ["Cancelled"],
    }
    for next_status in paths[status]:
        response = transition_ticket(client, ticket["id"], next_status)
        assert response.status_code == 200, response.text
        ticket = response.json()
    return ticket
