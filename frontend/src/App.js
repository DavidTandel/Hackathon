import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./LoginPage";
import Dashboard from "./Dashboard";
import ExpenseSubmission from "./ExpenseSubmission";
import ApprovalPage from "./ApprovalPage";
import AdminSettings from "./AdminSettings";
import { RoleProvider } from "./RoleContext";

function App() {
  return (
    <RoleProvider>
      <Router>
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/submit-expense" element={<ExpenseSubmission />} />
          <Route path="/approve-expenses" element={<ApprovalPage />} />
          <Route path="/admin-settings" element={<AdminSettings />} />
        </Routes>
      </Router>
    </RoleProvider>
  );
}
export default App;
