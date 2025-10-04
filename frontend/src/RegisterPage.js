import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { RoleContext } from "./RoleContext";

function RegisterPage() {
  const navigate = useNavigate();
  const { setRole } = useContext(RoleContext);

  const [form, setForm] = useState({
    companyName: "",
    adminName: "",
    adminEmail: "",
    country: "",
    currency: "USD",
    password: "",
    confirmPassword: ""
  });

  const handleChange = e => {
    const { name, value } = e.target;
    setForm(f => ({ ...f, [name]: value }));
  };

  const handleSubmit = e => {
    e.preventDefault();
    // Place API call to create company and admin user here
    // On success:
    setRole("Admin");
    navigate("/dashboard");
  };

  return (
    <div>
      <h2>Admin Signup</h2>
      <form onSubmit={handleSubmit}>
        <input
          name="companyName"
          type="text"
          placeholder="Company Name"
          required
          value={form.companyName}
          onChange={handleChange}
        />
        <input
          name="adminName"
          type="text"
          placeholder="Admin Name"
          required
          value={form.adminName}
          onChange={handleChange}
        />
        <input
          name="adminEmail"
          type="email"
          placeholder="Admin Email"
          required
          value={form.adminEmail}
          onChange={handleChange}
        />
        <select name="country" required value={form.country} onChange={handleChange}>
          <option value="">Select Country</option>
          <option value="India">India</option>
          <option value="USA">USA</option>
          {/* Extend with full list or fetch from RESTcountries API */}
        </select>
        <select name="currency" required value={form.currency} onChange={handleChange}>
          <option value="USD">USD</option>
          <option value="INR">INR</option>
          <option value="EUR">EUR</option>
          {/* Extend with full currency list or fetch from API */}
        </select>
        <input
          name="password"
          type="password"
          placeholder="Password"
          required
          value={form.password}
          onChange={handleChange}
        />
        <input
          name="confirmPassword"
          type="password"
          placeholder="Confirm Password"
          required
          value={form.confirmPassword}
          onChange={handleChange}
        />
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default RegisterPage;
