// $(document).ready(function () {
//   // Function to get the CSRF token from the meta tag
//   function getCSRFToken() {
//     return $('meta[name="csrf-token"]').attr("content");
//   }

//   // Initialize checkbox state based on data-status attribute
//   $(".form-check-input").each(function () {
//     var status = $(this).data("status");
//     if (status.toLowerCase() === "completed") {
//       $(this).prop("checked", true);
//     }
//   });

//   // Handle checkbox change event
//   $(".form-check-input").on("change", function (event) {
//     var isChecked = $(this).is(":checked");
//     var form = $(this).closest("form");
//     var taskStatus = form.data("status");
//     var csrftoken = getCSRFToken();

//     if (
//       (isChecked && taskStatus !== "completed") ||
//       (!isChecked && taskStatus === "completed")
//     ) {
//       $.ajax({
//         url: form.attr("action"), // URL for form submission
//         type: "POST",
//         data: form.serialize(), // Serialize form data
//         dataType: "json",
//         beforeSend: function (xhr, settings) {
//           xhr.setRequestHeader("X-CSRFToken", csrftoken); // Include CSRF token
//         },
//         success: function (response) {
//           if (response.status === "success") {
//             // Optionally, refresh the task list or show a success message
//             location.reload();
//           } else {
//             // Handle error response
//             alert("Error: " + response.message);
//           }
//         },
//         error: function (jqXHR, textStatus, errorThrown) {
//           // Handle network errors
//           alert("Network error: " + textStatus);
//         },
//       });
//     } else {
//       event.preventDefault();
//     }
//   });
// });
