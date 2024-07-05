// Utility functions
const fetchData = async (url) => {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error("Network response was not ok");
    return await response.json();
  } catch (error) {
    console.error("Error fetching data:", error);
    return null;
  }
};

// Chart update functions
const updateChart = (elementId, chartType, data, options) => {
  const element = document.getElementById(elementId);
  if (element) {
    const ctx = element.getContext("2d");
    new Chart(ctx, { type: chartType, data, options });
  } else {
    console.error(`Element with ID ${elementId} not found.`);
  }
};

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
        title: {
          display: true,
          text: "Task Completion Rate",
        },
      },
    }
  );
};

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
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: "Task Priority Distribution",
        },
        tooltip: {
          callbacks: {
            label: function (tooltipItem) {
              return `${tooltipItem.label}: ${tooltipItem.raw}`;
            },
          },
        },
      },
    }
  );
};

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
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: "Productivity Trends Over Time",
        },
        tooltip: {
          callbacks: {
            label: function (tooltipItem) {
              return `Count: ${tooltipItem.raw}`;
            },
          },
        },
      },
    }
  );
};

// Table update functions
const updateCategoryTaskCompletionTable = async () => {
  const data = await fetchData("/dashboard/category-wise-task-completion/");
  if (!data) return;

  const tableBody = document.getElementById("categoryTaskCompletionTableBody");
  if (tableBody) {
    tableBody.innerHTML = data
      .map(
        (item) => `
    <tr>
      <td>${item.category}</td>
      <td>${item.completed_tasks}</td>
      <td>${item.total_tasks}</td>
      <td>${item.completion_rate.toFixed(1)}</td>
    </tr>
  `
      )
      .join("");
  } else {
    console.error(`Element with ID categoryTaskCompletionTableBody not found.`);
  }
};

// KPI update functions
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

const updateKPIs = async () => {
  await updateKPICard(
    "/dashboard/total-tasks/",
    "totalTasksValue",
    (data) => data.total_tasks
  );
  await updateKPICard(
    "/dashboard/percent-overdue/",
    "percentOverdueValue",
    (data) => data.percent_overdue.toFixed(1) + "%"
  );
  await updateKPICard(
    "/dashboard/percent-completed/",
    "percentCompletedValue",
    (data) => data.percent_completed.toFixed(1) + "%"
  );
};

// Event listeners
document.addEventListener("DOMContentLoaded", () => {
  refreshDashboard();
});

// Main refresh function
const refreshDashboard = () => {
  updateTaskCompletionRateChart();
  updateTaskPriorityDistributionChart();
  updateProductivityTrendsChart();
  updateCategoryTaskCompletionTable();
  updateKPIs();
};
