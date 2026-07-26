import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import { ActingAsProvider } from "./context/ActingAsContext.jsx";
import "./index.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <ActingAsProvider>
      <App />
    </ActingAsProvider>
  </StrictMode>,
);
