import React, { useState, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { RoleContext } from "./RoleContext";

function Navbar() {
  const { role, setRole } = useContext(RoleContext);
  const [searchTerm, setSearchTerm] = useState("");
  const navigate = useNavigate();

  const handleLogout = () => {
    setRole(null);
    navigate("/");
  };

  return (
    <nav
      style={{
        display: "flex",
        alignItems: "center",
        background: "#1565c0",
        color: "#fff",
        padding: "0.7rem 2rem",
        gap: "2rem",
        justifyContent: "space-between"
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "2rem" }}>
        <Link to="/dashboard" style={{ color: "#fff", fontWeight: "bold", fontSize: "1.3rem", textDecoration: "none"}}>
          Expense Manager
        </Link>
        {/* Show navigation links only if logged in */}
        {role && (
          <>
            <Link to="/submit-expense" style={{ color: "#fff", textDecoration: "none" }}>
              Submit Expense
            </Link>
            {(role === "Manager" || role === "Admin") && (
              <Link to="/approve-expenses" style={{ color: "#fff", textDecoration: "none" }}>
                Approve Expenses
              </Link>
            )}
            {role === "Admin" && (
              <Link to="/admin-settings" style={{ color: "#fff", textDecoration: "none" }}>
                Admin Settings
              </Link>
            )}
          </>
        )}
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
        {role ? (
          <>
            <input
              style={{ padding: "0.4rem", borderRadius: "4px", border: "none" }}
              type="text"
              placeholder="Search expenses..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
            />
            <span
              style={{
                background: "#fff",
                color: "#1565c0",
                borderRadius: "12px",
                padding: "0.2rem 0.8rem",
                fontWeight: "bold"
              }}
            >
              {role}
            </span>
            <button
              onClick={handleLogout}
              style={{
                background: "#fff",
                color: "#1565c0",
                border: "none",
                borderRadius: "8px",
                padding: "0.4rem 1rem",
                fontWeight: "bold",
                cursor: "pointer"
              }}
            >
              Logout
            </button>
          </>
        ) : (
          <Link to="/" style={{ color: "#fff", textDecoration: "none", fontWeight: "bold" }}>
            Login
          </Link>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
