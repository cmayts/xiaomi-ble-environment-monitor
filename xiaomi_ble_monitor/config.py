from dataclasses import dataclass
import os
from pathlib import Path

DATA_UUID = "ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6"


@dataclass(frozen=True)
class Settings:
    address: str
    device_id: str = "xiaomi_sensor"
    device_name: str = "Xiaomi BLE Sensor"
    read_interval: int = 1800
    database_path: Path = Path("data/home.db")
    data_uuid: str = DATA_UUID

    @classmethod
    def from_environment(cls) -> "Settings":
        address = os.environ.get("XIAOMI_BLE_ADDRESS", "").strip()
        if not address:
            raise ValueError("XIAOMI_BLE_ADDRESS is required")

        interval = int(os.environ.get("XIAOMI_READ_INTERVAL", "1800"))
        if interval <= 0:
            raise ValueError("XIAOMI_READ_INTERVAL must be positive")

        return cls(
            address=address,
            device_id=os.environ.get("XIAOMI_DEVICE_ID", "xiaomi_sensor"),
            device_name=os.environ.get("XIAOMI_DEVICE_NAME", "Xiaomi BLE Sensor"),
            read_interval=interval,
            database_path=Path(os.environ.get("XIAOMI_DATABASE_PATH", "data/home.db")),
        )
