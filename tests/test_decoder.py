import unittest

from xiaomi_ble_monitor.decoder import Measurement, decode_sensor_data


class DecoderTests(unittest.TestCase):
    def test_decodes_positive_temperature(self):
        payload = bytes([0x2E, 0x09, 45, 0xB8, 0x0B])
        self.assertEqual(decode_sensor_data(payload), Measurement(23.5, 45, 3000))

    def test_decodes_negative_temperature(self):
        payload = (-525).to_bytes(2, "little", signed=True) + bytes([61]) + (2850).to_bytes(2, "little")
        self.assertEqual(decode_sensor_data(payload), Measurement(-5.25, 61, 2850))

    def test_rejects_short_payload(self):
        with self.assertRaises(ValueError):
            decode_sensor_data(b"\x00\x01")


if __name__ == "__main__":
    unittest.main()
