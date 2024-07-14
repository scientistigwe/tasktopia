document.addEventListener("DOMContentLoaded", function () {
  // CATEGORY TOGGLE FUNCTION
  const categoryTypeField = document.getElementById("id_category_type");
  const otherCategoryDiv = document.getElementById("other-category");

  function toggleOtherCategory() {
    otherCategoryDiv.style.display =
      categoryTypeField.value === "other" ? "block" : "none";
  }

  if (categoryTypeField) {
    toggleOtherCategory();
    categoryTypeField.addEventListener("change", toggleOtherCategory);
  }

  // ALERT MESSAGE HANDLING
  const dismissibleMessages = document.querySelectorAll(".dismissible-message");

  function autoHideMessage(element, delay) {
    setTimeout(() => {
      if (element) element.style.display = "none";
    }, delay);
  }

  dismissibleMessages.forEach((message) => autoHideMessage(message, 5000));

  function showFormAlert(message, alertType) {
    const alertDiv = document.createElement("div");
    alertDiv.className = `alert alert-${alertType} dismissible-message`;
    alertDiv.textContent = message;

    const formElement = document.querySelector("form");
    formElement.parentNode.insertBefore(alertDiv, formElement);

    autoHideMessage(alertDiv, 5000);
  }

  const formErrors = document.querySelectorAll(".invalid-feedback");
  if (formErrors.length > 0) {
    formErrors.forEach((errorElement) => {
      showFormAlert(errorElement.textContent.trim(), "danger");
    });
  }

  // TASK COMPLETION TOGGLE
  const csrfToken = document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  ).value;
  const checkboxes = document.querySelectorAll(".form-check-input");

  checkboxes.forEach((checkbox) => {
    checkbox.checked = checkbox.dataset.status.toLowerCase() === "completed";
    checkbox.addEventListener("change", handleCheckboxChange);
  });

  function handleCheckboxChange(event) {
    const checkbox = event.target;
    const form = checkbox.closest("form");
    const isChecked = checkbox.checked;
    const taskStatus = form.dataset.status;
    const actionUrl = form.action;
    const csrfToken = document.querySelector(
      'input[name="csrfmiddlewaretoken"]'
    ).value;
    const startDate = form.dataset.startDate;
    const dueDate = form.dataset.dueDate;
    const currentDate = new Date().toISOString().split("T")[0]; // Today's date in YYYY-MM-DD format

    if (isChecked && taskStatus !== "Completed") {
      completeTask(actionUrl, new FormData(form));
    } else if (!isChecked && taskStatus === "Completed") {
      const newStatus = determineStatus(startDate, dueDate, currentDate);
      updateTaskStatus(
        actionUrl.replace("mark_completed", "update_status"),
        csrfToken,
        form,
        newStatus
      );
    } else if (isChecked && dueDate > currentDate) {
      alert(
        "You are trying to complete a task with a due date still in the future."
      );
      checkbox.checked = false;
    } else if (!isChecked) {
      const newStatus = determineStatus(startDate, dueDate, currentDate);
      updateTaskStatus(
        actionUrl.replace("mark_completed", "update_status"),
        csrfToken,
        form,
        newStatus
      );
    }
  }

  function determineStatus(startDate, dueDate, currentDate) {
    const start = new Date(startDate);
    const due = new Date(dueDate);

    if (currentDate > due) {
      return "Overdue";
    } else if (currentDate >= start && currentDate <= due) {
      return "In Progress";
    } else {
      return "Pending";
    }
  }

  function completeTask(actionUrl, formData) {
    fetch(actionUrl, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "X-Requested-With": "XMLHttpRequest",
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          location.reload();
        } else {
          alert("Error: " + data.message);
        }
      })
      .catch((error) => {
        alert("Network error: " + error.message);
      });
  }

  function updateTaskStatus(actionUrl, csrfToken, form, newStatus) {
    fetch(actionUrl, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        csrfmiddlewaretoken: csrfToken,
        status: newStatus,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          location.reload();
        } else {
          alert("Error: " + data.message);
        }
      })
      .catch((error) => {
        alert("Network error: " + error.message);
      });
  }

  function handleTaskCompletionResponse(data) {
    if (data.status === "success") {
      location.reload();
    } else {
      alert("Error: " + data.message);
    }
  }

  // Ensure the form is responsive
  const forms = document.querySelectorAll("form.form-inline");

  function toggleFormClass() {
    forms.forEach((form) => {
      if (window.innerWidth <= 768) {
        form.classList.remove("form-inline");
        form.classList.add("col-md-12");
      } else {
        form.classList.remove("col-md-12");
        form.classList.add("form-inline");
      }
    });
  }

  toggleFormClass();
  window.addEventListener("resize", toggleFormClass);
});
