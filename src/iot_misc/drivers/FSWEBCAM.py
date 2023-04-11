import asyncio

from abstract import IoTSensor
from time import time_ns


class FSWEBCAM(IoTSensor):
    """Class for sampling from an `fswebcam`-connected source."""

    def __init__(self, driver, sensor) -> None:
        """Initialize class for an fswebcam device using
        `driver` and `sensor` from the `IoTSensor` superclass."""
        super().__init__(driver, sensor)

    # TODO Refactor for `popen`
    async def sample(self, delay: float):
        """Sample from the fswebcam `device` at the
        interval (in seconds) set by `delay`."""
        while True:
            if self.sensor.data_available:
                yield {
                    "timestamp": time_ns(),
                    "img": bytes("...", "utf8"),
                }
            else:
                raise ValueError("SCD-30 sensor is not ready")

            await asyncio.sleep(delay)

    @property
    def driver(self) -> dict:
        """Return driver for fswebcam sensor."""
        # TODO Customize?
        return super().driver

    @property
    def units(self) -> dict:
        """Return units for fswebcam sample values."""
        return {"timstamp": "nanosecond", "img": "jpeg"}
