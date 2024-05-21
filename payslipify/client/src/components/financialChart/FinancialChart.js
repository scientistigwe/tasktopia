import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import * as d3 from "d3";

const FinancialChart = () => {
  const [financialData, setFinancialData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8000/api/financial_data"
        );
        setFinancialData(response.data);
      } catch (error) {
        console.error("Error fetching financial data:", error);
      }
    };

    fetchData();
  }, []);

  const ref = useRef();

  useEffect(() => {
    if (financialData && financialData.length > 0) {
      const svg = d3.select(ref.current);
      svg.selectAll("*").remove(); // Clear previous render

      const margin = { top: 20, right: 30, bottom: 30, left: 40 },
        width = 800 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

      const x = d3
        .scaleTime()
        .domain(d3.extent(financialData, (d) => new Date(d.date)))
        .range([0, width]);

      const y = d3
        .scaleLinear()
        .domain([0, d3.max(financialData, (d) => d.income)])
        .nice()
        .range([height, 0]);

      const line = d3
        .line()
        .x((d) => x(new Date(d.date)))
        .y((d) => y(d.income));

      const svgContent = svg
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

      svgContent
        .append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x));

      svgContent.append("g").call(d3.axisLeft(y));

      svgContent
        .append("path")
        .datum(financialData)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1.5)
        .attr("d", line);

      svgContent
        .selectAll("dot")
        .data(financialData)
        .enter()
        .append("circle")
        .attr("r", 5)
        .attr("cx", (d) => x(new Date(d.date)))
        .attr("cy", (d) => y(d.income))
        .attr("fill", "steelblue");
    }
  }, [financialData]);

  return <svg ref={ref}></svg>;
};

export default FinancialChart;
