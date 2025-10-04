import React, { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { RoleContext } from "./RoleContext";

function LoginPage() {
  const navigate = useNavigate();
  const { setRole } = useContext(RoleContext);

  const [selectedRole, setSelectedRole] = useState("Employee");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();
    // Add authentication logic, API call here if needed
    setRole(selectedRole);
    navigate("/dashboard");
  };

  const handleSignupClick = () => {
    navigate("/register");
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <label>
          Role:
          <select value={selectedRole} onChange={(e) => setSelectedRole(e.target.value)}>
            <option value="Admin">Admin</option>
            <option value="Manager">Manager</option>
            <option value="Employee">Employee</option>
          </select>
        </label>
        <input
          type="email"
          placeholder="Email"
          required
          value={email}
          onChange={e => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          required
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
        <button type="submit">Login</button>
      </form>
      <hr />
      <p>
        Don't have an Admin account?{' '}
        <button onClick={handleSignupClick}>Sign up as Admin</button>
      </p>
    </div>
  );
}

export default LoginPage;
