import asyncio

from bleak import BleakClient

from .config import Settings
from .database import initialize_database, save_measurement
from .decoder import Measurement, decode_sensor_data


async def read_sensor(settings: Settings) -> Measurement:
    async with BleakClient(settings.address, timeout=20) as client:
        data = await client.read_gatt_char(settings.data_uuid)
    return decode_sensor_data(bytes(data))


async def collect_once(settings: Settings) -> tuple[Measurement, str]:
    initialize_database(settings.database_path)
    measurement = await read_sensor(settings)
    timestamp = save_measurement(
        settings.database_path, settings.device_id, settings.device_name, measurement
    )
    return measurement, timestamp


async def run_collector(settings: Settings) -> None:
    initialize_database(settings.database_path)
    print(f"Monitoring {settings.device_name} every {settings.read_interval} seconds")

    while True:
        try:
            measurement, timestamp = await collect_once(settings)
            print(
                f"[{timestamp}] {measurement.temperature:.2f} °C, "
                f"{measurement.humidity}% RH, {measurement.battery_mv} mV"
            )
        except Exception as error:
            print(f"Sensor read failed: {error}. Retrying after the configured interval.")
        await asyncio.sleep(settings.read_interval)
