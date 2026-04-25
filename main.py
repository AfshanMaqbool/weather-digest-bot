#!/usr/bin/env python3
"""
weather-digest-bot
------------------
Fetch a weather digest for any city and save it as markdown
or send it to Telegram.

Usage:
    python main.py "London"
    python main.py "Tokyo" --telegram
    python main.py "New York" --output nyc_weather.md
"""

import argparse
import sys

from weather import WeatherFetcher, WeatherFormatter, Notifier


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a weather digest for a city.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("city", help="City name (e.g. 'London', 'New York')")
    parser.add_argument(
        "--telegram",
        action="store_true",
        help="Send digest to Telegram (requires TELEGRAM_TOKEN and TELEGRAM_CHAT_ID env vars)",
    )
    parser.add_argument(
        "--output",
        default="weather_report.md",
        metavar="FILE",
        help="Output markdown file path (default: weather_report.md)",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save to file (only useful with --telegram)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print(f"🌍 Fetching weather for: {args.city!r}")

    try:
        fetcher = WeatherFetcher(args.city)
        data = fetcher.fetch()
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to fetch weather data: {e}", file=sys.stderr)
        sys.exit(1)

    report = WeatherFormatter(data).to_markdown()

    notifier = Notifier()

    if not args.no_save:
        path = notifier.save_markdown(report, args.output)
        print(f"✅ Report saved → {path}")

    if args.telegram:
        try:
            chunks = notifier.send_telegram(report)
            print(f"✅ Sent to Telegram ({chunks} message(s))")
        except ValueError as e:
            print(f"❌ Telegram error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"❌ Failed to send Telegram message: {e}", file=sys.stderr)
            sys.exit(1)

    if not args.telegram and args.no_save:
        print(report)


if __name__ == "__main__":
    main()
