from abc import ABC, abstractmethod
from .   import IoTSensor

class ZMQSensorInterface(ABC):
    """
    """

    @abstractmethod
    def __init__(self, iot_sensor: IoTSensor, rate: float, address, socket) -> None:
        """
        """
        self._address = address
        self._iot_sensor = iot_sensor
        self._sample_rate = rate
        self._socket = socket

        self._publishing = False
        self._socket.bind(self._address)
         
    @abstractmethod
    def cleanup(self):
        """
        """
        pass

    @abstractmethod
    def publish(self):
        """
        """
        pass

    @abstractmethod
    def stop(self):
        """
        """
        pass

    @property
    def driver(self) -> str:
        """
        """
        return self._iot_sensor.driver
    
    @property
    def units(self) -> str:
        return self._iot_sensor.units
    
    @property
    @abstractmethod
    def publishing(self) -> str:
        """
        """
        return f"""{{ 'publishing': {self._publishing} }}"""

    @publishing.setter
    @abstractmethod
    def publishing(self, flag: bool) -> None:
        """
        """
        pass
    
    @property
    @abstractmethod
    def sample_rate(self) -> str:
        """
        """
        return f"""{{ 'sample_rate': {self._sample_rate} }}"""

    @sample_rate.setter
    @abstractmethod
    def sample_rate(self, rate) -> None:
        """
        """
        pass
