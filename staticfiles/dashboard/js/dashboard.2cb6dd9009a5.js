// Function to fetch data from Django views
async function fetchData(url) {
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
}

// Function to update Task Completion Rate Chart
async function updateTaskCompletionRateChart() {
  const data = await fetchData("/dashboard/task-completion-rate/");
  if (!data) return;

  const ctx = document
    .getElementById("taskCompletionRateChart")
    .getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Total Tasks", "Tasks Completed", "Completion Rate"],
      datasets: [
        {
          label: "Value",
          data: [
            data.total_tasks,
            data.completed_tasks,
            data.completion_rate.toFixed(2),
          ],
          backgroundColor: [
            "rgba(75, 192, 192, 0.6)",
            "rgba(54, 162, 235, 0.6)",
            "rgba(255, 206, 86, 0.6)",
          ],
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Values",
          },
        },
      },
      responsive: true,
      plugins: {
        legend: {
          display: false, // Hide the legend
        },
        title: {
          display: true,
          text: `Task Statistics: Completion rate = ${data.completion_rate.toFixed(
            1
          )}%`,
        },
      },
      indexAxis: "y", // Plot bars vertically
      scales: {
        x: {
          title: {
            display: true,
            text: "", // No label for x-axis
          },
        },
      },
    },
  });
}

// Function to update Task Priority Distribution Chart
async function updateTaskPriorityDistributionChart() {
  const data = await fetchData("/dashboard/task-priority-distribution/");
  if (!data) return;

  const ctx = document
    .getElementById("taskPriorityDistributionChart")
    .getContext("2d");
  const labels = data.map((item) => item.priority);
  const values = data.map((item) => item.count);

  new Chart(ctx, {
    type: "pie",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Task Priority",
          data: values,
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
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: "Task Priority Distribution",
        },
      },
    },
  });
}

// Function to update Productivity Trends Chart
async function updateProductivityTrendsChart() {
  const data = await fetchData("/dashboard/productivity-trends/");
  if (!data) return;

  const x_data = data.map((item) => item.created_at__date);
  const y_data = data.map((item) => item.count);

  const ctx = document
    .getElementById("productivityTrendsChart")
    .getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels: x_data,
      datasets: [
        {
          label: "Productivity Trends",
          data: y_data,
          fill: false,
          borderColor: "rgb(75, 192, 192)",
          tension: 0.1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: "Productivity Trends",
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Date",
          },
        },
        y: {
          title: {
            display: true,
            text: "Tasks Created",
          },
        },
      },
    },
  });
}

// Function to update Category-wise Task Completion Table
async function updateCategoryTaskCompletionTable() {
  const data = await fetchData("/dashboard/category-wise-task-completion/");
  if (!data) return;

  const tableBody = document.getElementById("categoryTaskCompletionTableBody");
  tableBody.innerHTML = "";

  data.forEach((item) => {
    const row = `<tr>
                        <td>${item.category}</td>
                        <td>${item.completed_tasks}</td>
                        <td>${item.total_tasks}</td>
                        <td>${item.completion_rate.toFixed(1)}</td>
                    </tr>`;
    tableBody.insertAdjacentHTML("beforeend", row);
  });
}

// Function to update KPI cards
async function updateKPIs() {
  await updateTotalTasksCard();
  await updatePercentOverdueCard();
  await updatePercentCompletedCard();
}

// Function to update Total Tasks KPI card
async function updateTotalTasksCard() {
  const data = await fetchData("/dashboard/total-tasks/");
  if (!data) return;

  const totalTasksValue = document.getElementById("totalTasksValue");
  totalTasksValue.textContent = data.total_tasks;
}

// Function to update % Overdue KPI card
async function updatePercentOverdueCard() {
  const data = await fetchData("/dashboard/percent-overdue/");
  if (!data) return;

  const percentOverdueValue = document.getElementById("percentOverdueValue");
  percentOverdueValue.textContent = data.percent_overdue.toFixed(1) + "%";
}

// Function to update % Completed KPI card
async function updatePercentCompletedCard() {
  const data = await fetchData("/dashboard/percent-completed/");
  if (!data) return;

  const percentCompletedValue = document.getElementById(
    "percentCompletedValue"
  );
  percentCompletedValue.textContent = data.percent_completed.toFixed(1) + "%";
}

// Function to refresh all charts and tables
function refreshDashboard() {
  updateTaskCompletionRateChart();
  updateTaskPriorityDistributionChart();
  updateProductivityTrendsChart();
  updateCategoryTaskCompletionTable();
}

// Initial load of the dashboard
document.addEventListener("DOMContentLoaded", function () {
  refreshDashboard();
  updateKPIs(); // Update KPIs after initial dashboard load
});

/*
// Function to fetch data from Django views
async function fetchData(url) {
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
}

// Function to update Task Completion Rate Chart
async function updateTaskCompletionRateChart() {
  const data = await fetchData("/dashboard/task-completion-rate/");
  if (!data) return;

  const ctx = document
    .getElementById("taskCompletionRateChart")
    .getContext("2d");

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Task Statistics"], // Single label since we are showing three stats for the same category
      datasets: [
        {
          label: "Total Tasks",
          data: [data.total_tasks],
          backgroundColor: "rgba(75, 192, 192, 0.6)",
        },
        {
          label: "Tasks Completed",
          data: [data.completed_tasks],
          backgroundColor: "rgba(54, 162, 235, 0.6)",
        },
        {
          label: "Completion Rate",
          data: [data.completion_rate.toFixed(2)],
          backgroundColor: "rgba(255, 206, 86, 0.6)",
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Values",
          },
        },
      },
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: `Task Statistics: Completion rate = ${data.completion_rate.toFixed(
            2
          )}%`,
        },
      },
    },
  });
}

// Initial call to update the chart
document.addEventListener("DOMContentLoaded", function () {
  updateTaskCompletionRateChart();
});

// Function to update Task Priority Distribution Chart
async function updateTaskPriorityDistributionChart() {
  const data = await fetchData("/dashboard/task-priority-distribution/");
  if (!data) return;

  const ctx = document
    .getElementById("taskPriorityDistributionChart")
    .getContext("2d");
  const labels = data.map((item) => item.priority);
  const values = data.map((item) => item.count);

  new Chart(ctx, {
    type: "pie",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Task Priority",
          data: values,
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
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: "Task Priority Distribution",
        },
      },
    },
  });
}

// Function to update Productivity Trends Chart
async function updateProductivityTrendsChart() {
  const data = await fetchData("/dashboard/productivity-trends/");
  if (!data) return;

  const x_data = data.map((item) => item.created_at__date);
  const y_data = data.map((item) => item.count);

  const ctx = document
    .getElementById("productivityTrendsChart")
    .getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels: x_data,
      datasets: [
        {
          label: "Productivity Trends",
          data: y_data,
          fill: false,
          borderColor: "rgb(75, 192, 192)",
          tension: 0.1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: "Productivity Trends",
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Date",
          },
        },
        y: {
          title: {
            display: true,
            text: "Tasks Created",
          },
        },
      },
    },
  });
}

// Function to update Category-wise Task Completion Table
async function updateCategoryTaskCompletionTable() {
  const data = await fetchData("/dashboard/category-wise-task-completion/");
  if (!data) return;

  const tableBody = document.getElementById("categoryTaskCompletionTableBody");
  tableBody.innerHTML = "";

  data.forEach((item) => {
    const row = `<tr>
                          <td>${item.category}</td>
                          <td>${item.completed_tasks}</td>
                          <td>${item.total_tasks}</td>
                          <td>${item.completion_rate.toFixed(2)}</td>
                      </tr>`;
    tableBody.insertAdjacentHTML("beforeend", row);
  });
}

// Initial call to update the chart
document.addEventListener("DOMContentLoaded", function () {
  updateTasksCreatedVsCompletedChart();
});

// Initial call to update the chart
document.addEventListener("DOMContentLoaded", function () {
  updateTasksCreatedVsCompletedChart();
});

// Function to fetch user activity levels data from Django view
async function fetchUserActivityLevels() {
  try {
    const response = await fetch("/user-activity-levels/");
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching user activity levels:", error);
    return null;
  }
}


// Function to update User Activity Chart
async function updateUserActivityChart() {
  const data = await fetchUserActivityLevels();
  if (!data) return;

  const ctx = document.getElementById("user-activity-chart").getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.map((item) => item.user),
      datasets: [
        {
          label: "Tasks Completed",
          data: data.map((item) => item.tasks_completed),
          backgroundColor: "rgba(54, 162, 235, 0.6)",
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
        },
      },
      plugins: {
        legend: {
          display: true,
          position: "top",
        },
        title: {
          display: true,
          text: "User Activity Levels",
        },
      },
    },
  });
}

// Initial load of user activity chart
document.addEventListener("DOMContentLoaded", function () {
  updateUserActivityChart();
});

// Function to fetch filtered tasks based on filters
async function fetchFilteredTasks(filterValue) {
  try {
    const response = await fetch(`/filtered-tasks/?filter=${filterValue}`);
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching filtered tasks:", error);
    return null;
  }
}

// Event listener for filter select change
document
  .getElementById("filter-select")
  .addEventListener("change", async function () {
    const filterValue = this.value;
    const data = await fetchFilteredTasks(filterValue);
    if (!data) return;

    const filteredTasksDiv = document.getElementById("filtered-tasks");
    filteredTasksDiv.innerHTML = `<h3>Filtered Tasks (${filterValue})</h3><ul>${data
      .map((task) => `<li>${task.name}</li>`)
      .join("")}</ul>`;
  });

// Function to fetch real-time tasks data
async function fetchRealTimeTasks() {
  try {
    const response = await fetch("/real-time-tasks/");
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching real-time tasks:", error);
    return null;
  }
}

// Function to update real-time stats
function updateRealTimeStats(data) {
  const realTimeStatsDiv = document.getElementById("real-time-stats");
  realTimeStatsDiv.innerHTML = `<p>Tasks Created: ${data.create_tasks}</p><p>Tasks Completed: ${data.tasks_completed}</p>`;
}

// Interval to update real-time stats every 5 seconds
setInterval(async () => {
  const data = await fetchRealTimeTasks();
  if (data) {
    updateRealTimeStats(data);
  }
}, 5000); // Update every 5 seconds

// Function to fetch real-time tasks created count
async function fetchRealTimeTasksCreated() {
  try {
    const response = await fetch("/get-real-time-tasks-created/");
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching real-time tasks created:", error);
    return null;
  }
}

// Function to fetch real-time tasks completed count
async function fetchRealTimeTasksCompleted() {
  try {
    const response = await fetch("/get-real-time-tasks-completed/");
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching real-time tasks completed:", error);
    return null;
  }
}

// Function to refresh all charts and tables

function refreshDashboard() {
  updateTaskCompletionRateChart();
  updateTaskPriorityDistributionChart();
  updateProductivityTrendsChart();
  updateCategoryTaskCompletionTable();
  updateTasksCreatedVsCompletedChart();
  fetchUserActivityLevels();
  updateUserActivityChart();
  fetchFilteredTasks();
  fetchRealTimeTasks();
  updateRealTimeStats();
  fetchRealTimeTasksCreated();
  fetchRealTimeTasksCompleted();
}

// Initial load of the dashboard
document.addEventListener("DOMContentLoaded", function () {
  refreshDashboard();
});

// Function to fetch data from Django views
async function fetchData(url) {
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
}

// Function to update Total Tasks KPI card
async function updateTotalTasksCard() {
  const data = await fetchData("/dashboard/total-tasks/");
  if (!data) return;

  const totalTasksValue = document.getElementById("totalTasksValue");
  totalTasksValue.textContent = data.total_tasks;
}

// Function to update % Overdue KPI card
async function updatePercentOverdueCard() {
  const data = await fetchData("/dashboard/percent-overdue/");
  if (!data) return;

  const percentOverdueValue = document.getElementById("percentOverdueValue");
  percentOverdueValue.textContent = data.percent_overdue.toFixed(2) + "%";
}

// Function to update % Completed KPI card
async function updatePercentCompletedCard() {
  const data = await fetchData("/dashboard/percent-completed/");
  if (!data) return;

  const percentCompletedValue = document.getElementById(
    "percentCompletedValue"
  );
  percentCompletedValue.textContent = data.percent_completed.toFixed(2) + "%";
}

// Function to refresh all KPI cards
async function refreshKPIs() {
  await updateTotalTasksCard();
  await updatePercentOverdueCard();
  await updatePercentCompletedCard();
}

// Initial load of KPI cards
document.addEventListener("DOMContentLoaded", function () {
  refreshKPIs();
}); */
