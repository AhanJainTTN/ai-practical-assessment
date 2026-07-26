import { createContext, useContext, useEffect, useState } from "react";

const STORAGE_KEY = "actingAsUserId";

const ActingAsContext = createContext(null);

export function ActingAsProvider({ children }) {
  const [actingAsUserId, setActingAsUserIdState] = useState(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? Number(stored) : null;
  });

  useEffect(() => {
    if (actingAsUserId === null) {
      localStorage.removeItem(STORAGE_KEY);
      return;
    }
    localStorage.setItem(STORAGE_KEY, String(actingAsUserId));
  }, [actingAsUserId]);

  const setActingAsUserId = (userId) => {
    setActingAsUserIdState(userId === "" || userId === null ? null : Number(userId));
  };

  return (
    <ActingAsContext.Provider value={{ actingAsUserId, setActingAsUserId }}>
      {children}
    </ActingAsContext.Provider>
  );
}

export function useActingAs() {
  const context = useContext(ActingAsContext);
  if (!context) {
    throw new Error("useActingAs must be used within ActingAsProvider");
  }
  return context;
}
