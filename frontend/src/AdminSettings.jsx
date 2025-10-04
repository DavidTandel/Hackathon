import React, { useState } from "react";
function AdminSettings() {
  const [users, setUsers] = useState([]);
  const [approvalRule, setApprovalRule] = useState("sequence");

  // Handlers for user/role management, approval rules, currency settings, etc.

  return (
    <div>
      <h2>Admin Settings</h2>
      <section>
        <h3>Manage Users/Roles</h3>
        {/* Add/edit user forms */}
        <h3>Approval Flows</h3>
        <select value={approvalRule} onChange={e => setApprovalRule(e.target.value)}>
          <option value="sequence">Sequence</option>
          <option value="percentage">Percentage</option>
          <option value="specific">Specific Approver</option>
          <option value="hybrid">Hybrid</option>
        </select>
        {/* Setup rules for % required, specific approver, step sequence */}
        <h3>Currency Settings</h3>
        {/* Select country/currency from REST API */}
      </section>
    </div>
  );
}
export default AdminSettings;
