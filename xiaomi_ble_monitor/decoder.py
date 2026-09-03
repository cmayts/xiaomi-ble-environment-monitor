from dataclasses import dataclass


@dataclass(frozen=True)
class Measurement:
    temperature: float
    humidity: int
    battery_mv: int


def decode_sensor_data(data: bytes) -> Measurement:
    """Decode the five-byte Xiaomi temperature/humidity characteristic."""
    if len(data) < 5:
        raise ValueError(f"Expected at least 5 bytes, received {len(data)}")

    temperature = int.from_bytes(data[0:2], byteorder="little", signed=True) / 100
    humidity = data[2]
    battery_mv = int.from_bytes(data[3:5], byteorder="little")
    return Measurement(temperature, humidity, battery_mv)
