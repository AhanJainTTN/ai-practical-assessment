import { Link } from "react-router-dom";

export function TicketListPage() {
  return (
    <div className="page-placeholder">
      <h1>Ticket list</h1>
      <p>Placeholder — list, status filter, and CSV export will be implemented in the Frontend UI milestone.</p>
      <p>
        <Link to="/tickets/new">Create ticket</Link>
      </p>
    </div>
  );
}

export function CreateTicketPage() {
  return (
    <div className="page-placeholder">
      <h1>Create ticket</h1>
      <p>Placeholder — create form will be implemented in the Frontend UI milestone.</p>
      <p>
        <Link to="/">Back to list</Link>
      </p>
    </div>
  );
}

export function TicketDetailPage() {
  return (
    <div className="page-placeholder">
      <h1>Ticket detail</h1>
      <p>Placeholder — detail view will be implemented in the Frontend UI milestone.</p>
      <p>
        <Link to="/">Back to list</Link>
      </p>
    </div>
  );
}
