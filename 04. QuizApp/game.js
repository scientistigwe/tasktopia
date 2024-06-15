/**
 * DEFINE ALL REQUIRED GLOBAL VARIABLES
 */
const playerLife = document.getElementById("player-life");
const opponentLife = document.getElementById("opponent-life");
const resultDiv = document.getElementById("result");
const makeMoveVar = document.querySelectorAll(".makeMove");
let healthChange;
let currentWeather = "Clear"; // Default weather

const pNameBtn = document.getElementById("p-name-btn");
let playerMove;
let opponentMove;
let playerWin;

// Use OpenWeather API to fetch weather data
const apiKey = "b5a9fa9b52af2d466adaeceb1f4aeb48";
let city = "london"; // Initialize city variable

let playerLifePoints = 100;
let opponentLifePoints = 100;

const moves = ["rock", "paper", "scissors", "spock", "lizard"];
const moveEffects = {
  rock: { wins: ["scissors", "lizard"], loses: ["paper", "spock"] },
  paper: { wins: ["rock", "spock"], loses: ["scissors", "lizard"] },
  scissors: { wins: ["paper", "lizard"], loses: ["rock", "spock"] },
  spock: { wins: ["scissors", "rock"], loses: ["paper", "lizard"] },
  lizard: { wins: ["spock", "paper"], loses: ["rock", "scissors"] },
};

const citiesByContinent = {
  Africa: [
    "Cairo",
    "Lagos",
    "Kinshasa",
    "Johannesburg",
    "Nairobi",
    "Alexandria",
    "Casablanca",
    "Durban",
    "Abuja",
    "Pretoria",
    "Luanda",
    "Khartoum",
    "Rabat",
    "Maputo",
    "Tunis",
    "Porto-Novo",
    "Accra",
    "Omdurman",
    "Conakry",
    "Gaborone",
  ],
  Asia: [
    "Tokyo",
    "Jakarta",
    "Delhi",
    "Seoul",
    "Mumbai",
    "Manila",
    "Shanghai",
    "Guangzhou",
    "Osaka",
    "Dhaka",
    "Karachi",
    "Chennai",
    "Bangkok",
    "Hyderabad",
    "Surabaya",
    "Nagoya",
    "Bandung",
    "Faisalabad",
    "Chongqing",
    "Wuhan",
  ],
  Europe: [
    "Moscow",
    "Istanbul",
    "London",
    "Berlin",
    "Madrid",
    "Paris",
    "Barcelona",
    "Rome",
    "Milan",
    "Amsterdam",
    "Vienna",
    "Prague",
    "Warsaw",
    "Athens",
    "Hamburg",
    "Budapest",
    "Brussels",
    "Stockholm",
    "Zürich",
    "Dublin",
  ],
  "North America": [
    "New York City",
    "Los Angeles",
    "Chicago",
    "Houston",
    "Philadelphia",
    "Phoenix",
    "San Antonio",
    "San Diego",
    "Dallas",
    "San Jose",
    "Indianapolis",
    "Jacksonville",
    "Austin",
    "Columbus",
    "Fort Worth",
    "Charlotte",
    "Memphis",
    "Seattle",
    "Denver",
    "Washington D.C.",
  ],
  "South America": [
    "São Paulo",
    "Lima",
    "Bogotá",
    "Caracas",
    "Medellín",
    "Quito",
    "Guayaquil",
    "Cali",
    "Recife",
    "Belém",
    "Salvador",
    "Manaus",
    "Aracaju",
    "João Pessoa",
    "Florianópolis",
    "Curitiba",
    "Goiania",
    "Campinas",
    "Vitória",
    "Natal",
  ],
};

// Define move messages
const moveMessages = {
  rock: {
    wins: {
      lizard: "Rock crushed lizard!",
      scissors: "Rock crushed scissors!",
    },
    loses: { paper: "Paper covers rock!", spock: "Spock vaporizes rock!" },
  },
  paper: {
    wins: { rock: "Paper covers rock!", spock: "Paper disproves Spock!" },
    loses: {
      scissors: "Scissors cuts paper!",
      lizard: "Lizard eats paper!",
    },
  },
  scissors: {
    wins: {
      paper: "Scissors cuts paper!",
      lizard: "Scissors decapitates lizard!",
    },
    loses: { rock: "Rock crushes scissors!", spock: "Spock smashes scissors!" },
  },
  spock: {
    wins: {
      scissors: "Spock smashes scissors!",
      rock: "Spock vaporizes rock!",
    },
    loses: {
      paper: "Paper disproves Spock!",
      lizard: "Lizard poisons Spock!",
    },
  },
  lizard: {
    wins: { paper: "Lizard eats paper!", spock: "Lizard poisons Spock!" },
    loses: {
      rock: "Rock crushes lizard!",
      scissors: "Scissors decapitates lizard!",
    },
  },
};

const continentSelect = document.getElementById("continentSelect");
const citySelect = document.getElementById("citySelect");

continentSelect.addEventListener("change", function () {
  const selectedContinent = this.value;
  const cities = citiesByContinent[selectedContinent];
  populateCityDropdown(cities);
});

function populateCityDropdown(cities) {
  citySelect.innerHTML = ""; // Clear existing options
  cities.forEach((city) => {
    const option = document.createElement("option");
    option.text = city;
    citySelect.add(option);
  });
}

// Initial population of city dropdown based on default selected continent
const defaultContinent = continentSelect.value;
const defaultCities = citiesByContinent[defaultContinent];
populateCityDropdown(defaultCities);

const weatherEffects = {
  Thunderstorm: {
    rock: { healthChange: -5, message: "This heavy rain eroded me!" },
    paper: {
      healthChange: -5,
      message: "I'm soaked and disintegrated in the rain!",
    },
    scissors: { healthChange: 5, message: "Lightning sharpened my blades!" },
    lizard: { healthChange: -5, message: "I must hide from the thunderstorm!" },
    spock: {
      healthChange: -1,
      message: "My logic is slightly influenced by the chaos.",
    },
  },
  Drizzle: {
    rock: {
      healthChange: -3,
      message: "This drizzle has little effect on me.",
    },
    paper: { healthChange: -3, message: "I'm damp and less effective." },
    scissors: {
      healthChange: -3,
      message: "This drizzle might rust me over time.",
    },
    lizard: {
      healthChange: 3,
      message: "I might come out in this light rain!",
    },
    spock: {
      healthChange: -1,
      message: "My logic is slightly influenced by the drizzle.",
    },
  },
  Rain: {
    rock: {
      healthChange: -4,
      message:
        "This rain causes some erosion, but not as bad as a thunderstorm.",
    },
    paper: { healthChange: -4, message: "I'm wet and useless in this rain." },
    scissors: {
      healthChange: -2,
      message: "This rain has a neutral or slight rusting effect on me.",
    },
    lizard: {
      healthChange: -3,
      message: "I may hide or be inactive in this rain.",
    },
    spock: {
      healthChange: -1,
      message: "My logic is slightly influenced by the rain.",
    },
  },
  Snow: {
    rock: { healthChange: -3, message: "The ice makes me slippery!" },
    paper: {
      healthChange: -6,
      message: "I'm fragile and easily torn in this snow!",
    },
    scissors: { healthChange: -4, message: "The cold makes my metal brittle." },
    lizard: {
      healthChange: -5,
      message: "I hibernate or stay inactive in the cold.",
    },
    spock: {
      healthChange: -1,
      message: "My logic is slightly influenced by the snow.",
    },
  },
  Atmosphere: {
    rock: { healthChange: -2, message: "This fog has minimal effect on me." },
    paper: { healthChange: -4, message: "I'm damp and fragile in this mist." },
    scissors: {
      healthChange: -2,
      message: "This fog doesn't impact my metal.",
    },
    lizard: { healthChange: 5, message: "I thrive in these humid conditions!" },
    spock: {
      healthChange: 1,
      message: "My logic is slightly influenced by the atmosphere.",
    },
  },
  Clear: {
    rock: {
      healthChange: 0,
      message: "These clear skies have no adverse effects on me.",
    },
    paper: { healthChange: 0, message: "These are ideal conditions for me!" },
    scissors: {
      healthChange: 0,
      message: "I'm in ideal conditions with no rust.",
    },
    lizard: { healthChange: 0, message: "I thrive in this clear weather!" },
    spock: {
      healthChange: 1,
      message: "My logic remains unaffected by the clear weather.",
    },
  },
  Clouds: {
    rock: {
      healthChange: -1,
      message: "These clouds have minimal effect on me.",
    },
    paper: {
      healthChange: -2,
      message: "The overcast skies might make me damp.",
    },
    scissors: {
      healthChange: -1,
      message: "These clouds have minimal effect on me.",
    },
    lizard: {
      healthChange: -3,
      message: "I'm less active under these clouds.",
    },
    spock: {
      healthChange: 1,
      message: "My logic is unaffected by these clouds.",
    },
  },
  Extreme: {
    rock: { healthChange: -10, message: "These extreme conditions erode me!" },
    paper: {
      healthChange: -10,
      message: "I'm easily destroyed in extreme conditions!",
    },
    scissors: {
      healthChange: -10,
      message: "These extreme conditions could rust me instantly!",
    },
    lizard: {
      healthChange: -10,
      message: "I'm endangered in these extreme conditions!",
    },
    spock: {
      healthChange: -10,
      message: "Even my logic is affected by these extremes!",
    },
  },
};

// Initialize totalMoves and movesCount
let totalMoves = 0;
let movesCount = { rock: 0, paper: 0, scissors: 0, spock: 0, lizard: 0 };

makeMoveVar.forEach((element) => element.addEventListener("click", handleMove));

/*// Event listener for the pNameBtn to set the city and update weather
pNameBtn.addEventListener("click", function () {
  city = citySelect.value;
  updateWeather(city);
});
*/

let p1WeatherInfoDivText;
let p2WeatherInfoDivText;
let p1WeatherInfoDiv;
let p2WeatherInfoDiv;

pNameBtn.addEventListener("click", function () {
  setTimeout(function () {
    p1WeatherInfoDivText =
      document.getElementById("p1-weather-info").textContent;
    p2WeatherInfoDivText =
      document.getElementById("p2-weather-info").textContent;

    p1WeatherInfoDiv = p1WeatherInfoDivText.split(": ").pop().trim();
    p2WeatherInfoDiv = p2WeatherInfoDivText.split(": ").pop().trim();
  }, 3000);
});

let profilesComplete = false;

// Event listener for player name inputs
document.getElementById("p-name-btn").addEventListener("click", function () {
  const p1Name = document.getElementById("p1-name").textContent;
  const p2Name = document.getElementById("p2-name").textContent;
  profilesComplete = p1Name && p2Name;
});

// Event listener for makeMove buttons
const buttons = document.querySelectorAll(".makeMove");
buttons.forEach((button) => {
  button.addEventListener("click", function () {
    if (!profilesComplete) {
      alert("Please complete both player profiles before making moves.");
      return;
    }
  });
});

function handleMove(event) {
  playerMove = event.target.dataset.move;
  opponentMove = moves[Math.floor(Math.random() * moves.length)];

  console.log(currentWeather);
  console.log(playerMove);
  if (playerMove) {
  } else {
  }
  console.log(currentWeather);

  let resultMessage;
  let playerHealthChange = 0;
  let opponentHealthChange = 0;

  totalMoves++; // Increment total moves
  movesCount[playerMove]++; // Update movesCount for the player move

  if (playerMove === opponentMove) {
    resultMessage = `It's a tie! You both chose ${playerMove}.`;
  } else if (moveEffects[playerMove].wins.includes(opponentMove)) {
    currentWeather = p1WeatherInfoDiv;
    resultMessage = `You win! ${
      moveMessages[playerMove].wins[opponentMove]
    }! Player 1 from ${city} wins after ${totalMoves} moves with combinations of ${formatMovesCount(
      movesCount
    )}.`;
    playerHealthChange =
      weatherEffects[currentWeather][playerMove].healthChange;
    opponentHealthChange =
      weatherEffects[currentWeather][opponentMove].healthChange;
    opponentLifePoints -= Math.max(0, 20 + opponentHealthChange);
  } else {
    currentWeather = p2WeatherInfoDiv;
    resultMessage = `You lose! ${
      moveMessages[playerMove].loses[opponentMove]
    } Player 2 wins after ${totalMoves} moves with combinations of ${formatMovesCount(
      movesCount
    )}.`;
    playerHealthChange =
      weatherEffects[currentWeather][playerMove].healthChange;
    opponentHealthChange =
      weatherEffects[currentWeather][opponentMove].healthChange;
    playerLifePoints -= Math.max(0, 20 + playerHealthChange);
  }

  // Ensure life points do not go below zero
  playerLifePoints = Math.max(0, playerLifePoints);
  opponentLifePoints = Math.max(0, opponentLifePoints);

  // Include winner's weather message in the result message
  if (playerLifePoints <= 0 || opponentLifePoints <= 0) {
    if (playerLifePoints > opponentLifePoints) {
      resultMessage += `\nWeather message of the winner: ${weatherEffects[currentWeather][playerMove].message}`;
    } else if (playerLifePoints < opponentLifePoints) {
      resultMessage += `\nWeather message of the winner: ${weatherEffects[currentWeather][opponentMove].message}`;
    }
  }

  playerLife.innerText = `Player Life: ${playerLifePoints}`;
  opponentLife.innerText = `Opponent Life: ${opponentLifePoints}`;
  resultDiv.innerText = resultMessage;
}

// Attach handleMove function to makeMove buttons
makeMoveVar.forEach((element) => element.addEventListener("click", handleMove));

function formatMovesCount(movesCount) {
  return Object.entries(movesCount)
    .filter(([move, count]) => count > 0)
    .map(([move, count]) => `${count} ${move}(s)`)
    .join(", ");
}

// Function to declare the winner of the game
function declareWinner() {
  let winnerMessage;

  if (playerLifePoints > opponentLifePoints) {
    winnerMessage = `Player from ${city} won after ${totalMoves} moves with combinations of ${formatMovesCount(
      movesCount
    )}. CONGRATULATIONS!`;
  } else if (playerLifePoints < opponentLifePoints) {
    winnerMessage = `Computer from ${city} won after ${totalMoves} moves with combinations of ${formatMovesCount(
      movesCount
    )}. BETTER LUCK NEXT TIME!`;
  } else {
    winnerMessage = "It's a draw!";
  }

  resultDiv.innerText += "\n" + winnerMessage;

  // Reset life points
  playerLifePoints = 100;
  opponentLifePoints = 100;

  // Update life points display
  playerLife.innerText = `Player Life: ${playerLifePoints}`;
  opponentLife.innerText = `Opponent Life: ${opponentLifePoints}`;

  // Disable move buttons
  disableMoves();
}

// Function to disable moves after game ends
function disableMoves() {
  makeMoveVar.forEach((moveButton) => {
    moveButton.disabled = true;
  });
}

// Function to format moves count for the result message
function formatMovesCount(movesCount) {
  return Object.entries(movesCount)
    .map(([move, count]) => `${count} ${move}${count > 1 ? "s" : ""}`)
    .join(", ");
}
