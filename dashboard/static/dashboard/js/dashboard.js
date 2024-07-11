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

// Function to update the Task Priority Bubble Charts
const updateTaskPriorityBubbleCharts = async () => {
  const data = await fetchData("/dashboard/task-priority-distribution/");
  if (!data) return;

  const priorityData = ["High", "Medium", "Low"].map((priority) => {
    const priorityItem = data.find((item) => item.priority === priority);
    return {
      data: priorityItem,
      elementId: `${priority.toLowerCase()}PriorityChart`,
      backgroundColor: `rgba(${
        priority === "High"
          ? "255, 99, 132"
          : priority === "Medium"
          ? "255, 206, 86"
          : "75, 192, 192"
      }, 0.2)`,
      borderColor: `rgba(${
        priority === "High"
          ? "255, 99, 132"
          : priority === "Medium"
          ? "255, 206, 86"
          : "75, 192, 192"
      }, 1)`,
    };
  });

  priorityData.forEach(({ data, elementId, backgroundColor, borderColor }) => {
    if (data) {
      updateChart(
        elementId,
        "bubble",
        {
          datasets: [
            {
              label: `${data.priority} Priority`,
              data: [{ x: 1, y: data.count, r: 20 }],
              backgroundColor,
              borderColor,
              borderWidth: 1,
            },
          ],
        },
        {
          scales: {
            x: { display: false },
            y: { beginAtZero: true, max: 100 },
          },
          plugins: { legend: { display: false } },
        }
      );
    }
  });
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

const updateCategoryTaskCompletionTable = async () => {
  try {
    const data = await fetchData("/dashboard/category-wise-task-completion/");
    console.log(data);
    if (!data) return;

    const aggregatedData = {};

    // Aggregate data by category
    data.forEach((item) => {
      let category = item.category_type;
      if (category === "other" && item.category_name) {
        category = `${category}: ${item.category_name}`;
      }

      if (!aggregatedData[category]) {
        aggregatedData[category] = {
          category: category,
          completed_tasks: item.completed_tasks,
          total_tasks: item.total_tasks,
          completion_rate: 0.0, // Initialize completion_rate
        };
      } else {
        // Sum up values for duplicate categories
        aggregatedData[category].completed_tasks += item.completed_tasks;
        aggregatedData[category].total_tasks += item.total_tasks;
      }
    });

    // Calculate completion rate and format the table rows
    const tableBody = document.getElementById(
      "categoryTaskCompletionTableBody"
    );
    if (tableBody) {
      tableBody.innerHTML = Object.keys(aggregatedData)
        .map((category) => {
          const item = aggregatedData[category];
          const completionRate =
            (item.completed_tasks / item.total_tasks) * 100;
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
      console.error(
        `Element with ID categoryTaskCompletionTableBody not found.`
      );
    }
  } catch (error) {
    console.error("Error fetching or processing data:", error);
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

// Function to update the Overdue Tasks Chart
const updateOverdueTasksChart = async () => {
  const data = await fetchData("/dashboard/overdue-tasks/");
  if (!data) return;

  updateChart(
    "overdueTasks",
    "doughnut",
    {
      labels: data.map((item) => item.task_name),
      datasets: [
        {
          data: data.map((item) => item.overdue_percent),
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
        tooltip: {
          callbacks: {
            label: (tooltipItem) => `${tooltipItem.label}: ${tooltipItem.raw}%`,
          },
        },
      },
    }
  );
};

// Function to update the Task Completion Rate Over Time Chart
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

// Function to update the Tasks Created vs Completed Chart
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

// Main function to refresh the entire dashboard
const refreshDashboard = async () => {
  updateKPIs();
  updateTaskCompletionRateChart();
  updateCategoryTaskCompletionTable();
  updateTasksCreatedCompletedChart();

  updateTaskPriorityBubbleCharts();
  updateProductivityTrendsChart();
  updateOverdueTasksChart();
  updateTaskCompletionRateOverTimeChart();
  updateTaskPriorityDistributionChart();
  updateProductivityTrendsChart();
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
