# Miscellaneous IoT Repository: `aio-cli` branch

Command-line interface for sampling from IoT sensors then writing to one or more persistent stores. Merges the design goals (and partial implementations) of [iot-data-stream-utils](https://github.com/jagrafft/iot-data-stream-utils) and the `{ main ; dev }` branches of [iot-misc](https://github.com/jagrafft/iot-misc), but is otherwise a "ground up" rewrite using a modularized `async` framework.

**Note:** [CircuitPython][circuitpython], drivers, and support libraries for IoT devices are _NOT_ included in `pyproject.toml` (e.g. not installed by default).

## Initial Targets

- Standardize Configuration File
  - [ ] TOML
- Data Persistence
    - [ ] [Apache Parquet][apacheparquet]
    - [ ] [InfluxDB][influxdb]
    - [ ] [NeonDB][neondb]
    - [ ] [Redis Streams][redisstreams]
- Platform
    - [Raspberry Pi][rpif]
        - [CircuitPython][circuitpython]
- Drivers
    - [ ] Abstract class for an IoT Sensor
    - [AdaFruit][adafruit]
        - [ ] [BNO055 - 9-DoF Absolute Orientation IMU Fusion Breakout][bno055]
        - [ ] [MAX31865 - PT1000 RTD Temperature Sensor Amplifier][max31865]
        - [ ] [SCD-30 - NDIR CO<sub>2</sub> Temperature and Humidity Sensor][scd30]
        - [ ] [SHT-30 - Mesh-protected Weather-proof Temperature/Humidity Sensor][sht30]
    - Platform Utilities
        - [ ] [fswebcam][fswebcam]

## Options

| CLI               | Configuation TOML     | Type      | Description                                              |
|:-----------------:|:---------------------:|:---------:|:---------------------------------------------------------|
| `-c, --config`    |                       | _flag_    | Path to session configuration. **Required.**             |
| `-n, --name`      | `[session].name`      | `String`  | Name of session. Used as key and identifier for dataset. |
| `-t, --timestamp` | `[session].timestamp` | `Boolean` | Append current timestamp to session name.                |


[adafruit]: https://www.adafruit.com/
[apacheparquet]: https://parquet.apache.org/
[bno055]: https://www.adafruit.com/product/2472
[circuitpython]: https://circuitpython.org
[fswebcam]: https://github.com/fsphil/fswebcam
[influxdb]: https://github.com/influxdata/influxdb
[max31865]: https://www.adafruit.com/product/3328
[neondb]: https://neon.tech
[redisstreams]: https://redis.io/docs/data-types/streams/
[rpif]: https://www.raspberrypi.org/
[scd30]: https://www.adafruit.com/product/4867 
[sht30]: https://www.adafruit.com/product/4099
