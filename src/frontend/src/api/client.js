import { formatApiError } from "../utils/errors.js";

const API_BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    throw new Error(
      formatApiError(errorBody.detail, `Request failed with status ${response.status}`),
    );
  }

  if (response.status === 204) {
    return null;
  }

  const contentType = response.headers.get("content-type") ?? "";
  if (contentType.includes("application/json")) {
    return response.json();
  }

  return response.text();
}

async function requestBlob(path) {
  const response = await fetch(`${API_BASE_URL}${path}`);

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    throw new Error(
      formatApiError(errorBody.detail, `Request failed with status ${response.status}`),
    );
  }

  return response.blob();
}

export const apiClient = {
  getUsers: () => request("/api/users"),
  getTickets: (status) => {
    const query = status ? `?status=${encodeURIComponent(status)}` : "";
    return request(`/api/tickets${query}`);
  },
  getTicket: (id) => request(`/api/tickets/${id}`),
  createTicket: (payload) =>
    request("/api/tickets", { method: "POST", body: JSON.stringify(payload) }),
  updateTicket: (id, payload) =>
    request(`/api/tickets/${id}`, { method: "PATCH", body: JSON.stringify(payload) }),
  transitionTicket: (id, status) =>
    request(`/api/tickets/${id}/transitions`, {
      method: "POST",
      body: JSON.stringify({ status }),
    }),
  createComment: (ticketId, payload) =>
    request(`/api/tickets/${ticketId}/comments`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  exportTicketsCsv: (createdBy) =>
    requestBlob(`/api/tickets/export.csv?createdBy=${createdBy}`),
};

export function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}
