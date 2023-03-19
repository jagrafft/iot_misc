# Miscellaneous IoT Repository: `dev`elopment branch

"Home" for scripts and utilities I've written for working with Internet o' Things (IoT) devices---predominantly those manufactured by [Adafruit][adafruit] and the [Raspberry Pi Foundation][rpif]. See `README` in individual folders.

| Folder                     | Description                                                                                                                                                                                                                                                                                      |
|:---------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `fswebcam/max31865/`       | Script to sample from an [Adafruit PT1000 RTD Temperature Sensor Amplifier MAX31865][max31865], take a photo using [`fswebcam`][fswebcam], label the photograph with a timestamp and temperature reading, then write the sample to a CSV. |
| `fswebcam/max31865-scd41/` | Sample from an [Adafruit PT1000 RTD Temperature Sensor Amplifier MAX31865][max31865] and [Adafruit SCD-41 - True CO2 Temperature and Humidity Sensor][scd41], take a photo using [`fswebcam`][fswebcam], label the photograph with sensor readings, write data samples to individual [Redis Streams][redis-streams]. |
| `fswebcam/scd30/`       | Script to sample from an [Adafruit SCD-30 - NDIR CO2 Temperature and Humidity Sensor][scd30], take a photo using [`fswebcam`][fswebcam], label the photograph with a timestamp, CO<sub>2</sub>, relative humidity, and temperature reading then write the sample a [Redis Stream][redis-streams]. |

[adafruit]: https://www.adafruit.com/
[fswebcam]: https://github.com/fsphil/fswebcam
[max31865]: https://www.adafruit.com/product/3328
[redis-streams]: https://redis.io/docs/data-types/streams/
[rpif]: https://www.raspberrypi.org/
[scd30]: https://www.adafruit.com/product/4867 
[scd41]: https://www.adafruit.com/product/5190
