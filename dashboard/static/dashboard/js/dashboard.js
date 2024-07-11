const charts = {}; // Object to store chart instances

// Utility function to fetch data from the server
async function fetchData(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching data:", error);
    return null;
  }
}

// Function to update a chart based on provided data
const updateChart = (chartId, chartType, chartData, chartOptions) => {
  const canvas = document.getElementById(chartId);
  if (!canvas) {
    console.error(`Canvas element with ID ${chartId} not found.`);
    return;
  }

  const ctx = canvas.getContext("2d");

  // Destroy existing chart instance if it exists
  if (charts[chartId]) {
    charts[chartId].destroy();
  }

  // Create new chart instance
  charts[chartId] = new Chart(ctx, {
    type: chartType,
    data: chartData,
    options: chartOptions,
  });
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
      (data) => `${data.percent_overdue.toFixed(1)}%`
    ),
    updateKPICard(
      "/dashboard/percent-completed/",
      "percentCompletedValue",
      (data) => `${data.percent_completed.toFixed(1)}%`
    ),
  ]);
};

// Function to update Category Task Completion Table
const updateCategoryTaskCompletionTable = async () => {
  const data = await fetchData("/dashboard/category-wise-task-completion/");
  if (!data) return;

  const aggregatedData = {};

  data.forEach((item) => {
    let category = item.category_type;
    if (category === "other" && item.category_name) {
      category = `${category}: ${item.category_name}`;
    }

    if (!aggregatedData[category]) {
      aggregatedData[category] = {
        category,
        completed_tasks: item.completed_tasks,
        total_tasks: item.total_tasks,
      };
    } else {
      aggregatedData[category].completed_tasks += item.completed_tasks;
      aggregatedData[category].total_tasks += item.total_tasks;
    }
  });

  const tableBody = document.getElementById("categoryTaskCompletionTableBody");
  if (tableBody) {
    tableBody.innerHTML = Object.keys(aggregatedData)
      .map((category) => {
        const item = aggregatedData[category];
        const completionRate = (item.completed_tasks / item.total_tasks) * 100;
        return `
          <tr>
            <td>${category}</td>
            <td>${item.completed_tasks}</td>
            <td>${item.total_tasks}</td>
            <td>${
              isNaN(completionRate) ? "0.0" : completionRate.toFixed(1)
            }</td>
          </tr>
        `;
      })
      .join("");
  } else {
    console.error("Element with ID categoryTaskCompletionTableBody not found.");
  }
};

// Function to update Tasks Created vs Completed Chart
const updateTasksCreatedCompletedChart = async () => {
  const data = await fetchData("/dashboard/tasks-created-vs-completed/");
  if (!data) return;

  updateChart(
    "tasksCreatedCompleted",
    "doughnut",
    {
      labels: ["Tasks created", "Tasks completed"],
      datasets: [
        {
          data: [data.tasks_created, data.tasks_completed],
          backgroundColor: ["#36A2EB", "#FF6384"],
        },
      ],
    },
    {
      responsive: true,
      plugins: {
        legend: { position: "top" },
        tooltip: {
          callbacks: {
            label: (tooltipItem) => `${tooltipItem.label}: ${tooltipItem.raw}`,
          },
        },
      },
    }
  );
};

// Function to update Overdue Tasks Table
// Function to fetch and display overdue tasks
const updateOverdueTasksTable = async () => {
  try {
    const response = await fetch("/dashboard/overdue-tasks/");
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const overdueTasks = await response.json();

    const tableBody = document.getElementById("overdueTasksTableBody");
    if (tableBody) {
      tableBody.innerHTML = overdueTasks
        .map(
          (task) => `
          <tr>
          <td>${item.user_id}</td>
          <td>${item.username}</td>
          <td>${item.first_name}</td>
          <td>${item.email}</td>
          <td>${item.title}</td>
          <td>${item.status}</td>
          </tr>
        `
        )
        .join("");
    } else {
      console.error("Element with ID overdueTasksTableBody not found.");
    }
  } catch (error) {
    console.error("Error fetching or displaying overdue tasks:", error);
  }
};

// Function to update Task Completion Rate Over Time Chart
const updateTaskCompletionRateOverTimeChart = async () => {
  const data = await fetchData("/dashboard/task-completion-rate-over-time/");
  if (!data) return;

  updateChart(
    "taskCompletionRateOverTime",
    "line",
    {
      labels: data.map((item) => item.date),
      datasets: [
        {
          label: "Completion Rate",
          data: data.map((item) => item.completion_rate),
          borderColor: "#36A2EB",
          fill: false,
        },
      ],
    },
    {
      responsive: true,
      plugins: {
        legend: { position: "top" },
        title: { display: true, text: "Task Completion Rate Over Time" },
        tooltip: {
          callbacks: {
            label: (tooltipItem) => `Rate: ${tooltipItem.raw}%`,
          },
        },
      },
    }
  );
};

// Function to update Task Priority Distribution Chart
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

const updateProductivityTrendsChart = async () => {
  fetch("/dashboard/productivity-trends/")
    .then((response) => response.json())
    .then((data) => {
      const chartData = {
        labels: data.map((item) => item.date), // Use 'date' field for labels
        datasets: [
          {
            label: "Tasks Created",
            data: data.map((item) => item.total_tasks), // Use 'total_tasks' for data
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 1,
            fill: false,
          },
          {
            label: "Tasks Completed",
            data: data.map((item) => item.completed_tasks), // Use 'completed_tasks' for data
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 1,
            fill: false,
          },
          {
            label: "Completion Rate (%)",
            data: data.map((item) => item.completion_rate), // Use 'completion_rate' for data
            borderColor: "rgba(255, 206, 86, 1)",
            borderWidth: 1,
            fill: false,
          },
        ],
      };

      const chartOptions = {
        scales: {
          x: {
            type: "time",
            time: {
              unit: "day",
            },
          },
          y: {
            beginAtZero: true,
          },
        },
      };

      updateChart("productivityTrendsChart", "line", chartData, chartOptions);
    })
    .catch((error) =>
      console.error("Error updating productivity trends chart:", error)
    );
};

// Main function to refresh the entire dashboard
const refreshDashboard = async () => {
  await updateKPIs();
  await updateTasksCreatedCompletedChart();
  await updateTaskCompletionRateOverTimeChart();
  await updateTaskPriorityDistributionChart();
  await updateCategoryTaskCompletionTable();
  await updateOverdueTasksTable();
  await updateProductivityTrendsChart();
};

// Event listener for DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("analyticsInsightsMarker")) {
    console.log(
      "Analytics and Insights page detected, refreshing dashboard..."
    );
    refreshDashboard();
  } else {
    console.log("Not on Analytics and Insights page");
  }
});
