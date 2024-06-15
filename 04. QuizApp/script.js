const quizSection = document.getElementById("quiz-section");
let currentQuestionIndex = 0;
let score = 0;

// Example questions array
const questions = [
  {
    questionText: "What is the capital of England?",
    options: [
      { id: "a", value: "Edinburgh", text: "Edinburgh" },
      { id: "b", value: "Birmingham", text: "Birmingham" },
      { id: "c", value: "London", text: "London" },
      { id: "d", value: "Manchester", text: "Manchester" },
    ],
    correctAnswer: "c",
  },
  // Add more questions here...
];

function loadQuestion() {
  const questionElement = document.createElement("div");
  questionElement.innerHTML = `
        <h2>${questions[currentQuestionIndex].questionText}</h2>
        ${questions[currentQuestionIndex].options
          .map(
            (option) => `
            <input type="radio" id="${option.id}" name="answer" value="${option.value}">
            <label for="${option.id}">${option.text}</label><br>
        `
          )
          .join("")}
    `;
  quizSection.appendChild(questionElement);

  const nextButton = document.createElement("button");
  nextButton.textContent = "Next";
  nextButton.addEventListener("click", nextQuestion);
  quizSection.appendChild(nextButton);
}

function nextQuestion() {
  const selectedOption = document.querySelector(
    'input[name="answer"]:checked'
  ).value;
  if (selectedOption === questions[currentQuestionIndex].correctAnswer) {
    score++;
  }
  currentQuestionIndex++;
  if (currentQuestionIndex >= questions.length) {
    endQuiz();
  } else {
    quizSection.innerHTML = ""; // Clear the quiz section
    loadQuestion(); // Load the next question
  }
}

function endQuiz() {
  quizSection.innerHTML = `<h2>Quiz Complete!</h2><p>Your score: ${score}/${questions.length}</p>`;
}

loadQuestion(); // Start loading the first question
