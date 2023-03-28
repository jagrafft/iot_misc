# Miscellaneous IoT Repository: `aio-cli` branch

Command-line interface for sampling from IoT sensors then writing to one or more persistent stores. Merges the design goals (and partial implementations) of [iot-data-stream-utils](https://github.com/jagrafft/iot-data-stream-utils) and the `{ main ; dev }` branches of [iot-misc](https://github.com/jagrafft/iot-misc), but is otherwise a "ground up" rewrite using a modularized `async` framework.

## Initial Targets

- Data Persistence
    - [ ] [Apache Parquet][apacheparquet]
    - [ ] [InfluxDB][influxdb]
    - [ ] [NeonDB][neondb]
    - [ ] [Redis Streams][redisstreams]
- Platform
    - [Raspberry Pi][rpif]
        - [CircuitPython][circuitpython]
- Sensors
    - [AdaFruit][adafruit]
        - [ ] [MAX31865 - PT1000 RTD Temperature Sensor Amplifier][max31865]
        - [ ] [SCD-30 - NDIR CO<sub>2</sub> Temperature and Humidity Sensor][scd30]
        - [ ] [SHT-30 - Mesh-protected Weather-proof Temperature/Humidity Sensor][sht30]
    - Platform Utilities
        - [ ] [fswebcam][fswebcam]

[adafruit]: https://www.adafruit.com/
[apacheparquet]: https://parquet.apache.org/
[circuitpython]: https://circuitpython.org
[fswebcam]: https://github.com/fsphil/fswebcam
[influxdb]: https://github.com/influxdata/influxdb
[max31865]: https://www.adafruit.com/product/3328
[neondb]: https://neon.tech
[redisstreams]: https://redis.io/docs/data-types/streams/
[rpif]: https://www.raspberrypi.org/
[scd30]: https://www.adafruit.com/product/4867 
[sht30]: https://www.adafruit.com/product/4099
