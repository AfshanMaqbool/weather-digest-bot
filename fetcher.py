import requests


GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WMO_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Icy fog",
    51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
    61: "Light rain", 63: "Rain", 65: "Heavy rain",
    71: "Light snow", 73: "Snow", 75: "Heavy snow",
    80: "Light showers", 81: "Showers", 82: "Heavy showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Heavy thunderstorm with hail",
}


class WeatherFetcher:
    def __init__(self, city: str):
        self.city = city
        self.lat = None
        self.lon = None
        self.country = None

    def geocode(self):
        """Resolve city name to coordinates."""
        resp = requests.get(GEOCODE_URL, params={"name": self.city, "count": 1}, timeout=10)
        resp.raise_for_status()
        results = resp.json().get("results")
        if not results:
            raise ValueError(f"City not found: {self.city!r}")
        r = results[0]
        self.lat = r["latitude"]
        self.lon = r["longitude"]
        self.country = r.get("country", "")
        return self

    def fetch(self) -> dict:
        """Fetch today's weather data from Open-Meteo."""
        if self.lat is None:
            self.geocode()

        params = {
            "latitude": self.lat,
            "longitude": self.lon,
            "current": [
                "temperature_2m",
                "apparent_temperature",
                "relative_humidity_2m",
                "wind_speed_10m",
                "weathercode",
            ],
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "weathercode",
                "sunrise",
                "sunset",
            ],
            "timezone": "auto",
            "forecast_days": 3,
        }

        resp = requests.get(FORECAST_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        return {
            "city": self.city,
            "country": self.country,
            "timezone": data.get("timezone", ""),
            "current": data["current"],
            "daily": data["daily"],
        }

    @staticmethod
    def describe_code(code: int) -> str:
        return WMO_CODES.get(code, "Unknown")
