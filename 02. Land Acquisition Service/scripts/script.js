/**** TYPEWRITER FUNCTION ****/
//Initialize variables
const titleElement = document.getElementById("hero-text");
const text = "LandLens Marketplace";
let index = 0;

//Define 'Typewriter' function
function typeWriter() {
  if (index < text.length) {
    titleElement.textContent += text.charAt(index);
    index++;
    setTimeout(typeWriter, 500);
  } else {
    index = 0;
    titleElement.textContent = "";
    setTimeout(typeWriter, 1000);
  }
}
//Call the function
document.addEventListener("DOMContentLoaded", typeWriter);
