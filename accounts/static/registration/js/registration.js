// ALERT MESSAGE HANDLING
document.addEventListener("DOMContentLoaded", function () {
  function autoHideMessage(element, delay) {
    setTimeout(function () {
      if (element && element.classList.contains("dismissible-message")) {
        element.remove(); // Remove the element from the DOM
      }
    }, delay);
  }

  function showErrorAlert(message) {
    const alertDiv = document.createElement("div");
    alertDiv.className = "alert alert-danger dismissible-message";
    alertDiv.textContent = message;

    const formElement = document.querySelector("form");
    formElement.parentNode.insertBefore(alertDiv, formElement);

    autoHideMessage(alertDiv, 5000);
  }

  function showFormAlert(message, alertType) {
    const alertDiv = document.createElement("div");
    alertDiv.className = "alert alert-" + alertType + " dismissible-message";
    alertDiv.textContent = message;

    const formElement = document.querySelector("form");
    formElement.parentNode.insertBefore(alertDiv, formElement);

    autoHideMessage(alertDiv, 5000);

    // Clear session message after displaying it
    clearSessionMessage(alertDiv);
  }

  function clearSessionMessage(alertDiv) {
    const messageKey = alertDiv.getAttribute("data-message-key");
    if (messageKey) {
      console.log(`Clearing session message '${messageKey}'...`);

      fetch("/clear_message/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
            .value,
        },
        body: JSON.stringify({ message_key: messageKey }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          console.log(`Session message '${messageKey}' cleared.`);
        })
        .catch((error) => {
          console.error(
            `Error clearing session message '${messageKey}':`,
            error
          );
          showErrorAlert(
            `Failed to clear session message. Please try again later.`
          ); // Show error to the user
        });
    }
  }

  const dismissibleMessages = document.querySelectorAll(".dismissible-message");
  dismissibleMessages.forEach(function (message) {
    autoHideMessage(message, 5000);
  });

  const formErrors = document.querySelectorAll(".invalid-feedback");
  if (formErrors.length > 0) {
    formErrors.forEach(function (errorElement) {
      showFormAlert(errorElement.textContent.trim(), "danger");
    });
  }

  const bodyElement = document.body;
  const messages = {
    login_success: bodyElement.getAttribute("data-login-success"),
    login_error: bodyElement.getAttribute("data-login-error"),
    signup_success: bodyElement.getAttribute("data-signup-success"),
    signup_error: bodyElement.getAttribute("data-signup-error"),
    task_create_success: bodyElement.getAttribute("data-task-create-success"),
    task_create_error: bodyElement.getAttribute("data-task-create-error"),
    // Add other session messages as needed
  };

  for (let key in messages) {
    if (messages[key]) {
      const alertType = key.includes("error") ? "danger" : "success";
      showFormAlert(messages[key], alertType);
    }
  }
});
