$(document).ready(function () {
  var isDragging = false;
  var sidebar = $("#sidebarMenu");
  var handle = sidebar.find(".drag-handle");

  handle.on("mousedown", function (e) {
    isDragging = true;
    $("body").addClass("resizing");
  });

  $(document).on("mousemove", function (e) {
    if (isDragging) {
      var newWidth = e.clientX;
      sidebar.css("width", newWidth + "px");
    }
  });

  $(document).on("mouseup", function (e) {
    if (isDragging) {
      isDragging = false;
      $("body").removeClass("resizing");
    }
  });
});

function toggleSidebar() {
  var sidebar = document.getElementById("sidebarMenu");
  sidebar.classList.toggle("collapsed");
}

document
  .querySelector(".navbar-toggler")
  .addEventListener("click", toggleSidebar);
