import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { RoleContext } from "./RoleContext";

function LoginPage() {
  const navigate = useNavigate();
  const { setRole } = useContext(RoleContext);

  const handleLogin = (role) => {
    setRole(role);
    navigate("/dashboard");
  };

  return (
    <div>
      <h2>Login / Signup</h2>
      <button onClick={() => handleLogin("Admin")}>Login as Admin</button>
      <button onClick={() => handleLogin("Manager")}>Login as Manager</button>
      <button onClick={() => handleLogin("Employee")}>Login as Employee</button>
    </div>
  );
}

export default LoginPage;
