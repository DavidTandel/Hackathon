import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { RoleContext } from "./RoleContext";

// Sample summary data (replace with API calls)
const summary = {
  submitted: 12,
  approved: 9,
  rejected: 3,
};

function Dashboard() {
  const { role } = useContext(RoleContext);

  return (
    <div style={{ margin: "2rem" }}>
      <h2 style={{ textAlign: "center", marginBottom: "2rem" }}>
        {role} Dashboard
      </h2>
      <div style={{
        display: "flex",
        gap: "2rem",
        justifyContent: "center",
        marginBottom: "2rem"
      }}>
        <div style={{
          background: "#e3f2fd",
          padding: "1rem 2rem",
          borderRadius: "8px",
          boxShadow: "0 2px 5px #bbb"
        }}>
          <h3>Submitted</h3>
          <p style={{ fontSize: "2rem", textAlign: "center" }}>{summary.submitted}</p>
        </div>
        <div style={{
          background: "#e8f5e9",
          padding: "1rem 2rem",
          borderRadius: "8px",
          boxShadow: "0 2px 5px #bbb"
        }}>
          <h3>Approved</h3>
          <p style={{ fontSize: "2rem", textAlign: "center" }}>{summary.approved}</p>
        </div>
        <div style={{
          background: "#ffebee",
          padding: "1rem 2rem",
          borderRadius: "8px",
          boxShadow: "0 2px 5px #bbb"
        }}>
          <h3>Rejected</h3>
          <p style={{ fontSize: "2rem", textAlign: "center" }}>{summary.rejected}</p>
        </div>
      </div>
      <nav style={{ display: "flex", gap: "1rem", justifyContent: "center", marginBottom: "2rem" }}>
        <Link to="/submit-expense">
          <button style={{ padding: "0.7rem 1.5rem", fontWeight: "bold", borderRadius: "6px" }}>
            Submit Expense
          </button>
        </Link>
        {(role === "Manager" || role === "Admin") && (
          <Link to="/approve-expenses">
            <button style={{ padding: "0.7rem 1.5rem", fontWeight: "bold", borderRadius: "6px" }}>
              Approve Expenses
            </button>
          </Link>
        )}
        {role === "Admin" && (
          <Link to="/admin-settings">
            <button style={{ padding: "0.7rem 1.5rem", fontWeight: "bold", borderRadius: "6px" }}>
              Admin Settings
            </button>
          </Link>
        )}
      </nav>
      <div style={{
        background: "#f5f5f5",
        padding: "1rem 2rem",
        borderRadius: "10px",
        boxShadow: "0 1px 4px #ddd",
        maxWidth: "600px",
        margin: "0 auto"
      }}>
        {role === "Employee" && (
          <div>
            <h3>Expense History</h3>
            <p>View your submitted claims status. Track approvals and rejections.</p>
          </div>
        )}
        {role === "Manager" && (
          <div>
            <h3>Team Expenses</h3>
            <p>Approve or escalate team claims. View overall stats for your department.</p>
          </div>
        )}
        {role === "Admin" && (
          <div>
            <h3>Company Controls</h3>
            <p>Manage employees/managers, control approval flows, set company currency and view all expenses.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
