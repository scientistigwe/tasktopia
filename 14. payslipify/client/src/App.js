import React, { useState, useEffect } from "react";
import IncomeInput from "../src/components/incomeInput/IncomeInput";
import FinancialChart from "../src/components/financialChart/FinancialChart";
import axios from "axios";
import "./App.css";

const App = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("/api/financial_data");
        setData(response.data);
      } catch (error) {
        console.error("Error fetching financial data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Payslipify</h1>
      <IncomeInput />
      <FinancialChart data={data} />
    </div>
  );
};

export default App;
