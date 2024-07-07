document.addEventListener("DOMContentLoaded", function () {
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

    // Initial check on page load
    toggleOtherCategory();

    // Event listener for category select change
    categorySelect.addEventListener("change", toggleOtherCategory);
  } else {
    console.log("Not on Tasks creation page");
  }

  // 2. ALERT MESSAGE HANDLING FUNCTION
  // Function to handle cancel action
  function cancelMessage(event) {
    const successMessage = event.target.closest(".dismissible-message");
    successMessage.style.display = "none";
  }

  // Function to automatically hide messages after a delay
  function autoHideMessage(element, delay) {
    setTimeout(function () {
      if (element) {
        element.style.display = "none";
      }
    }, delay);
  }

  // Automatically hide all dismissible messages after 5 seconds
  const dismissibleMessages = document.querySelectorAll(".dismissible-message");
  dismissibleMessages.forEach(function (message) {
    autoHideMessage(message, 5000); // 5000 milliseconds = 5 seconds
  });

  // Function to show alert based on form validation errors
  function showFormAlert(message, alertType) {
    // Create alert element
    var alertDiv = document.createElement("div");
    alertDiv.className = "alert alert-" + alertType + " dismissible-message";
    alertDiv.textContent = message;

    // Insert alert before the form
    var formElement = document.querySelector("form");
    formElement.parentNode.insertBefore(alertDiv, formElement);

    // Set timeout to remove alert after 5 seconds (adjust as needed)
    autoHideMessage(alertDiv, 5000); // 5000 milliseconds = 5 seconds
  }

  // Check if there are any form errors when the page loads
  var formErrors = document.querySelectorAll(".invalid-feedback");
  if (formErrors.length > 0) {
    formErrors.forEach(function (errorElement) {
      showFormAlert(errorElement.textContent.trim(), "danger");
    });
  }
});
