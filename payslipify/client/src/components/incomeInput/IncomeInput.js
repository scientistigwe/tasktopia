// src/components/IncomeInput.js
import React, { useState } from "react";
import axios from "axios";

const IncomeInput = () => {
  const [income, setIncome] = useState(0);
  const [date, setDate] = useState("");

  const handleSubmit = async () => {
    try {
      const response = await axios.post("http://localhost:8000/api/income", {
        user_id: 1, // Assuming user ID is 1 for simplicity
        date: date,
        income: income,
        expenses: 0,
        savings: 0,
      });
      console.log(response.data);
    } catch (error) {
      console.error("There was an error submitting the income data!", error);
    }
  };

  return (
    <div>
      <input
        type="date"
        value={date}
        onChange={(e) => setDate(e.target.value)}
      />
      <input
        type="number"
        value={income}
        onChange={(e) => setIncome(e.target.value)}
      />
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
};

export default IncomeInput;
