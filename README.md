# 🌤️ weather-digest-bot

A lightweight Python CLI that fetches a **daily weather digest** for any city and saves it as a Markdown report — or sends it straight to **Telegram**.

No API key required. Powered by [Open-Meteo](https://open-meteo.com/), a free and open-source weather API.

---

## ✨ Features

- 🌍 Works for any city worldwide
- 📋 Current conditions — temperature, feels-like, humidity, wind
- 📅 3-day forecast with highs, lows, rain, sunrise & sunset
- 💡 Smart tips (umbrella advice, wind warnings)
- 📄 Saves a clean Markdown report
- 📬 Optional Telegram delivery
- ⚡ Zero API key needed (uses Open-Meteo)

---

## 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/weather-digest-bot.git
cd weather-digest-bot
pip install -r requirements.txt
```

---

## 🚀 Usage

**Basic — save a report for any city:**
```bash
python main.py "London"
python main.py "Tokyo"
python main.py "New York"
```

Output: `weather_report.md` in the current directory.

**Custom output file:**
```bash
python main.py "Berlin" --output berlin.md
```

**Send to Telegram:**
```bash
export TELEGRAM_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"

python main.py "Paris" --telegram
```

**Print to terminal only:**
```bash
python main.py "Sydney" --no-save
```

---

## 📄 Sample Output

```
# 🌍 Weather Digest — London, United Kingdom

**Generated:** Friday, April 25 2025 — 08:30
**Timezone:** Europe/London

---

## 🌤️ Current Conditions

| | |
|---|---|
| **Condition** | Partly cloudy |
| **Temperature** | 14°C |
| **Feels like** | 12°C |
| **Humidity** | 72% |
| **Wind speed** | 18 km/h |

> 🧘 Calm — perfect for outdoor plans.

## 📅 3-Day Forecast

| Date | Condition | High | Low | Rain | Sunrise | Sunset |
|---|---|---|---|---|---|---|
| Friday, Apr 25 | Partly cloudy | 16°C | 9°C | 0.0 mm | 05:42 | 20:18 |
| Saturday, Apr 26 | Light rain | 14°C | 8°C | 4.2 mm | 05:40 | 20:20 |
| Sunday, Apr 27 | Overcast | 13°C | 7°C | 1.1 mm | 05:38 | 20:22 |

> 🌦️ Light rain possible — maybe pack an umbrella.
```

---

## 🗂️ Project Structure

```
weather-digest-bot/
├── main.py              # CLI entry point
├── requirements.txt
├── .gitignore
└── weather/
    ├── __init__.py
    ├── fetcher.py       # Open-Meteo API + geocoding
    ├── formatter.py     # Markdown report builder
    └── notifier.py      # File save + Telegram sender
```

---

## 🤖 Setting Up Telegram (Optional)

1. Message [@BotFather](https://t.me/BotFather) on Telegram → create a bot → copy the token
2. Message your bot, then visit:
   `https://api.telegram.org/bot<TOKEN>/getUpdates`
   to find your `chat_id`
3. Set the env vars and run with `--telegram`

---

## 📄 License

MIT — free to use, modify, and share.
