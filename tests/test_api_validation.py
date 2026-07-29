from helpers import create_open_ticket, ticket_in_status


def test_create_ticket_missing_required_fields_returns_422(client, seed_users):
    response = client.post(
        "/api/tickets",
        json={"title": "", "description": "desc", "priority": "Medium", "createdBy": seed_users["requester"].id},
    )

    assert response.status_code == 422


def test_create_ticket_invalid_priority_returns_422(client, seed_users):
    response = client.post(
        "/api/tickets",
        json={
            "title": "Title",
            "description": "Description",
            "priority": "Urgent",
            "createdBy": seed_users["requester"].id,
        },
    )

    assert response.status_code == 422


def test_assign_to_nonexistent_user_returns_422(client, seed_users):
    response = client.post(
        "/api/tickets",
        json={
            "title": "Title",
            "description": "Description",
            "priority": "Medium",
            "createdBy": seed_users["requester"].id,
            "assignedTo": 9999,
        },
    )

    assert response.status_code == 422
    assert "assignedTo user does not exist" in response.json()["detail"]


def test_comment_on_missing_ticket_returns_404(client, seed_users):
    response = client.post(
        "/api/tickets/9999/comments",
        json={"message": "Hello", "createdBy": seed_users["requester"].id},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"


def test_list_filter_by_status_returns_subset(client, seed_users):
    ticket_in_status(client, seed_users["requester"].id, "Open")
    ticket_in_status(client, seed_users["requester"].id, "Resolved")

    response = client.get("/api/tickets", params={"status": "Open"})

    assert response.status_code == 200
    tickets = response.json()
    assert len(tickets) == 1
    assert tickets[0]["status"] == "Open"


def test_csv_export_with_no_matches_returns_headers_only(client, seed_users):
    create_open_ticket(client, seed_users["agent"].id)

    response = client.get(
        "/api/tickets/export.csv",
        params={"createdBy": seed_users["requester"].id},
    )

    assert response.status_code == 200
    lines = response.text.strip().splitlines()
    assert len(lines) == 1
    assert lines[0].startswith("id,title,description,priority,status,")
