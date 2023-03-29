import asyncio

from abstract import IoTSensor
from time import time_ns


class SCD30(IoTSensor):
    """Class for sampling from an Adafruit SCD-30."""

    def __init__(self, driver, sensor) -> None:
        """Initialize class for an Adafruit SCD-30 device using
        `driver` and `sensor` from the `IoTSensor` superclass."""
        super().__init__(driver, sensor)

    async def sample(self, delay: float):
        """Sample from the Adafruit SCD-30 `device` at the
        interval (in seconds) set by `delay`."""
        while True:
            if self.sensor.data_available:
                yield {
                    "timestamp": time_ns(),
                    "CO2": self.sensor.CO2,
                    "C": self.sensor.temperature,
                    "RH": self.sensor.relative_humidity,
                }
            else:
                raise ValueError("SCD-30 sensor is not ready")

            await asyncio.sleep(delay)

    @property
    def driver(self) -> dict:
        """Return driver for SCD-30 sensor."""
        return super().driver

    @property
    def units(self) -> dict:
        """Return units for SCD-30 sample values."""
        return {"timestamp": "nanosecond", "CO2": "ppm", "C": "°C", "RH": "%RH"}
