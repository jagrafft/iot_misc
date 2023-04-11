import asyncio

from abstract.IoTSensor import IoTSensor
from time import time_ns


class BNO055(IoTSensor):
    """Class for sampling from an Adafruit BNO055."""

    def __init__(self, driver, sensor) -> None:
        """Initialize class for an Adafruit BNO055 sensor using
        `driver` and `sensor` from the `IoTSensor` superclass."""
        super().__init__(driver, sensor)

    async def sample(self, delay: float) -> dict:
        """Sample from the Adafruit BNO055 `device` at the interval
        (in seconds) set by `delay`."""
        while True:
            yield {
                "timestamp": time_ns(),
                "accelerometer": self._sensor.acceleration,
                "eulerAngle": self._sensor.euler,
                "gravity": self._sensor.gravity,
                "gyroscope": self._sensor.gyro,
                "linearAcceleration": self._sensor.linear_acceleration,
                "magnetometer": self._sensor.magnetic,
                "quaternion": self._sensor.quaternion,
            }

            await asyncio.sleep(delay)

    @property
    def driver(self) -> dict:
        """Return driver for Adafruit BNO055 sensor."""
        return super().driver

    @property
    def units(self) -> dict:
        """Return units for BNO055 sample values."""
        return {
            "timestamp": "nanosecond",
            "accelerometer": "m/s^2",
            "eulerAngle": "degree",
            "gravity": "m/s^2",
            "gyroscope": "rad/sec",
            "linearAcceleration": "m/s^2",
            "magnetometer": "microtesla",
            "quaternion": "float",
        }
