import argparse
import asyncio

from .collector import collect_once, run_collector
from .config import Settings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Collect Xiaomi BLE sensor measurements")
    parser.add_argument("command", choices=("once", "run"), help="Read once or run continuously")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    try:
        settings = Settings.from_environment()
        if args.command == "once":
            measurement, timestamp = asyncio.run(collect_once(settings))
            print(f"Temperature: {measurement.temperature:.2f} °C")
            print(f"Humidity: {measurement.humidity}%")
            print(f"Battery: {measurement.battery_mv} mV")
            print(f"Timestamp: {timestamp}")
        else:
            asyncio.run(run_collector(settings))
    except (ValueError, KeyboardInterrupt) as error:
        raise SystemExit(str(error)) from error
