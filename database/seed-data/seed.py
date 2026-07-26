"""Wipe and reseed demo data for local development."""

import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[2] / "src" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from sqlalchemy import delete

from app.comments.models import Comment
from app.core.database import SessionLocal
from app.core.time import utcnow
from app.tickets.models import Ticket
from app.users.models import User


def seed() -> None:
    db = SessionLocal()
    try:
        db.execute(delete(Comment))
        db.execute(delete(Ticket))
        db.execute(delete(User))
        db.commit()

        users = [
            User(name="Alice Requester", email="alice@example.com", role="requester"),
            User(name="Bob Requester", email="bob@example.com", role="requester"),
            User(name="Carol Agent", email="carol@example.com", role="agent"),
        ]
        db.add_all(users)
        db.flush()

        alice, bob, carol = users
        now = utcnow()

        tickets = [
            Ticket(
                title="Cannot log in",
                description="Password reset link does not arrive in my inbox.",
                priority="High",
                status="Open",
                created_by=alice.id,
                assigned_to=carol.id,
                created_at=now,
                updated_at=now,
            ),
            Ticket(
                title="Export button missing on reports page",
                description="The CSV export option is not visible after the latest update.",
                priority="Medium",
                status="Open",
                created_by=alice.id,
                assigned_to=None,
                created_at=now,
                updated_at=now,
            ),
            Ticket(
                title="Slow dashboard load",
                description="Dashboard takes over 10 seconds to load on first visit.",
                priority="Medium",
                status="In Progress",
                created_by=bob.id,
                assigned_to=carol.id,
                created_at=now,
                updated_at=now,
            ),
            Ticket(
                title="Billing amount incorrect",
                description="Last invoice shows duplicate line items.",
                priority="Low",
                status="Resolved",
                created_by=bob.id,
                assigned_to=carol.id,
                created_at=now,
                updated_at=now,
            ),
            Ticket(
                title="Feature request: dark mode",
                description="Users have requested a dark mode toggle in settings.",
                priority="Low",
                status="Closed",
                created_by=carol.id,
                assigned_to=carol.id,
                created_at=now,
                updated_at=now,
            ),
            Ticket(
                title="Duplicate account merge",
                description="Customer asked to merge two accounts; request withdrawn.",
                priority="High",
                status="Cancelled",
                created_by=alice.id,
                assigned_to=None,
                created_at=now,
                updated_at=now,
            ),
        ]
        db.add_all(tickets)
        db.flush()

        open_ticket = tickets[0]
        comments = [
            Comment(
                ticket_id=open_ticket.id,
                message="I tried twice and checked spam folder.",
                created_by=alice.id,
                created_at=now,
            ),
            Comment(
                ticket_id=open_ticket.id,
                message="Checking mail server logs on our side.",
                created_by=carol.id,
                created_at=now,
            ),
        ]
        db.add_all(comments)
        db.commit()

        print(
            f"Seed complete: {len(users)} users, {len(tickets)} tickets, {len(comments)} comments",
        )
    finally:
        db.close()


if __name__ == "__main__":
    seed()
