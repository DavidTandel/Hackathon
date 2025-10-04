import React, { useState } from "react";

const initialUsers = [
  { id: 1, name: "Alice", role: "Manager", email: "alice@example.com" },
  { id: 2, name: "Bob", role: "Employee", email: "bob@example.com" },
];

function AdminSettings() {
  const [users, setUsers] = useState(initialUsers);
  const [newUser, setNewUser] = useState({ name: "", email: "", role: "Employee" });
  const [approvalRule, setApprovalRule] = useState("sequence");
  const [currency, setCurrency] = useState("USD");
  const [country, setCountry] = useState("USA");

  // User management handlers
  const addUser = (e) => {
    e.preventDefault();
    if (!newUser.name || !newUser.email) return;
    setUsers([
      ...users,
      { id: users.length + 1, ...newUser }
    ]);
    setNewUser({ name: "", email: "", role: "Employee" });
  };

  return (
    <div style={{ maxWidth: 900, margin: "2rem auto", padding: "2rem" }}>
      <h2 style={{ textAlign: "center", marginBottom: "2rem" }}>Admin Settings</h2>
      <div style={{ display: "flex", gap: "2rem", flexWrap: "wrap" }}>
        {/* User Management Card */}
        <section style={{
          flex: "1 1 350px",
          background: "#fff",
          borderRadius: "12px",
          boxShadow: "0 2px 8px #eee",
          padding: "1.5rem"
        }}>
          <h3>Manage Users & Roles</h3>
          <form onSubmit={addUser} style={{ marginBottom: "1.5rem" }}>
            <input
              style={{ marginRight: "8px" }}
              type="text"
              placeholder="Name"
              value={newUser.name}
              onChange={e => setNewUser({ ...newUser, name: e.target.value })}
              required
            />
            <input
              style={{ marginRight: "8px" }}
              type="email"
              placeholder="Email"
              value={newUser.email}
              onChange={e => setNewUser({ ...newUser, email: e.target.value })}
              required
            />
            <select
              style={{ marginRight: "8px" }}
              value={newUser.role}
              onChange={e => setNewUser({ ...newUser, role: e.target.value })}
            >
              <option value="Employee">Employee</option>
              <option value="Manager">Manager</option>
            </select>
            <button type="submit">Add User</button>
          </form>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ background: "#f5f5f5" }}>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
              </tr>
            </thead>
            <tbody>
              {users.map(u =>
                <tr key={u.id}>
                  <td>{u.name}</td>
                  <td>{u.email}</td>
                  <td>{u.role}</td>
                </tr>
              )}
            </tbody>
          </table>
        </section>

        {/* Approval Flow Card */}
        <section style={{
          flex: "1 1 350px",
          background: "#fff",
          borderRadius: "12px",
          boxShadow: "0 2px 8px #eee",
          padding: "1.5rem"
        }}>
          <h3>Configure Approval Flow</h3>
          <label>
            Rule Type:
            <select
              style={{ marginLeft: "1rem" }}
              value={approvalRule}
              onChange={e => setApprovalRule(e.target.value)}
            >
              <option value="sequence">Sequence</option>
              <option value="percentage">Percentage</option>
              <option value="specific">Specific Approver</option>
              <option value="hybrid">Hybrid</option>
            </select>
          </label>
          <div style={{ marginTop: "1rem" }}>
            {approvalRule === "sequence" && (
              <p>Expenses move through a fixed approval sequence (e.g., Manager → Finance → Director).</p>
            )}
            {approvalRule === "percentage" && (
              <p>Auto-approve expense when a certain % of approvers approve (e.g., 60%).</p>
            )}
            {approvalRule === "specific" && (
              <p>If a specific approver (e.g., CFO) approves, expense is auto-approved.</p>
            )}
            {approvalRule === "hybrid" && (
              <p>Combine both rules (e.g., 60% approval or CFO approval triggers auto-approve).</p>
            )}
          </div>
        </section>
      </div>

      <hr style={{ margin: "2rem 0", borderColor: "#eee" }} />

      {/* Currency & Country Settings */}
      <section style={{
        background: "#fff",
        borderRadius: "12px",
        boxShadow: "0 2px 8px #eee",
        padding: "1.5rem",
        maxWidth: "500px",
        margin: "0 auto"
      }}>
        <h3>Company Settings</h3>
        <form>
          <label style={{ marginRight: "2rem" }}>
            Country:
            <select
              style={{ marginLeft: "1rem" }}
              value={country}
              onChange={e => setCountry(e.target.value)}
            >
              <option value="USA">USA</option>
              <option value="India">India</option>
              <option value="UK">UK</option>
            </select>
          </label>
          <label>
            Currency:
            <select
              style={{ marginLeft: "1rem" }}
              value={currency}
              onChange={e => setCurrency(e.target.value)}
            >
              <option value="USD">USD</option>
              <option value="INR">INR</option>
              <option value="GBP">GBP</option>
            </select>
          </label>
        </form>
      </section>
    </div>
  );
}

export default AdminSettings;
