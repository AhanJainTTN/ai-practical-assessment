import pytest

from helpers import ticket_in_status, transition_ticket


@pytest.mark.parametrize(
    ("from_status", "to_status"),
    [
        ("Open", "In Progress"),
        ("In Progress", "Resolved"),
        ("Resolved", "Closed"),
        ("Open", "Cancelled"),
        ("In Progress", "Cancelled"),
    ],
)
def test_valid_transitions_succeed(client, seed_users, from_status, to_status):
    ticket = ticket_in_status(client, seed_users["requester"].id, from_status)

    response = transition_ticket(client, ticket["id"], to_status)

    assert response.status_code == 200
    assert response.json()["status"] == to_status


@pytest.mark.parametrize(
    ("from_status", "to_status"),
    [
        ("Open", "Closed"),
        ("Resolved", "In Progress"),
        ("Closed", "Open"),
        ("Cancelled", "Open"),
    ],
)
def test_invalid_transitions_are_rejected(client, seed_users, from_status, to_status):
    ticket = ticket_in_status(client, seed_users["requester"].id, from_status)

    response = transition_ticket(client, ticket["id"], to_status)

    assert response.status_code == 400
    assert "Invalid transition" in response.json()["detail"]


def test_transition_on_missing_ticket_returns_404(client, seed_users):
    response = transition_ticket(client, 9999, "In Progress")

    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"
