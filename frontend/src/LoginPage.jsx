import React, { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { RoleContext } from "./RoleContext";

function LoginPage() {
  const navigate = useNavigate();
  const { setRole } = useContext(RoleContext);

  const [selectedRole, setSelectedRole] = useState("Employee");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const response = await fetch("/api/login/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          email,
          password,
          role: selectedRole
        })
      });
      const data = await response.json();
      if (response.ok) {
        setRole(data.role);
        navigate("/dashboard");
      } else {
        setError(data.error || "Login failed");
      }
    } catch {
      setError("Network error");
    }
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
          <select value={selectedRole} onChange={e => setSelectedRole(e.target.value)}>
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
        {error && <div style={{ color: "red", marginTop: "8px" }}>{error}</div>}
      </form>
      <hr />
      <p>
        Don't have an Admin account?{" "}
        <button onClick={handleSignupClick}>Sign up as Admin</button>
      </p>
    </div>
  );
}

export default LoginPage;
