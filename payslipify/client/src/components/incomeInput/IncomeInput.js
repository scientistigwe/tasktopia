// src/components/incomeInput/IncomeInput.js
import React, { useState } from "react";
import axios from "axios";

const IncomeInput = () => {
  // State for storing input values
  const [date, setDate] = useState("");
  const [income, setIncome] = useState("");
  const [selectedExpense, setSelectedExpense] = useState("");

  // Function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Send form data to backend API endpoint
      await axios.post("http://localhost:8000/api/financial_data", {
        date: date,
        income: income,
        expense: selectedExpense,
      });
      console.log("Form data submitted successfully!");
      // Clear form fields after submission
      setDate("");
      setIncome("");
      setSelectedExpense("");
    } catch (error) {
      console.error("Error submitting form data:", error);
    }
  };

  // List of possible expenses for an average citizen in the UK
  const expenseOptions = [
    "Rent/Mortgage",
    "Utilities (Electricity, Gas, Water)",
    "Transportation (Public Transit, Fuel)",
    "Food and Groceries",
    "Insurance (Health, Home, Car)",
    "Education",
    "Healthcare",
    "Entertainment",
    "Clothing",
    "Savings/Investments",
    "Debt Payments (Credit Cards, Loans)",
    "Other",
  ];

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Date:
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />
      </label>
      <label>
        Income:
        <input
          type="number"
          value={income}
          onChange={(e) => setIncome(e.target.value)}
        />
      </label>
      <label>
        Expense:
        <select
          value={selectedExpense}
          onChange={(e) => setSelectedExpense(e.target.value)}
        >
          <option value="">Select an Expense</option>
          {expenseOptions.map((expense, index) => (
            <option key={index} value={expense}>
              {expense}
            </option>
          ))}
        </select>
      </label>
      <button type="submit">Submit</button>
    </form>
  );
};

export default IncomeInput;
