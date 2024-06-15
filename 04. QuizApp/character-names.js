const celebritiesByCity = {
  Africa: {
    Cairo: [
      "Tamer Hosny",
      "Mohamed Salah",
      "Sherine Abdel Wahab",
      "Yasmine Sabri",
    ],
    Lagos: ["Davido", "Wizkid", "Genevieve Nnaji", "Tiwa Savage"],
    Kinshasa: ["Fally Ipupa", "Papa Wemba", "Marie Daulne", "Barbara Kanam"],
    Johannesburg: [
      "Trevor Noah",
      "AB de Villiers",
      "Charlize Theron",
      "Pearl Thusi",
    ],
    Nairobi: [
      "Lupita Nyong'o",
      "Edi Gathegi",
      "Ngũgĩ wa Thiong'o",
      "Victoria Kimani",
    ],
    Alexandria: ["Amr Diab", "Mohamed Elneny", "Laila Eloui", "Dorra Zarrouk"],
    Casablanca: [
      "Saad Lamjarred",
      "Amine Harit",
      "Asmaa Lamnawar",
      "Samira Said",
    ],
    Durban: ["Black Coffee", "Shaun Pollock", "Lira", "Minnie Dlamini"],
    Abuja: [
      "Yemi Alade",
      "P-Square (Peter and Paul Okoye)",
      "Chimamanda Ngozi Adichie",
      "Nneka",
    ],
    Pretoria: [
      "Oscar Pistorius",
      "Faf du Plessis",
      "Karen Zoid",
      "Connie Ferguson",
    ],
    Luanda: ["Anselmo Ralph", "Gelson Dala", "Yola Semedo", "Neide Van-Dúnem"],
    Khartoum: [
      "Mohamed Wardi",
      "Abdel Karim Al Kabli",
      "Nancy Ajaj",
      "Rasha Sheikh Eldin",
    ],
    Rabat: ["RedOne", "Ahmed Soultan", "Manal Benchlikha", "Samira Said"],
    Maputo: ["Stewart Sukuma", "Nelson Neves", "Mingas", "Euridice Jeque"],
    Tunis: ["Dhafer L'Abidine", "Lotfi Bouchnak", "Hend Sabry", "Latifa"],
    "Porto-Novo": [
      "Angélique Kidjo",
      "Sessimè",
      "Olivier Verdon",
      "Stanley Djougla",
    ],
    Accra: ["Michael Essien", "Sarkodie", "Jackie Appiah", "Yvonne Nelson"],
    Omdurman: [
      "Tarig Hilal",
      "Yousif Kuwa Mekki",
      "Sudanese queens",
      "Salma El Hassan",
    ],
    Conakry: [
      "Mory Kanté",
      "Sory Kandia Kouyaté",
      "Miriam Makeba",
      "N'Faly Kouyaté",
    ],
    Gaborone: [
      "Vee Mampeezy",
      "Kaone Kario",
      "Samantha Mogwe",
      "Thato Sikwane (DJ Fresh)",
    ],
  },
  Asia: {
    Tokyo: [
      "Takeshi Kitano",
      "Keisuke Honda",
      "Ayumi Hamasaki",
      "Rinko Kikuchi",
    ],
    Jakarta: ["Agnez Mo", "Raisa Andriana", "Iko Uwais", "Nicholas Saputra"],
    Delhi: ["Virat Kohli", "Ranbir Kapoor", "Priyanka Chopra", "Sonam Kapoor"],
    Seoul: ["PSY", "Lee Min-ho", "Kim Tae-hee", "IU (Lee Ji-eun)"],
    Mumbai: ["Shah Rukh Khan", "Salman Khan", "Deepika Padukone", "Alia Bhatt"],
    Manila: ["Manny Pacquiao", "Alden Richards", "Lea Salonga", "Anne Curtis"],
    Shanghai: ["Jay Chou", "Huang Xiaoming", "Fan Bingbing", "Zhou Xun"],
    Guangzhou: ["Jiro Wang", "William Chan", "Liu Yifei", "Huang Shengyi"],
    Osaka: ["Naomi Osaka", "Takashi Miike", "Aya Ueto", "Yuji Naka"],
    Dhaka: [
      "Tahsan Rahman Khan",
      "Shakib Al Hasan",
      "Jaya Ahsan",
      "Mim Bidya Sinha Saha",
    ],
    Karachi: ["Atif Aslam", "Fawad Khan", "Mahira Khan", "Saba Qamar"],
    Chennai: ["Rajinikanth", "Vijay", "Nayanthara", "Trisha Krishnan"],
    Bangkok: [
      "Mario Maurer",
      "Nadech Kugimiya",
      "Aum Patcharapa",
      "Yaya Urassaya Sperbund",
    ],
    Hyderabad: [
      "Mahesh Babu",
      "N. T. Rama Rao Jr.",
      "Samantha Akkineni",
      "Anushka Shetty",
    ],
    Surabaya: ["Tulus", "Reza Rahadian", "Rossa", "Bunga Citra Lestari"],
    Nagoya: ["Yuki Kashiwagi", "Sho Sakurai", "Masami Nagasawa", "Koji Kondo"],
    Bandung: [
      "Afgan Syahreza",
      "Ridwan Kamil",
      "Gita Gutawa",
      "Raisa Andriana",
    ],
    Faisalabad: [
      "Rahat Fateh Ali Khan",
      "Moin Akhter",
      "Meesha Shafi",
      "Noor Jehan",
    ],
    Chongqing: ["Zhao Liying", "Zhang Yixing (Lay)", "Liu Tao", "Chen Sicheng"],
    Wuhan: ["Li Na", "Han Han", "Zhao Wei", "Hu Ge"],
  },
  Europe: {
    Moscow: [
      "Sergey Lazarev",
      "Fyodor Smolov",
      "Anna Netrebko",
      "Maria Sharapova",
    ],
    Istanbul: ["Tarkan", "Arda Turan", "Beren Saat", "Elçin Sangu"],
    London: ["David Beckham", "Benedict Cumberbatch", "Emma Watson", "Adele"],
    Berlin: ["Til Schweiger", "Manuel Neuer", "Diane Kruger", "Nina Hoss"],
    Madrid: [
      "Penélope Cruz",
      "Enrique Iglesias",
      "Sergio Ramos",
      "Elsa Pataky",
    ],
    Paris: ["Omar Sy", "Kylian Mbappé", "Marion Cotillard", "Carla Bruni"],
    Barcelona: ["Gerard Piqué", "Jordi Alba", "Shakira", "Aitana"],
    Rome: [
      "Francesco Totti",
      "Claudio Baglioni",
      "Monica Bellucci",
      "Laura Pausini",
    ],
    Milan: [
      "Eros Ramazzotti",
      "Alessandro Del Piero",
      "Valentina Lodovini",
      "Elisabetta Canalis",
    ],
    Amsterdam: [
      "Armin van Buuren",
      "Virgil van Dijk",
      "Famke Janssen",
      "Carice van Houten",
    ],
    Vienna: [
      "Christoph Waltz",
      "David Alaba",
      "Conchita Wurst",
      "Senta Berger",
    ],
    Prague: [
      "Milan Kundera",
      "Petr Čech",
      "Eva Herzigová",
      "Martina Navratilova",
    ],
    Warsaw: [
      "Robert Lewandowski",
      "Zbigniew Preisner",
      "Joanna Kulig",
      "Anja Rubik",
    ],
    Athens: [
      "Stamatis Kokotas",
      "Nikos Vertis",
      "Nana Mouskouri",
      "Maria Callas",
    ],
    Hamburg: [
      "Udo Lindenberg",
      "Hannes Jaenicke",
      "Jasmin Wagner",
      "Helene Fischer",
    ],
    Budapest: ["Gábor Király", "Péter Eötvös", "Zsa Zsa Gabor", "Eva Gabor"],
    Brussels: [
      "Jean-Claude Van Damme",
      "Axel Witsel",
      "Cécile de France",
      "Annie Cordy",
    ],
    Munich: [
      "Thomas Müller",
      "Helene Fischer",
      "Lisa Martinek",
      "Michael 'Bully' Herbig",
    ],
    Sofia: [
      "Nina Dobrev",
      "Hristo Stoichkov",
      "Maria Bakalova",
      "Grigor Dimitrov",
    ],
    Copenhagen: [
      "Mads Mikkelsen",
      "Nikolaj Coster-Waldau",
      "Scarlett Johansson",
      "Viggo Mortensen",
    ],
  },
  "North America": {
    "New York": ["Beyoncé", "Robert De Niro", "Jennifer Lopez", "Jay-Z"],
    "Los Angeles": [
      "Leonardo DiCaprio",
      "Will Smith",
      "Angelina Jolie",
      "Katy Perry",
    ],
    Chicago: [
      "Kanye West",
      "Michelle Obama",
      "Harrison Ford",
      "Jennifer Hudson",
    ],
    Houston: ["Beyoncé", "Jim Parsons", "Hilary Duff", "Travis Scott"],
    Toronto: ["Drake", "Keanu Reeves", "Shawn Mendes", "Rachel McAdams"],
    "Mexico City": [
      "Salma Hayek",
      "Diego Luna",
      "Gael García Bernal",
      "Eiza González",
    ],
    Philadelphia: ["Bradley Cooper", "Will Smith", "Kevin Hart", "Pink"],
    Miami: ["Pitbull", "Camila Cabello", "Enrique Iglesias", "Gloria Estefan"],
    Atlanta: ["Kanye West", "Tyler Perry", "Julia Roberts", "Jeff Foxworthy"],
    Montreal: ["Céline Dion", "William Shatner", "Ellen Page", "Leonard Cohen"],
    Vancouver: [
      "Ryan Reynolds",
      "Michael J. Fox",
      "Seth Rogen",
      "Cobie Smulders",
    ],
    "San Francisco": [
      "Robin Williams",
      "Tom Hanks",
      "Bruce Lee",
      "Clint Eastwood",
    ],
    Boston: ["Mark Wahlberg", "Ben Affleck", "Chris Evans", "Matt Damon"],
    "Las Vegas": [
      "Celine Dion",
      "Britney Spears",
      "Wayne Newton",
      "Siegfried & Roy",
    ],
    Washington: [
      "Dave Chappelle",
      "Samuel L. Jackson",
      "Bill Nye",
      "Wanda Sykes",
    ],
    Dallas: ["Owen Wilson", "Selena Gomez", "Robin Wright", "Kelly Clarkson"],
    Orlando: ["Carrot Top", "Wayne Brady", "Johnny Depp", "Joey Fatone"],
    Detroit: ["Eminem", "Diana Ross", "Stevie Wonder", "Aretha Franklin"],
    Minneapolis: ["Prince", "Bob Dylan", "Judy Garland", "Winona Ryder"],
    Tampa: ["Hulk Hogan", "Aaron Carter", "Sarah Paulson", "Nick Carter"],
  },
  "South America": {
    "São Paulo": ["Neymar", "Gisele Bündchen", "Pelé", "Alessandra Ambrosio"],
    "Buenos Aires": [
      "Lionel Messi",
      "Juan Martín del Potro",
      "Eva Perón",
      "Lali Espósito",
    ],
    "Rio de Janeiro": [
      "Anitta",
      "Adriana Lima",
      "Vinícius Júnior",
      "Gilberto Gil",
    ],
    Bogotá: ["Shakira", "Sofía Vergara", "Juanes", "Carlos Vives"],
    Lima: [
      "Gian Marco",
      "Carlos Alcántara",
      "Claudia Llosa",
      "Nathalie Kelley",
    ],
    Santiago: ["Alexis Sánchez", "Pablo Neruda", "Mon Laferte", "Pedro Pascal"],
    Caracas: ["Simón Bolívar", "Gustavo Dudamel", "Miguel Cabrera", "Karina"],
    Brasília: [
      "Michel Teló",
      "Maria Ribeiro",
      "Marcos Palmeira",
      "Paolla Oliveira",
    ],
    Quito: [
      "María Teresa Guerrero",
      "Jonathan González",
      "María Isabel Urrutia",
      "Jonathan Estrada",
    ],
    Montevideo: [
      "Luis Suárez",
      "Jorge Drexler",
      "Natalia Oreiro",
      "Enzo Francescoli",
    ],
    "La Paz": [
      "Marco Antonio Etcheverry",
      "María Fernanda Álvarez",
      "David Mondaca",
      "Willy Claure",
    ],
    Georgetown: [
      "Eddy Grant",
      "Shakira Caine",
      "Nikita Mandryka",
      "Claudette Colvin",
    ],
    Asunción: [
      "Larissa Riquelme",
      "José Luis Chilavert",
      "Leryn Franco",
      "Roque Santa Cruz",
    ],
    Paramaribo: [
      "Clarence Seedorf",
      "Edgar Davids",
      "Tjatjie Dors",
      "Sherwin Campbell",
    ],
    Cochabamba: [
      "Ana María Romero",
      "Carlos Arana",
      "David Santalla",
      "Elizabeth Vargas",
    ],
    Córdoba: [
      "El Cordobes",
      "Cacho Castaña",
      "Lázaro Cárdenas",
      "Susana Giménez",
    ],
    Maracaibo: [
      "Betulio González",
      "Daniel Sarcos",
      "Valeria Valle",
      "Mónica Spear",
    ],
    Guayaquil: [
      "Vanessa Marcil",
      "Juan Manuel Correa",
      "Jonathan Gonzalez",
      "Héctor Napolitano",
    ],
    "San Salvador": [
      "Carla Vila",
      "Cheryl Perera",
      "Ricardo Arjona",
      "José Napoleón Duarte",
    ],
  },
};

(function () {
  const continentSelect = document.getElementById("continentSelect");
  const citySelect = document.getElementById("citySelect");

  continentSelect.addEventListener("change", function () {
    const continent = continentSelect.value;
    updateCityOptions(continent);
    updateCelebrityOptions(); // Reset celebrities when continent changes
  });

  citySelect.addEventListener("change", function () {
    const continent = continentSelect.value;
    const city = citySelect.value;
    updateCelebrityOptions(continent, city);
  });

  function updateCityOptions(continent) {
    citySelect.innerHTML = '<option value="">Select City</option>';
    if (continent && celebritiesByCity[continent]) {
      for (const city of Object.keys(celebritiesByCity[continent])) {
        const option = document.createElement("option");
        option.value = city;
        option.textContent = city;
        citySelect.appendChild(option);
      }
    }
  }

  function updateCelebrityOptions(continent, city) {
    celebritySelect.innerHTML = '<option value="">Select Celebrity</option>';
    if (
      continent &&
      city &&
      celebritiesByCity[continent] &&
      celebritiesByCity[continent][city]
    ) {
      for (const celebrity of celebritiesByCity[continent][city]) {
        const option = document.createElement("option");
        option.value = celebrity;
        option.textContent = celebrity;
        celebritySelect.appendChild(option);
      }
    }
  }

  // Initial population of city dropdown based on default selected continent
  const defaultContinent = continentSelect.value;
  updateCityOptions(defaultContinent);
})();

document.addEventListener("DOMContentLoaded", function () {
  const currentPlayer = document.getElementById("player-select");
  const nameButton = document.getElementById("p-name-btn");
  let selectedPlayer;

  currentPlayer.addEventListener("change", function () {
    selectedPlayer = currentPlayer.value;
    console.log(selectedPlayer);

    // Detach any existing click event listener before attaching a new one
    nameButton.removeEventListener("click", handleSubmit);
    nameButton.addEventListener("click", handleSubmit);
  });

  function handleSubmit() {
    const playerName = document.getElementById("p-name").value;
    const characterName = document.getElementById("celebritySelect").value;
    const city = document.getElementById("citySelect").value;

    if (selectedPlayer === "Player 1") {
      // Update Player 1's profile
      document.getElementById("p1-name").textContent = playerName;
      document.getElementById("p1-character").textContent = characterName;
      document.getElementById("p1-city").textContent = city;

      // Modify the image src for Player 1
      const characterImage = characterName.toLowerCase().replace(/\s/g, "-");
      document.getElementById(
        "player1-img"
      ).src = `./static/images/${characterImage}.jpg`;
      document.getElementById("player1-img").alt = characterName;

      // Fetch weather information for Player 1
      fetchWeather(city, "p1-weather-info", "p1-temp", "p1-weather-icon");
    } else if (selectedPlayer === "Player 2") {
      // Update Player 2's profile
      document.getElementById("p2-name").textContent = playerName;
      document.getElementById("p2-character").textContent = characterName;
      document.getElementById("p2-city").textContent = city;

      // Modify the image src for Player 2
      const characterImage = characterName.toLowerCase().replace(/\s/g, "-");
      document.getElementById(
        "player2-img"
      ).src = `./static/images/${characterImage}.jpg`;
      document.getElementById("player2-img").alt = characterName;

      // Fetch weather information for Player 2
      fetchWeather(city, "p2-weather-info", "p2-temp", "p2-weather-icon");
    }

    // Reset form for next input
    document.getElementById("p-name").value = "";
    document.getElementById("celebritySelect").value = "";
    document.getElementById("citySelect").value = "";
  }

  function fetchWeather(city, targetElementId, tempElementId, iconElementId) {
    fetch(
      `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}`
    )
      .then((response) => response.json())
      .then((data) => {
        const weather = data.weather[0].main;
        const temperatureKelvin = data.main.temp;
        const temperatureCelsius = temperatureKelvin - 273.15;
        const weatherIcon = data.weather[0].icon;
        // Updated function to include temperature and icon
        updateWeather(
          weather,
          temperatureCelsius,
          weatherIcon,
          targetElementId,
          tempElementId,
          iconElementId
        );
      });
  }

  function updateWeather(
    weather,
    temperatureCelsius,
    weatherIcon,
    targetElementId,
    tempElementId,
    iconElementId
  ) {
    const weatherInfoDiv = document.getElementById(targetElementId);
    const tempElement = document.getElementById(tempElementId);
    const iconElement = document.getElementById(iconElementId);

    // Clear previous content
    weatherInfoDiv.innerHTML = "";
    tempElement.textContent = "";
    iconElement.innerHTML = "";

    // Update content with new data
    weatherInfoDiv.innerHTML = `
      <span> | Current Weather: ${weather}</span> 
      <img src="https://openweathermap.org/img/wn/${weatherIcon}.png" alt="${weather}">`;
    tempElement.textContent = `Temperature: ${temperatureCelsius.toFixed(1)}°C`;
  }
})();
