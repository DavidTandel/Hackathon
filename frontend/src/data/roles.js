export const roles = [
  { name: "Admin", permissions: ["manage_users", "override_approvals", "set_rules"] },
  { name: "Manager", permissions: ["approve_expenses", "escalate", "view_team"] },
  { name: "Employee", permissions: ["submit_expenses", "view_own_history"] }
];
