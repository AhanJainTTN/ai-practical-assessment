import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { apiClient } from "../api/client.js";
import { ErrorBanner } from "../components/ErrorBanner.jsx";
import { getAllowedNextStatuses, PRIORITIES } from "../constants.js";
import { useActingAs } from "../context/ActingAsContext.jsx";
import { getErrorMessage } from "../utils/errors.js";
import { formatDateTime } from "../utils/format.js";

export function TicketDetailPage() {
  const { id } = useParams();
  const { actingAsUserId } = useActingAs();
  const [users, setUsers] = useState([]);
  const [ticket, setTicket] = useState(null);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState("Medium");
  const [assignedTo, setAssignedTo] = useState("");
  const [commentMessage, setCommentMessage] = useState("");
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [isCommenting, setIsCommenting] = useState(false);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setIsLoading(true);
      setError("");
      try {
        const [usersData, ticketData] = await Promise.all([
          apiClient.getUsers(),
          apiClient.getTicket(id),
        ]);
        if (cancelled) {
          return;
        }
        setUsers(usersData);
        setTicket(ticketData);
        setTitle(ticketData.title);
        setDescription(ticketData.description);
        setPriority(ticketData.priority);
        setAssignedTo(ticketData.assignedTo ? String(ticketData.assignedTo.id) : "");
      } catch (err) {
        if (!cancelled) {
          setError(getErrorMessage(err, "Failed to load ticket."));
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [id]);

  const nextStatuses = ticket ? getAllowedNextStatuses(ticket.status) : [];

  async function handleSave(event) {
    event.preventDefault();
    setError("");
    setSuccessMessage("");
    setIsSaving(true);

    try {
      const updated = await apiClient.updateTicket(id, {
        title: title.trim(),
        description: description.trim(),
        priority,
        assignedTo: assignedTo ? Number(assignedTo) : null,
      });
      setTicket((current) => ({ ...current, ...updated, comments: current?.comments ?? updated.comments }));
      setSuccessMessage("Ticket updated.");
    } catch (err) {
      setError(getErrorMessage(err, "Failed to update ticket."));
    } finally {
      setIsSaving(false);
    }
  }

  async function handleTransition(status) {
    setError("");
    setSuccessMessage("");
    setIsTransitioning(true);

    try {
      const updated = await apiClient.transitionTicket(id, status);
      setTicket((current) => ({ ...current, ...updated, comments: current?.comments ?? updated.comments }));
      setSuccessMessage(`Status changed to ${status}.`);
    } catch (err) {
      setError(getErrorMessage(err, "Failed to change status."));
    } finally {
      setIsTransitioning(false);
    }
  }

  async function handleAddComment(event) {
    event.preventDefault();
    setError("");
    setSuccessMessage("");

    if (!actingAsUserId) {
      setError("Select an Acting-as user before adding a comment.");
      return;
    }

    if (!commentMessage.trim()) {
      setError("Comment message is required.");
      return;
    }

    setIsCommenting(true);
    try {
      const comment = await apiClient.createComment(id, {
        message: commentMessage.trim(),
        createdBy: actingAsUserId,
      });
      setTicket((current) => ({
        ...current,
        comments: [...(current?.comments ?? []), comment],
      }));
      setCommentMessage("");
      setSuccessMessage("Comment added.");
    } catch (err) {
      setError(getErrorMessage(err, "Failed to add comment."));
    } finally {
      setIsCommenting(false);
    }
  }

  if (isLoading) {
    return (
      <div className="page">
        <p className="empty-state">Loading ticket…</p>
      </div>
    );
  }

  if (!ticket) {
    return (
      <div className="page">
        <ErrorBanner message={error || "Ticket not found."} />
        <Link to="/" className="button button-secondary">
          Back to list
        </Link>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <p className="page-eyebrow">Ticket #{ticket.id}</p>
          <h1>{ticket.title}</h1>
        </div>
        <Link to="/" className="button button-secondary">
          Back to list
        </Link>
      </div>

      <ErrorBanner message={error} onDismiss={() => setError("")} />
      {successMessage ? <div className="success-banner">{successMessage}</div> : null}

      <div className="detail-grid">
        <section className="detail-panel">
          <h2>Details</h2>
          <form onSubmit={handleSave} className="form-card form-card-flat">
            <div className="form-field">
              <label htmlFor="detail-title">Title</label>
              <input
                id="detail-title"
                type="text"
                value={title}
                onChange={(event) => setTitle(event.target.value)}
                required
              />
            </div>

            <div className="form-field">
              <label htmlFor="detail-description">Description</label>
              <textarea
                id="detail-description"
                rows={6}
                value={description}
                onChange={(event) => setDescription(event.target.value)}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-field">
                <label htmlFor="detail-priority">Priority</label>
                <select
                  id="detail-priority"
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
                <label htmlFor="detail-assignee">Assignee</label>
                <select
                  id="detail-assignee"
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

            <dl className="meta-list">
              <div>
                <dt>Status</dt>
                <dd>
                  <span className={`status-pill status-${ticket.status.replace(/\s+/g, "-").toLowerCase()}`}>
                    {ticket.status}
                  </span>
                </dd>
              </div>
              <div>
                <dt>Created by</dt>
                <dd>{ticket.createdBy.name}</dd>
              </div>
              <div>
                <dt>Created</dt>
                <dd>{formatDateTime(ticket.createdAt)}</dd>
              </div>
              <div>
                <dt>Updated</dt>
                <dd>{formatDateTime(ticket.updatedAt)}</dd>
              </div>
            </dl>

            <div className="form-actions">
              <button type="submit" className="button button-primary" disabled={isSaving}>
                {isSaving ? "Saving…" : "Save changes"}
              </button>
            </div>
          </form>
        </section>

        <section className="detail-panel">
          <h2>Status</h2>
          {nextStatuses.length === 0 ? (
            <p className="muted-copy">No further transitions available for {ticket.status}.</p>
          ) : (
            <div className="transition-actions">
              {nextStatuses.map((status) => (
                <button
                  key={status}
                  type="button"
                  className="button button-secondary"
                  disabled={isTransitioning}
                  onClick={() => handleTransition(status)}
                >
                  Move to {status}
                </button>
              ))}
            </div>
          )}
        </section>
      </div>

      <section className="detail-panel comments-panel">
        <h2>Comments</h2>

        {ticket.comments.length === 0 ? (
          <p className="muted-copy">No comments yet.</p>
        ) : (
          <ul className="comment-list">
            {ticket.comments.map((comment) => (
              <li key={comment.id} className="comment-item">
                <div className="comment-meta">
                  <strong>{comment.createdBy.name}</strong>
                  <span>{formatDateTime(comment.createdAt)}</span>
                </div>
                <p>{comment.message}</p>
              </li>
            ))}
          </ul>
        )}

        {!actingAsUserId ? (
          <div className="notice-banner">
            Select an Acting-as user in the header before adding a comment.
          </div>
        ) : null}

        <form className="comment-form" onSubmit={handleAddComment}>
          <div className="form-field">
            <label htmlFor="comment-message">Add comment</label>
            <textarea
              id="comment-message"
              rows={3}
              value={commentMessage}
              onChange={(event) => setCommentMessage(event.target.value)}
              disabled={!actingAsUserId || isCommenting}
            />
          </div>
          <div className="form-actions">
            <button
              type="submit"
              className="button button-primary"
              disabled={!actingAsUserId || !commentMessage.trim() || isCommenting}
            >
              {isCommenting ? "Posting…" : "Post comment"}
            </button>
          </div>
        </form>
      </section>
    </div>
  );
}
