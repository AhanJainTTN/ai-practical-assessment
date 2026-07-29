import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiClient, downloadBlob } from "../api/client.js";
import { ErrorBanner } from "../components/ErrorBanner.jsx";
import { STATUSES } from "../constants.js";
import { useActingAs } from "../context/ActingAsContext.jsx";
import { getErrorMessage } from "../utils/errors.js";
import { formatDateTime } from "../utils/format.js";

export function TicketListPage() {
  const { actingAsUserId } = useActingAs();
  const [statusFilter, setStatusFilter] = useState("");
  const [tickets, setTickets] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [exportError, setExportError] = useState("");
  const [isExporting, setIsExporting] = useState(false);

  const loadTickets = useCallback(async () => {
    setIsLoading(true);
    setError("");
    try {
      const data = await apiClient.getTickets(statusFilter || undefined);
      setTickets(data);
    } catch (err) {
      setError(getErrorMessage(err, "Failed to load tickets."));
    } finally {
      setIsLoading(false);
    }
  }, [statusFilter]);

  useEffect(() => {
    loadTickets();
  }, [loadTickets]);

  async function handleExport() {
    setExportError("");

    if (!actingAsUserId) {
      setExportError("Select an Acting-as user before exporting tickets.");
      return;
    }

    setIsExporting(true);
    try {
      const blob = await apiClient.exportTicketsCsv(actingAsUserId);
      downloadBlob(blob, "tickets-export.csv");
    } catch (err) {
      setExportError(getErrorMessage(err, "Failed to export tickets."));
    } finally {
      setIsExporting(false);
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <p className="page-eyebrow">Support queue</p>
          <h1>Tickets</h1>
        </div>
        <div className="page-actions">
          <button
            type="button"
            className="button button-secondary"
            onClick={handleExport}
            disabled={isExporting}
          >
            {isExporting ? "Exporting…" : "Export CSV"}
          </button>
          <Link to="/tickets/new" className="button button-primary">
            Create ticket
          </Link>
        </div>
      </div>

      <ErrorBanner message={error} onDismiss={() => setError("")} />
      <ErrorBanner message={exportError} onDismiss={() => setExportError("")} />

      <div className="toolbar">
        <label className="filter-control" htmlFor="status-filter">
          Status
          <select
            id="status-filter"
            value={statusFilter}
            onChange={(event) => setStatusFilter(event.target.value)}
          >
            <option value="">All</option>
            {STATUSES.map((status) => (
              <option key={status} value={status}>
                {status}
              </option>
            ))}
          </select>
        </label>
        <span className="toolbar-meta">
          {isLoading ? "Loading…" : `${tickets.length} ticket${tickets.length === 1 ? "" : "s"}`}
        </span>
      </div>

      {isLoading ? (
        <p className="empty-state">Loading tickets…</p>
      ) : tickets.length === 0 ? (
        <p className="empty-state">No tickets match this filter.</p>
      ) : (
        <div className="ticket-list">
          <div className="ticket-list-header">
            <span>Title</span>
            <span>Status</span>
            <span>Priority</span>
            <span>Assignee</span>
            <span>Created</span>
          </div>
          {tickets.map((ticket) => (
            <Link key={ticket.id} to={`/tickets/${ticket.id}`} className="ticket-row">
              <span className="ticket-title">{ticket.title}</span>
              <span>
                <span className={`status-pill status-${ticket.status.replace(/\s+/g, "-").toLowerCase()}`}>
                  {ticket.status}
                </span>
              </span>
              <span className="ticket-meta">{ticket.priority}</span>
              <span className="ticket-meta">{ticket.assignedTo?.name ?? "Unassigned"}</span>
              <span className="ticket-meta">{formatDateTime(ticket.createdAt)}</span>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
