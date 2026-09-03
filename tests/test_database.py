import sqlite3
import tempfile
import unittest
from pathlib import Path

from xiaomi_ble_monitor.database import initialize_database, save_measurement
from xiaomi_ble_monitor.decoder import Measurement


class DatabaseTests(unittest.TestCase):
    def test_initializes_and_stores_measurement(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "measurements.db"
            initialize_database(path)
            save_measurement(path, "test_sensor", "Test Sensor", Measurement(21.5, 48, 2980))
            connection = sqlite3.connect(path)
            try:
                row = connection.execute(
                    "SELECT device_id, temperature, humidity, battery_mv FROM measurements"
                ).fetchone()
            finally:
                connection.close()
            self.assertEqual(row, ("test_sensor", 21.5, 48, 2980))


if __name__ == "__main__":
    unittest.main()
