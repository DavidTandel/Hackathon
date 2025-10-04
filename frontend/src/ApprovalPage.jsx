import React from "react";
function ApprovalPage() {
  // Load pending expenses via API/state
  return (
    <div>
      <h2>Approve/Reject Expenses</h2>
      {/* Example list, replace with API data */}
      <div>
        <p>Expense: $100 | Category: Travel | Date: 2025-10-02</p>
        <button>Approve</button>
        <button>Reject</button>
        <textarea placeholder="Comments" />
      </div>
    </div>
  );
}
export default ApprovalPage;
