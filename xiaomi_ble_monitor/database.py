import sqlite3
from datetime import datetime
from pathlib import Path

from .decoder import Measurement


def initialize_database(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    try:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                device_name TEXT NOT NULL,
                temperature REAL NOT NULL,
                humidity INTEGER NOT NULL,
                battery_mv INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )"""
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_measurements_timestamp ON measurements(timestamp)"
        )
        connection.commit()
    finally:
        connection.close()


def save_measurement(
    path: Path, device_id: str, device_name: str, measurement: Measurement
) -> str:
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    connection = sqlite3.connect(path)
    try:
        connection.execute(
            """INSERT INTO measurements
               (device_id, device_name, temperature, humidity, battery_mv, timestamp)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                device_id,
                device_name,
                measurement.temperature,
                measurement.humidity,
                measurement.battery_mv,
                timestamp,
            ),
        )
        connection.commit()
    finally:
        connection.close()
    return timestamp
