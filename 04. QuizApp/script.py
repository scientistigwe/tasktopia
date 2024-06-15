


 */
  // Update move combinations
  if (player1Moves[playerMove]) {
    player1Moves[playerMove]++;
  } else {
    player1Moves[playerMove] = 1;
  }
  if (player2Moves[opponentMove]) {
    player2Moves[opponentMove]++;
  } else {
    player2Moves[opponentMove] = 1;
  }
  console.log(currentWeather);
  console.log(playerMove);

  // Define a function to calculate the health change based on the move outcome
  function calculateHealthChange(playerMove, opponentMove, currentWeather) {
    // Lookup table for determining the health change based on the move outcome
    const outcomeMap = {
      win: getWeatherMessage(currentWeather, playerMove, playerWin)
        .healthChange,
      lose: -getWeatherMessage(currentWeather, playerMove, playerWin)
        .healthChange,
      draw: 0,
    };

    // Determine the outcome ('win', 'lose', or 'draw') based on the player's move and opponent's move
    let outcome = "draw";
    if (moveEffects[playerMove].wins.includes(opponentMove)) {
      outcome = "win";
    } else if (moveEffects[playerMove].loses.includes(opponentMove)) {
      outcome = "lose";
    }

    return outcomeMap[outcome];
  }

  // Usage within the makeMove function
  const playerPoints = calculateHealthChange(
    playerMove,
    opponentMove,
    currentWeather
  );

  console.log(playerPoints);
  // Determine if the player wins based on their health change
  if (playerPoints > 0) {
    playerWin = playerPoints;
  }

  // Get move and weather messages for the player's move
  const playerMoveMessage = getMoveMessage(playerMove, opponentMove);
  const playerWeatherMessage = getWeatherMessage(
    playerMove,
    playerWin,
    p1WeatherInfoDiv,
    p2WeatherInfoDiv
  );
  // Assuming the opponent's move message is determined based on the player's move outcome
  const opponentMoveMessage = moveEffects[opponentMove].wins.includes(
    playerMove
  )
    ? moveMessages[opponentMove].wins[playerMove]
    : moveMessages[opponentMove].loses[playerMove]
    ? moveMessages[opponentMove].loses[playerMove]
    : "It's a draw";

  // Immediate feedback based on the move outcome
  if (playerPoints > 0) {
    resultDiv.textContent = `You win ${playerMoveMessage} ${playerWeatherMessage}`;
  } else if (playerPoints < 0) {
    resultDiv.textContent = `You lose ${opponentMoveMessage} ${playerWeatherMessage}`; // Displaying opponent's move message
  } else {
    resultDiv.textContent = `It's a draw Both chose ${playerMove}.`;
  }

  // Update life points display
  player1Life.textContent = player1LifePoints;
  player2Life.textContent = player2LifePoints;

  // Check if a player has won or lost
  if (player1LifePoints <= 0 || player2LifePoints <= 0) {
    declareWinner();
  }
}

function getMoveMessage(playerMove, opponentMove) {
  const playerWinMessage = moveMessages[playerMove].wins[opponentMove];
  const playerLoseMessage = moveMessages[playerMove].loses[opponentMove];

  if (playerWinMessage) {
    return playerWinMessage;
  } else if (playerLoseMessage) {
    return playerLoseMessage;
  } else {
    return "It's a draw!";
  }
}

// Function to get weather message
function fetchWeatherAndCalculateMessage(playerMove, playerWin) {
  // Extract p1WeatherInfoDiv and p2WeatherInfoDiv based on the condition
  let p1WeatherInfoDiv = document.getElementById("p1-weather-info");
  let p2WeatherInfoDiv = document.getElementById("p2-weather-info");

  if (p1WeatherInfoDiv && p1WeatherInfoDiv.innerHTML.trim() !== "") {
    fetchWeather(city, function (weather) {
      const weatherMessage = getWeatherMessage(weather, playerMove, playerWin);
      console.log(weatherMessage);
      // Use the weatherMessage as needed
    });
  }

  if (p2WeatherInfoDiv && p2WeatherInfoDiv.innerHTML.trim() !== "") {
    fetchWeather(city, function (weather) {
      const weatherMessage = getWeatherMessage(weather, playerMove, playerWin);
      console.log(weatherMessage);
      // Use the weatherMessage as needed
    });
  }
}

function declareWinner() {
  let winnerMessage = "";
  let movesText = "";

  // Create text for move combinations
  Object.entries(player1Moves).forEach(([move, count]) => {
    movesText += `${count} moves of ${move}; `;
  });

  if (player1LifePoints > player2LifePoints) {
    winnerMessage = `Player 1 from ${city} wins after ${totalMoves} moves with combinations of ${movesText}.`;
  } else if (player1LifePoints < player2LifePoints) {
    winnerMessage = `Player 2 wins after ${totalMoves} moves with combinations of ${movesText}`;
  } else {
    winnerMessage = "It's a draw!";
  }

  resultDiv.textContent = winnerMessage;
  player1LifePoints = 100;
  player2LifePoints = 100;
  player1Life.textContent = player1LifePoints;
  player2Life.textContent = player2LifePoints;

  // Reset move combinations
  player1Moves = {};
  player2Moves = {};
  totalMoves = 0;
}

function fetchWeather(city, p1WeatherInfoDiv, p2WeatherInfoDiv) {
  setTimeout(function () {
    city = city;
    p1WeatherInfoDiv = p1WeatherInfoDiv;
    p2WeatherInfoDiv = p2WeatherInfoDiv;
  }, 4000);
}


