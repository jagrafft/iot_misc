from abc import ABC, abstractmethod


class IoTSensor(ABC):
    """ """

    @abstractmethod
    def __init__(self, driver, sensor) -> None:
        """ """
        self._driver = driver
        self._sensor = sensor

    @abstractmethod
    def sample(self, rate) -> dict:
        """ """
        pass

    @property
    @abstractmethod
    def driver(self) -> dict:
        """ """
        return {"driver": self._driver}

    @property
    @abstractmethod
    def units(self) -> dict:
        """ """
        pass
