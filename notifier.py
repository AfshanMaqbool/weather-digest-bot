import os
import requests


class Notifier:
    """Handles output: save to file and/or send to Telegram."""

    def save_markdown(self, content: str, path: str = "weather_report.md") -> str:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def send_telegram(self, content: str, token: str = None, chat_id: str = None):
        """
        Send the digest to a Telegram chat.
        Falls back to env vars TELEGRAM_TOKEN and TELEGRAM_CHAT_ID if not passed.
        """
        token = token or os.getenv("TELEGRAM_TOKEN")
        chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")

        if not token or not chat_id:
            raise ValueError(
                "Telegram token and chat_id are required. "
                "Set TELEGRAM_TOKEN and TELEGRAM_CHAT_ID environment variables, "
                "or pass them directly."
            )

        # Telegram has a 4096 char limit per message; split if needed
        chunks = [content[i:i+4000] for i in range(0, len(content), 4000)]
        url = f"https://api.telegram.org/bot{token}/sendMessage"

        for chunk in chunks:
            resp = requests.post(
                url,
                json={"chat_id": chat_id, "text": chunk, "parse_mode": "Markdown"},
                timeout=10,
            )
            resp.raise_for_status()

        return len(chunks)
