const charts = {}; // Object to store chart instances

// Utility function to fetch data from the server
const fetchData = async (url) => {
  try {
    console.log(`Fetching data from ${url}`); // Log the URL
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    return null;
  }
};

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
  try {
    const data = await fetchData("/dashboard/category-wise-task-completion/");
    if (!data) return;

    const aggregatedData = {};

    // Aggregate data by category and user
    data.forEach((item) => {
      let user_id = item.user_id;
      let category = item.category_type;
      if (category === "other" && item.category_name) {
        category = `${category}: ${item.category_name}`;
      }

      if (!aggregatedData[user_id]) {
        aggregatedData[user_id] = {};
      }

      if (!aggregatedData[user_id][category]) {
        aggregatedData[user_id][category] = {
          completed_tasks: 0,
          total_tasks: 0,
          completion_rate: 0,
        };
      }

      aggregatedData[user_id][category].completed_tasks += item.completed_tasks;
      aggregatedData[user_id][category].total_tasks += item.total_tasks;
      aggregatedData[user_id][category].completion_rate =
        aggregatedData[user_id][category].total_tasks > 0
          ? (aggregatedData[user_id][category].completed_tasks /
              aggregatedData[user_id][category].total_tasks) *
            100
          : 0;
    });

    const tableBody = document.getElementById(
      "categoryTaskCompletionTableBody"
    );
    if (tableBody) {
      tableBody.innerHTML = Object.keys(aggregatedData)
        .map((user_id) => {
          return Object.keys(aggregatedData[user_id])
            .map((category) => {
              const item = aggregatedData[user_id][category];
              return `
                <tr>
                  <td>${user_id}</td>
                  <td>${category}</td>
                  <td>${item.completed_tasks}</td>
                  <td>${item.total_tasks}</td>
                  <td>${item.completion_rate.toFixed(1)}</td>
                </tr>
              `;
            })
            .join("");
        })
        .join("");
    } else {
      console.error(
        "Element with ID categoryTaskCompletionTableBody not found."
      );
    }
  } catch (error) {
    console.error("Error updating category task completion table:", error);
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
        title: { display: true, text: "Task Completed vs Task Created" },
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
const updateOverdueTasksTable = async () => {
  try {
    const overdueTasks = await fetchData("/dashboard/overdue-tasks/");
    if (!overdueTasks) return;

    const tableBody = document.getElementById("overdueTasksTableBody");
    if (tableBody) {
      tableBody.innerHTML = overdueTasks
        .map(
          (item) => `
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
  console.log("Calling updateTaskCompletionRateOverTimeChart"); // Log function call
  const data = await fetchData("/dashboard/task-completion-rate-over-time/");
  if (!data) {
    console.log("No data fetched");
    return;
  }

  console.log(`TCR: ${JSON.stringify(data)}`);

  // Validate data format
  if (
    !Array.isArray(data) ||
    !data.every((item) => "date" in item && "completion_rate" in item)
  ) {
    console.error("Invalid data format");
    return;
  }

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

// Main function to refresh the entire dashboard
const refreshDashboard = async () => {
  await updateKPIs();
  await updateTasksCreatedCompletedChart();
  await updateTaskCompletionRateOverTimeChart();
  await updateTaskPriorityDistributionChart();
  await updateCategoryTaskCompletionTable();
  await updateOverdueTasksTable();
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
