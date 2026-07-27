import { useEffect, useState } from "react";
import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
import { apiClient } from "./api/client.js";
import { useActingAs } from "./context/ActingAsContext.jsx";
import { CreateTicketPage } from "./pages/CreateTicketPage.jsx";
import { TicketDetailPage } from "./pages/TicketDetailPage.jsx";
import { TicketListPage } from "./pages/TicketListPage.jsx";
import { getErrorMessage } from "./utils/errors.js";

function AppHeader() {
  const { actingAsUserId, setActingAsUserId } = useActingAs();
  const [users, setUsers] = useState([]);
  const [loadError, setLoadError] = useState("");

  useEffect(() => {
    apiClient
      .getUsers()
      .then(setUsers)
      .catch((err) => setLoadError(getErrorMessage(err, "Failed to load users.")));
  }, []);

  const selectedUser = users.find((user) => user.id === actingAsUserId);

  return (
    <header className="app-header">
      <Link to="/" className="app-brand">
        Support Tickets
      </Link>
      <div className="header-actions">
        {loadError ? <span className="header-error">{loadError}</span> : null}
        <div className="acting-as">
          <label htmlFor="acting-as-select">Acting as</label>
          <select
            id="acting-as-select"
            value={actingAsUserId ?? ""}
            onChange={(event) => setActingAsUserId(event.target.value)}
          >
            <option value="">Select user</option>
            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.name} ({user.role})
              </option>
            ))}
          </select>
        </div>
        {!actingAsUserId ? (
          <span className="acting-as-hint">Required for create, comment, export</span>
        ) : selectedUser ? (
          <span className="acting-as-selected">{selectedUser.email}</span>
        ) : null}
      </div>
    </header>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <AppHeader />
        <main className="app-main">
          <Routes>
            <Route path="/" element={<TicketListPage />} />
            <Route path="/tickets/new" element={<CreateTicketPage />} />
            <Route path="/tickets/:id" element={<TicketDetailPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
