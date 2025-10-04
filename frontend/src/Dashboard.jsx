import React, { useContext } from "react";
import { RoleContext } from "./RoleContext";
import { Link } from "react-router-dom";

function Dashboard() {
  const { role } = useContext(RoleContext);
  return (
    <div>
      <h2>Dashboard ({role})</h2>
      <nav>
        <Link to="/submit-expense">Submit Expense</Link>
        {(role === "Manager" || role === "Admin") && <Link to="/approve-expenses">Approve Expenses</Link>}
        {role === "Admin" && <Link to="/admin-settings">Admin Settings</Link>}
      </nav>
      <section>
        <p>Summary of submitted, approved, and rejected expenses here.</p>
      </section>
    </div>
  );
}
export default Dashboard;
