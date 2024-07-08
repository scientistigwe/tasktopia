// Utility function to fetch data from the server
const fetchData = async (url) => {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching data:", error);
    return null;
  }
};

// Function to update a chart based on provided data
const updateChart = (elementId, chartType, data, options) => {
  const element = document.getElementById(elementId);
  if (element) {
    const ctx = element.getContext("2d");
    new Chart(ctx, { type: chartType, data, options });
  } else {
    console.error(`Element with ID ${elementId} not found.`);
  }
};

// Function to update the Task Completion Rate Chart
const updateTaskCompletionRateChart = async () => {
  const data = await fetchData("/dashboard/task-completion-rate/");
  if (!data) return;

  updateChart(
    "taskCompletionRateChart",
    "bar",
    {
      labels: ["Total Tasks", "Tasks Completed", "Completion Rate"],
      datasets: [
        {
          data: [
            data.total_tasks,
            data.completed_tasks,
            data.completion_rate.toFixed(1),
          ],
          backgroundColor: [
            "rgba(75, 192, 192, 0.6)",
            "rgba(54, 162, 235, 0.6)",
            "rgba(255, 206, 86, 0.6)",
          ],
        },
      ],
    },
    {
      responsive: true,
      plugins: {
        title: { display: true, text: "Task Completion Rate" },
      },
    }
  );
};

// Function to update the Task Priority Distribution Chart
const updateTaskPriorityDistributionChart = async () => {
  const data = await fetchData("/dashboard/task-priority-distribution/");
  if (!data) return;

  updateChart(
    "taskPriorityDistributionChart",
    "pie",
    {
      labels: data.map((item) => item.priority),
      datasets: [
        {
          label: "Task Priority",
          data: data.map((item) => item.count),
          backgroundColor: [
            "#FF6384",
            "#36A2EB",
            "#FFCE56",
            "#4BC0C0",
            "#9966FF",
          ],
        },
      ],
    },
    {
      responsive: true,
      plugins: {
        legend: { position: "top" },
        title: { display: true, text: "Task Priority Distribution" },
        tooltip: {
          callbacks: {
            label: (tooltipItem) => `${tooltipItem.label}: ${tooltipItem.raw}`,
          },
        },
      },
    }
  );
};

// Function to update the Productivity Trends Chart
const updateProductivityTrendsChart = async () => {
  const data = await fetchData("/dashboard/productivity-trends/");
  if (!data) return;

  updateChart(
    "productivityTrendsChart",
    "line",
    {
      labels: data.map((item) => item.created_at__date),
      datasets: [
        {
          label: "Productivity Trends",
          data: data.map((item) => item.count),
          fill: false,
          borderColor: "rgb(75, 192, 192)",
          tension: 0.1,
        },
      ],
    },
    {
      responsive: true,
      plugins: {
        legend: { position: "top" },
        title: { display: true, text: "Productivity Trends Over Time" },
        tooltip: {
          callbacks: {
            label: (tooltipItem) => `Count: ${tooltipItem.raw}`,
          },
        },
      },
    }
  );
};

// Function to update the Category-wise Task Completion Table
const updateCategoryTaskCompletionTable = async () => {
  const data = await fetchData(
    "/dashboard/category-wise-task-completion-summary/"
  );
  console.log(data);
  if (!data) return;

  const aggregatedData = {};

  // Aggregate data by category
  data.forEach((item) => {
    const category = item.category_name; // Use category_name as per Django response
    if (!aggregatedData[category]) {
      aggregatedData[category] = {
        category: category,
        completed_tasks: item.completed_tasks,
        total_tasks: item.total_tasks,
        completion_rate: item.completion_rate.toFixed(1),
      };
    } else {
      // Sum up values for duplicate categories
      aggregatedData[category].completed_tasks += item.completed_tasks;
      aggregatedData[category].total_tasks += item.total_tasks;
      // Recalculate completion rate based on summed values
      aggregatedData[category].completion_rate =
        (aggregatedData[category].completed_tasks /
          aggregatedData[category].total_tasks) *
        100;
    }
  });

  const tableBody = document.getElementById("categoryTaskCompletionTableBody");
  if (tableBody) {
    tableBody.innerHTML = Object.keys(aggregatedData)
      .map((category) => {
        const item = aggregatedData[category];
        return `
          <tr>
            <td>${category}</td>
            <td>${item.completed_tasks}</td>
            <td>${item.total_tasks}</td>
            <td>${item.completion_rate.toFixed(1)}</td>
          </tr>
        `;
      })
      .join("");
  } else {
    console.error(`Element with ID categoryTaskCompletionTableBody not found.`);
  }
};

// Function to update a KPI card
const updateKPICard = async (url, elementId, formatFunc) => {
  const data = await fetchData(url);
  if (!data) return;

  const element = document.getElementById(elementId);
  if (element) {
    element.textContent = formatFunc(data);
  } else {
    console.error(`Element with ID ${elementId} not found.`);
  }
};

// Function to update all KPI cards
const updateKPIs = async () => {
  await Promise.all([
    updateKPICard(
      "/dashboard/total-tasks/",
      "totalTasksValue",
      (data) => data.total_tasks
    ),
    updateKPICard(
      "/dashboard/percent-overdue/",
      "percentOverdueValue",
      (data) => data.percent_overdue.toFixed(1) + "%"
    ),
    updateKPICard(
      "/dashboard/percent-completed/",
      "percentCompletedValue",
      (data) => data.percent_completed.toFixed(1) + "%"
    ),
  ]);
};

// Main function to refresh the dashboard
const refreshDashboard = () => {
  updateTaskCompletionRateChart();
  updateTaskPriorityDistributionChart();
  updateProductivityTrendsChart();
  updateCategoryTaskCompletionTable();
  updateKPIs();
};

// Event listener for DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
  // Check if this is the analytics and insights page
  if (document.getElementById("analyticsInsightsMarker")) {
    console.log(
      "Analytics and Insights page detected, refreshing dashboard..."
    );
    refreshDashboard();
  } else {
    console.log("Not on Analytics and Insights page");
  }
});
