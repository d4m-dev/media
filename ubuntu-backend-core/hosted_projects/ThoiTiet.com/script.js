const API_KEY = "1f0868ad4687f50e1fb0345863ecf1b0";
const BASE_API_URL = "https://api.openweathermap.org/data/2.5/weather";

const content = {
  weatherData: document.querySelector(".grid-item:first-child"),
  locationName: document.querySelector(".location"),
  temp: document.querySelector(".temp"),
  unit: document.querySelector(".unit"),
  desc: document.querySelector(".desc"),
  max: document.querySelector(".max"),
  min: document.querySelector(".min"),
  feelsLike: document.querySelector(".feels-like"),
  humidity: document.querySelector(".humidity"),
  windSpeed: document.querySelector(".wind-speed"),
  pressure: document.querySelector(".pressure"),
  weatherImage: document.querySelector(".weather-image"),
};

const searchForm = document.querySelector(".search-form");
searchForm.addEventListener("submit", handleSubmit);

async function handleSubmit(e) {
  e.preventDefault();

  const locationName = searchForm.search.value.trim();
  if (!locationName) {
    alert("Vui lòng nhập thành phố, tiểu bang hoặc quốc gia.");
    return;
  }

  const isImperial = document.getElementById("unitType").checked === false;

  const unitType = isImperial ? "imperial" : "metric";

  try {
    const data = await getWeatherByLocation(locationName, unitType);

    if (data.cod === "404") {
      alert("Không tìm thấy địa điểm.");
      return;
    }

    displayWeatherData(data, isImperial);
  } catch (error) {
    console.error("Error on form submit.", error);
  }

  searchForm.reset();
}

async function getWeatherByLocation(locationName, unitType) {
  const apiUrl = `${BASE_API_URL}?q=${locationName}&appid=${API_KEY}&units=${unitType}`;

  return await fetchData(apiUrl);
}

async function getWeatherByPosition(lat, lon, unitType) {
  const apiUrl = `${BASE_API_URL}?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=${unitType}`;

  return await fetchData(apiUrl);
}

async function fetchData(apiUrl) {
  try {
    const response = await fetch(apiUrl);
    return await response.json();
  } catch (error) {
    console.error("Error fetching data.", error);
    throw error;
  }
}

function displayWeatherData(data, isImperial) {
  const { weather, main, wind, sys, name } = data;

  // set units
  const tempUnit = isImperial ? "°F" : "°C";
  const windSpeedUnit = isImperial ? "mph" : "m/s";
  const pressureUnit = isImperial ? "inHg" : "hPa";

  // convert pressure
  const pressureInHg = (main.pressure / 33.8639).toFixed(2);
  const pressure = isImperial ? pressureInHg : main.pressure;

  // set data
  content.locationName.textContent = name;
  content.temp.textContent = main.temp.toFixed(2);
  content.unit.textContent = tempUnit;
  content.desc.textContent = weather[0].description;
  content.max.textContent = `${main.temp_max} ${tempUnit}`;
  content.min.textContent = `${main.temp_min} ${tempUnit}`;
  content.feelsLike.textContent = `${main.feels_like} ${tempUnit}`;
  content.humidity.textContent = `${main.humidity}%`;
  content.windSpeed.textContent = `${wind.speed} ${windSpeedUnit}`;
  content.pressure.textContent = `${pressure} ${pressureUnit}`;
  content.weatherImage.src = `https://refinedguides.com/weather-app/img/${weather[0].icon}.png`;

  const currentTimestamp = Math.floor(Date.now() / 1000);

  const isDayTime =
    currentTimestamp >= sys.sunrise && currentTimestamp <= sys.sunset;

  content.weatherData.classList.toggle("day-time", isDayTime);
  content.weatherData.classList.toggle("night-time", !isDayTime);
}

function getCurrentPosition() {
  return new Promise((resolve) => {
    // if geolocation is not enabled, set Tokyo as default
    const latitude = 35.689487;
    const longitude = 139.691706;

    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => resolve(position.coords),
        () => resolve({ latitude, longitude })
      );
    } else {
      resolve({ latitude, longitude });
    }
  });
}

async function initWeatherApp() {
  try {
    const { latitude, longitude } = await getCurrentPosition();

    const data = await getWeatherByPosition(latitude, longitude, "metric");

    displayWeatherData(data, false);
  } catch (error) {
    console.error("Error fetching data on page load", error);
  }
}

initWeatherApp();
