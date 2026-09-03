# Xiaomi BLE Environment Monitor

A lightweight Linux service that reads temperature, humidity, and battery voltage from a Xiaomi BLE sensor and stores timestamped measurements in SQLite.

The project is based on a working home-automation collector and has been reorganized for safe public use. Device addresses and local measurements are never committed to the repository.

## Features

- Asynchronous BLE communication with `bleak`
- Xiaomi temperature/humidity payload decoding
- Periodic measurements with retry-on-error behavior
- SQLite storage with an indexed timestamp column
- One-shot command for testing a sensor
- Configuration through environment variables
- Unit tests that do not require Bluetooth hardware
- Linux `systemd` service example

## Requirements

- Linux with Bluetooth support
- Python 3.10 or newer
- A compatible Xiaomi BLE temperature/humidity sensor

## Installation

```bash
git clone https://github.com/cmayts/xiaomi-ble-environment-monitor.git
cd xiaomi-ble-environment-monitor
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Configuration

Copy the example configuration and replace the placeholder address with your sensor's BLE address:

```bash
cp .env.example .env
```

Export the values before running the collector:

```bash
set -a
source .env
set +a
```

| Variable | Purpose | Default |
| --- | --- | --- |
| `XIAOMI_BLE_ADDRESS` | Sensor BLE address | Required |
| `XIAOMI_DEVICE_ID` | Stable identifier stored in SQLite | `xiaomi_sensor` |
| `XIAOMI_DEVICE_NAME` | Human-readable sensor name | `Xiaomi BLE Sensor` |
| `XIAOMI_READ_INTERVAL` | Seconds between readings | `1800` |
| `XIAOMI_DATABASE_PATH` | SQLite database location | `data/home.db` |

## Usage

Read and store one measurement:

```bash
python -m xiaomi_ble_monitor once
```

Run continuously:

```bash
python -m xiaomi_ble_monitor run
```

## Run as a Linux service

The example in [`deploy/xiaomi-ble-monitor.service`](deploy/xiaomi-ble-monitor.service) can be adapted to the installation directory and Linux user, then installed with `systemd`.

## Data and privacy

The repository contains no real Bluetooth addresses or sensor measurements. Runtime databases, `.env` files, logs, and Python caches are ignored by Git. The original local `home.db` remains only on the source computer.

## Tests

```bash
python -m unittest discover -s tests -v
```

## License

Released under the MIT License.
