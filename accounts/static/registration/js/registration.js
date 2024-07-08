// <!-- JavaScript to clear success messages with class name 'alert-message' after 5 seconds -->

// Wait for the document to load
document.addEventListener("DOMContentLoaded", function () {
  // Find all elements with class name 'alert-message'
  const alertMessages = document.getElementsByClassName("alert-message");

  // Iterate through each alert message
  Array.from(alertMessages).forEach(function (alertMessage) {
    // Set a timeout to remove each alert message after 5 seconds
    setTimeout(function () {
      alertMessage.remove(); // Remove the alert message
    }, 5000); // 5000 milliseconds = 5 seconds
  });
});
