from ..abstract.ZMQSensorInterface import ZMQSensorInterface
from ..sensors.BNO055              import BNO055

class BNO055_ZMQ(ZMQSensorInterface):
    """
    """

    def __init__(self, bno055: BNO055, sample_rate: float, address: str, socket) -> None:
        """
        """
        super().__init__(bno055, sample_rate, address, socket)

    def cleanup(self) -> None:
        """
        """
        print('Not yet implemented.')

    def publish(self):
        """
        """
        if self._publishing:
            while True:
                self._socket.send_json(next(self._iot_sensor.sample(self._sample_rate)))
        else:
            print('ERROR: publishing = False')
                

    def stop(self) -> None:
        """
        """
        print('Not yet implemented.')

    @property
    def driver(self) -> str:
        """
        """
        return super().driver

    @property
    def publishing(self) -> str:
        """
        """
        return super().publishing

    @publishing.setter
    def publishing(self, flag: bool) -> None:
        """
        """
        self._publishing = flag

    @property
    def sample_rate(self) -> str:
        """
        """
        return super().sample_rate

    @sample_rate.setter
    def sample_rate(self, rate: float) -> None:
        """
        """
        # TODO throw exception
        if rate >= 0.01:
            self._sample_rate = rate
        else:
            print('ERROR: rate must be >= 0.01')
