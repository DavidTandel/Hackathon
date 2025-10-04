import React, { useContext, useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { RoleContext } from "./RoleContext";

function Dashboard() {
  const { role } = useContext(RoleContext);
  const [summary, setSummary] = useState({
    submitted: 0,
    approved: 0,
    rejected: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchSummary() {
      try {
        const response = await fetch("/api/dashboard-summary/", {
          credentials: "include",  // ensure session authentication/Cookie
        });
        const data = await response.json();
        setSummary(data);
      } catch {
        // handle error if desired
      }
      setLoading(false);
    }
    fetchSummary();
  }, []);

  return (
    <div style={{ margin: "2rem" }}>
      <h2 style={{ textAlign: "center", marginBottom: "2rem" }}>
        {role} Dashboard
      </h2>
      {loading ? (
        <div>Loading...</div>
      ) : (
        <div style={{
          display: "flex",
          gap: "2rem",
          justifyContent: "center",
          marginBottom: "2rem"
        }}>
          <div style={{ background: "#e3f2fd", padding: "1rem 2rem", borderRadius: "8px", boxShadow: "0 2px 5px #bbb" }}>
            <h3>Submitted</h3>
            <p style={{ fontSize: "2rem", textAlign: "center" }}>{summary.submitted}</p>
          </div>
          <div style={{ background: "#e8f5e9", padding: "1rem 2rem", borderRadius: "8px", boxShadow: "0 2px 5px #bbb" }}>
            <h3>Approved</h3>
            <p style={{ fontSize: "2rem", textAlign: "center" }}>{summary.approved}</p>
          </div>
          <div style={{ background: "#ffebee", padding: "1rem 2rem", borderRadius: "8px", boxShadow: "0 2px 5px #bbb" }}>
            <h3>Rejected</h3>
            <p style={{ fontSize: "2rem", textAlign: "center" }}>{summary.rejected}</p>
          </div>
        </div>
      )}
      {/* ...rest of your Dashboard component code... */}
    </div>
  );
}

export default Dashboard;
