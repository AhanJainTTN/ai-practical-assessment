import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiClient } from "../api/client.js";
import { ErrorBanner } from "../components/ErrorBanner.jsx";
import { useActingAs } from "../context/ActingAsContext.jsx";
import { PRIORITIES } from "../constants.js";
import { getErrorMessage } from "../utils/errors.js";

export function CreateTicketPage() {
  const navigate = useNavigate();
  const { actingAsUserId } = useActingAs();
  const [users, setUsers] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState("Medium");
  const [assignedTo, setAssignedTo] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    apiClient
      .getUsers()
      .then(setUsers)
      .catch((err) => setError(getErrorMessage(err, "Failed to load users.")));
  }, []);

  const actingAsUser = users.find((user) => user.id === actingAsUserId) ?? null;
  const canSubmit = Boolean(actingAsUserId) && title.trim() && description.trim() && !isSubmitting;

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");

    if (!actingAsUserId) {
      setError("Select an Acting-as user before creating a ticket.");
      return;
    }

    setIsSubmitting(true);
    try {
      const ticket = await apiClient.createTicket({
        title: title.trim(),
        description: description.trim(),
        priority,
        createdBy: actingAsUserId,
        assignedTo: assignedTo ? Number(assignedTo) : null,
      });
      navigate(`/tickets/${ticket.id}`);
    } catch (err) {
      setError(getErrorMessage(err, "Failed to create ticket."));
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <p className="page-eyebrow">New ticket</p>
          <h1>Create ticket</h1>
        </div>
        <Link to="/" className="button button-secondary">
          Back to list
        </Link>
      </div>

      <ErrorBanner message={error} onDismiss={() => setError("")} />

      {!actingAsUserId ? (
        <div className="notice-banner">
          Select an Acting-as user in the header before creating a ticket.
        </div>
      ) : null}

      <form className="form-card" onSubmit={handleSubmit}>
        <div className="form-field">
          <label htmlFor="ticket-title">Title</label>
          <input
            id="ticket-title"
            type="text"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            required
          />
        </div>

        <div className="form-field">
          <label htmlFor="ticket-description">Description</label>
          <textarea
            id="ticket-description"
            rows={5}
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            required
          />
        </div>

        <div className="form-row">
          <div className="form-field">
            <label htmlFor="ticket-priority">Priority</label>
            <select
              id="ticket-priority"
              value={priority}
              onChange={(event) => setPriority(event.target.value)}
            >
              {PRIORITIES.map((value) => (
                <option key={value} value={value}>
                  {value}
                </option>
              ))}
            </select>
          </div>

          <div className="form-field">
            <label htmlFor="ticket-assignee">Assignee (optional)</label>
            <select
              id="ticket-assignee"
              value={assignedTo}
              onChange={(event) => setAssignedTo(event.target.value)}
            >
              <option value="">Unassigned</option>
              {users.map((user) => (
                <option key={user.id} value={user.id}>
                  {user.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="form-field">
          <label>Created by</label>
          <p className="read-only-field">
            {actingAsUser ? `${actingAsUser.name} (${actingAsUser.email})` : "Not selected"}
          </p>
        </div>

        <div className="form-field">
          <label>Status</label>
          <p className="read-only-field">Open (set automatically on create)</p>
        </div>

        <div className="form-actions">
          <button type="submit" className="button button-primary" disabled={!canSubmit}>
            {isSubmitting ? "Creating…" : "Create ticket"}
          </button>
        </div>
      </form>
    </div>
  );
}
