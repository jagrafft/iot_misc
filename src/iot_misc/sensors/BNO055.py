from abstract.IoTSensor import IoTSensor
from time import sleep, time_ns


# TODO Use `asyncio`
class BNO055(IoTSensor):
    """ """

    def __init__(self, driver, sensor) -> None:
        """ """
        super().__init__(driver, sensor)

    def sample(self, rate) -> dict:
        """ """
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
            sleep(rate)

    @property
    def driver(self) -> dict:
        """ """
        return super().driver

    @property
    def units(self) -> dict:
        """ """
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
