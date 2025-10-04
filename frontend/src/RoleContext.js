// RoleContext.js
import React, { createContext, useState } from "react";
export const RoleContext = createContext();
export function RoleProvider({ children }) {
  const [role, setRole] = useState(null);  // Should be null (not a string role)
  return (
    <RoleContext.Provider value={{ role, setRole }}>
      {children}
    </RoleContext.Provider>
  );
}
