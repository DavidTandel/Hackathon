import React, { useState } from "react";
function ExpenseSubmission() {
  const [formData, setFormData] = useState({
    amount: "",
    currency: "USD",
    category: "",
    date: "",
    description: "",
    receipt: null,
  });

  const handleChange = e => {
    const { name, value, files } = e.target;
    setFormData(f =>
      ({ ...f, [name]: files ? files[0] : value })
    );
  };

  const handleSubmit = e => {
    e.preventDefault();
    // Submit logic, API calls/reserve logic
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Submit Expense</h2>
      <input name="amount" type="number" placeholder="Amount" required onChange={handleChange} />
      <select name="currency" onChange={handleChange}>
        {/* Example currencies */}
        <option value="USD">USD</option>
        <option value="INR">INR</option>
      </select>
      <input name="category" type="text" placeholder="Category" onChange={handleChange} />
      <input name="date" type="date" onChange={handleChange} />
      <textarea name="description" placeholder="Description" onChange={handleChange} />
      <input name="receipt" type="file" accept="image/*" onChange={handleChange} />
      <button type="submit">Submit</button>
    </form>
  );
}
export default ExpenseSubmission;
