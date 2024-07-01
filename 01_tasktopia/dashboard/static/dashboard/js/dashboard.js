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
  const ctx = document.getElementById(elementId).getContext("2d");
  new Chart(ctx, { type: chartType, data, options });
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
          label: "Value",
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
      // ... (chart options)
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
      // ... (chart options)
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
      // ... (chart options)
    }
  );
};

const updateUserActivityChart = async () => {
  const data = await fetchData("/dashboard/user-activity-levels/");
  if (!data) return;

  updateChart(
    "user-activity-chart",
    "bar",
    {
      labels: data.map((item) => item.user),
      datasets: [
        {
          label: "Tasks Completed",
          data: data.map((item) => item.tasks_completed),
          backgroundColor: "rgba(54, 162, 235, 0.6)",
        },
      ],
    },
    {
      // ... (chart options)
    }
  );
};

// Table update functions
const updateCategoryTaskCompletionTable = async () => {
  const data = await fetchData("/dashboard/category-wise-task-completion/");
  if (!data) return;

  const tableBody = document.getElementById("categoryTaskCompletionTableBody");
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
};

// KPI update functions
const updateKPICard = async (url, elementId, formatFunc) => {
  const data = await fetchData(url);
  if (!data) return;
  document.getElementById(elementId).textContent = formatFunc(data);
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
  document
    .getElementById("filter-select")
    .addEventListener("change", (e) => updateFilteredTasks(e.target.value));
});

// Main refresh function
const refreshDashboard = () => {
  updateTaskCompletionRateChart();
  updateTaskPriorityDistributionChart();
  updateProductivityTrendsChart();
  updateCategoryTaskCompletionTable();
  updateUserActivityChart();
  updateKPIs();
  updateRealTimeStats();
};
