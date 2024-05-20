// src/App.js
import React from "react";
import IncomeInput from "../../client/src/components/incomeInput/IncomeInput";
import FinancialChart from "../src/components/financialChart/FinancialChart";

const App = () => {
  return (
    <div>
      <h1>Payslipify</h1>
      <IncomeInput />
      <FinancialChart />
    </div>
  );
};

export default App;
