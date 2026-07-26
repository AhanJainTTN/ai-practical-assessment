import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
import { useActingAs } from "./context/ActingAsContext";
import {
  CreateTicketPage,
  TicketDetailPage,
  TicketListPage,
} from "./pages/Placeholders";

function AppHeader() {
  const { actingAsUserId, setActingAsUserId } = useActingAs();

  return (
    <header className="app-header">
      <Link to="/" className="app-brand">Support Tickets</Link>
      <div className="acting-as">
        <label htmlFor="acting-as-select">Acting as</label>
        <select
          id="acting-as-select"
          value={actingAsUserId ?? ""}
          onChange={(event) => setActingAsUserId(event.target.value)}
        >
          <option value="">Select user</option>
          {/* User options populated when users API is implemented */}
        </select>
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
