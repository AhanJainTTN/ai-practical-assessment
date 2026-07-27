export const PRIORITIES = ["Low", "Medium", "High"];

export const STATUSES = [
  "Open",
  "In Progress",
  "Resolved",
  "Closed",
  "Cancelled",
];

/** Mirrors backend ALLOWED_TRANSITIONS in app/tickets/service.py */
export const ALLOWED_TRANSITIONS = {
  Open: ["In Progress", "Cancelled"],
  "In Progress": ["Resolved", "Cancelled"],
  Resolved: ["Closed"],
  Closed: [],
  Cancelled: [],
};

export function getAllowedNextStatuses(currentStatus) {
  return ALLOWED_TRANSITIONS[currentStatus] ?? [];
}
