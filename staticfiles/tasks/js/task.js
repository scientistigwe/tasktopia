document.addEventListener("DOMContentLoaded", function () {
  // CATEGORY TOGGLE FUNCTION
  const categorySelect = document.querySelector('select[name="category_type"]');
  const otherCategoryDiv = document.getElementById("other-category");

  function toggleOtherCategory() {
    const selectedCategory = categorySelect.value;
    if (selectedCategory === "other") {
      otherCategoryDiv.style.display = "block";
    } else {
      otherCategoryDiv.style.display = "none";
    }
  }

  if (document.getElementById("toggleFunction")) {
    console.log("Task creation page detected!");
    toggleOtherCategory();
    categorySelect.addEventListener("change", toggleOtherCategory);
  } else {
    console.log("Not on Tasks creation page");
  }

  // ALERT MESSAGE HANDLING
  function cancelMessage(event) {
    const successMessage = event.target.closest(".dismissible-message");
    successMessage.style.display = "none";
  }

  function autoHideMessage(element, delay) {
    setTimeout(function () {
      if (element) {
        element.style.display = "none";
      }
    }, delay);
  }

  const dismissibleMessages = document.querySelectorAll(".dismissible-message");
  dismissibleMessages.forEach(function (message) {
    autoHideMessage(message, 5000); // 5000 milliseconds = 5 seconds
  });

  function showFormAlert(message, alertType) {
    const alertDiv = document.createElement("div");
    alertDiv.className = "alert alert-" + alertType + " dismissible-message";
    alertDiv.textContent = message;

    const formElement = document.querySelector("form");
    formElement.parentNode.insertBefore(alertDiv, formElement);

    autoHideMessage(alertDiv, 5000);
  }

  const formErrors = document.querySelectorAll(".invalid-feedback");
  if (formErrors.length > 0) {
    formErrors.forEach(function (errorElement) {
      showFormAlert(errorElement.textContent.trim(), "danger");
    });
  }

  // TASK COMPLETION TOGGLE
  function getCSRFToken() {
    return document
      .querySelector('meta[name="csrf-token"]')
      .getAttribute("content");
  }

  function initializeCheckbox() {
    const checkboxes = document.querySelectorAll(".form-check-input");
    checkboxes.forEach(function (checkbox) {
      const status = checkbox.dataset.status;
      checkbox.checked = status.toLowerCase() === "completed";
    });
  }

  function getCurrentDate() {
    return new Date().toISOString().split("T")[0]; // YYYY-MM-DD
  }

  function showAlert(message) {
    alert(message);
  }

  function determineStatus(startDate, dueDate) {
    const currentDate = getCurrentDate();
    if (currentDate > dueDate) {
      return "overdue";
    } else if (currentDate >= startDate && currentDate <= dueDate) {
      return "in progress";
    } else {
      return "pending";
    }
  }

  function handleCheckboxChange(event) {
    const checkbox = event.target;
    const isChecked = checkbox.checked;
    const form = checkbox.closest("form");
    const taskStatus = form.dataset.status;
    const csrftoken = getCSRFToken();
    const startDate = form.dataset.startDate;
    const dueDate = form.dataset.dueDate;
    const currentDate = getCurrentDate();

    if (isChecked && dueDate > currentDate) {
      showAlert(
        "You are trying to complete a task with a due date still in the future."
      );
      event.preventDefault();
      return;
    }

    if (
      (isChecked && taskStatus !== "completed") ||
      (!isChecked && taskStatus === "completed")
    ) {
      $.ajax({
        url: form.action,
        type: "POST",
        data: $(form).serialize(),
        dataType: "json",
        beforeSend: function (xhr) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (response) {
          if (response.status === "success") {
            location.reload();
          } else {
            alert("Error: " + response.message);
          }
        },
        error: function (jqXHR, textStatus) {
          alert("Network error: " + textStatus);
        },
      });
    } else if (!isChecked) {
      const newStatus = determineStatus(startDate, dueDate);
      form.dataset.status = newStatus;

      $.ajax({
        url: form.action.replace("mark_completed", "update_status"),
        type: "POST",
        data: {
          csrfmiddlewaretoken: csrftoken,
          status: newStatus,
        },
        dataType: "json",
        beforeSend: function (xhr) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (response) {
          if (response.status === "success") {
            location.reload();
          } else {
            alert("Error: " + response.message);
          }
        },
        error: function (jqXHR, textStatus) {
          alert("Network error: " + textStatus);
        },
      });
    }
  }

  initializeCheckbox();
  document.querySelectorAll(".form-check-input").forEach(function (checkbox) {
    checkbox.addEventListener("change", handleCheckboxChange);
  });

  // Ensure the form is responsive
  const forms = document.querySelectorAll("form.form-inline");
  forms.forEach(function (form) {
    if (window.innerWidth <= 768) {
      form.classList.remove("form-inline");
      form.classList.add("col-md-12");
    }
  });

  window.addEventListener("resize", function () {
    forms.forEach(function (form) {
      if (window.innerWidth <= 768) {
        form.classList.remove("form-inline");
        form.classList.add("col-md-12");
      } else {
        form.classList.remove("col-md-12");
        form.classList.add("form-inline");
      }
    });
  });
});
