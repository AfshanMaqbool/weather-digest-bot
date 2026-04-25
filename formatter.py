from datetime import datetime
from .fetcher import WeatherFetcher


WIND_ADVICE = [
    (20,  "🧘 Calm — perfect for outdoor plans."),
    (40,  "🚶 Light breeze — comfortable outside."),
    (60,  "🌬️ Moderate wind — hold onto your hat."),
    (80,  "💨 Strong wind — be careful outdoors."),
    (999, "🌪️ Very strong wind — stay indoors if possible."),
]

RAIN_ADVICE = [
    (0,   "☀️ No rain expected — no umbrella needed."),
    (5,   "🌦️ Light rain possible — maybe pack an umbrella."),
    (20,  "🌧️ Moderate rain expected — bring an umbrella."),
    (999, "⛈️ Heavy rain expected — dress accordingly."),
]


def _wind_tip(speed_kmh: float) -> str:
    for threshold, msg in WIND_ADVICE:
        if speed_kmh < threshold:
            return msg
    return ""


def _rain_tip(mm: float) -> str:
    for threshold, msg in RAIN_ADVICE:
        if mm <= threshold:
            return msg
    return ""


class WeatherFormatter:
    def __init__(self, data: dict):
        self.data = data

    def _current_section(self) -> str:
        c = self.data["current"]
        code = c.get("weathercode", 0)
        condition = WeatherFetcher.describe_code(code)
        temp = c.get("temperature_2m", "?")
        feels = c.get("apparent_temperature", "?")
        humidity = c.get("relative_humidity_2m", "?")
        wind = c.get("wind_speed_10m", 0)

        lines = [
            "## 🌤️ Current Conditions\n",
            f"| | |",
            f"|---|---|",
            f"| **Condition** | {condition} |",
            f"| **Temperature** | {temp}°C |",
            f"| **Feels like** | {feels}°C |",
            f"| **Humidity** | {humidity}% |",
            f"| **Wind speed** | {wind} km/h |",
            "",
            f"> {_wind_tip(wind)}",
        ]
        return "\n".join(lines)

    def _forecast_section(self) -> str:
        daily = self.data["daily"]
        dates = daily.get("time", [])
        max_t = daily.get("temperature_2m_max", [])
        min_t = daily.get("temperature_2m_min", [])
        precip = daily.get("precipitation_sum", [])
        codes = daily.get("weathercode", [])
        sunrises = daily.get("sunrise", [])
        sunsets = daily.get("sunset", [])

        lines = ["\n## 📅 3-Day Forecast\n"]
        lines.append("| Date | Condition | High | Low | Rain | Sunrise | Sunset |")
        lines.append("|---|---|---|---|---|---|---|")

        for i, date in enumerate(dates[:3]):
            dt = datetime.fromisoformat(date)
            label = dt.strftime("%A, %b %d")
            condition = WeatherFetcher.describe_code(codes[i] if i < len(codes) else 0)
            hi = max_t[i] if i < len(max_t) else "?"
            lo = min_t[i] if i < len(min_t) else "?"
            rain = precip[i] if i < len(precip) else 0
            sunrise = sunrises[i].split("T")[-1][:5] if i < len(sunrises) else "?"
            sunset = sunsets[i].split("T")[-1][:5] if i < len(sunsets) else "?"
            lines.append(f"| {label} | {condition} | {hi}°C | {lo}°C | {rain} mm | {sunrise} | {sunset} |")

        # Rain tip based on today
        today_rain = precip[0] if precip else 0
        lines.append(f"\n> {_rain_tip(today_rain)}")
        return "\n".join(lines)

    def to_markdown(self) -> str:
        city = self.data["city"]
        country = self.data["country"]
        tz = self.data["timezone"]
        now = datetime.now().strftime("%A, %B %d %Y — %H:%M")

        header = (
            f"# 🌍 Weather Digest — {city}, {country}\n\n"
            f"**Generated:** {now}  \n"
            f"**Timezone:** {tz}\n"
        )
        divider = "\n---\n"
        footer = (
            "\n---\n"
            "_Data provided by [Open-Meteo](https://open-meteo.com/) — free & open-source weather API._"
        )

        return header + divider + self._current_section() + self._forecast_section() + footer
