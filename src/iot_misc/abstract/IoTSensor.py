import asyncio

from abc import ABC, abstractmethod


class IoTSensor(ABC):
    """Abstract class for IoT sensor supported by application."""

    @abstractmethod
    def __init__(self, driver, sensor) -> None:
        """Initialize class with `driver` for IoT `sensor`."""
        self._driver = driver
        self._sensor = sensor

    @abstractmethod
    async def sample(self, delay: float) -> dict:
        """Sample from IoT sensor at interval set by `delay`."""
        pass

    @property
    @abstractmethod
    def driver(self) -> dict:
        """Return driver used by `IoTSensor` instance."""
        return {"driver": self._driver}

    @property
    @abstractmethod
    def units(self) -> dict:
        """Return units of values sampled from `IoTSensor`."""
        pass
