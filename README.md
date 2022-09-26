# Miscellaneous IoT Repository

"Home" for scripts and utilities I've written for working with Internet o' Things (IoT) devices---predominantly those manufactured by [Adafruit][adafruit] and the [Raspberry Pi Foundation][rpif]. Individual folders contain `README`s, 

| Folder                     | Description                                                                                                                                                                                                                                                                                      |
|:---------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `fswebcam-max31865/`       | Script to sample from an [Adafruit PT1000 RTD Temperature Sensor Amplifier MAX31865](https://www.adafruit.com/product/3328), take a photo using [`fswebcam`](https://github.com/fsphil/fswebcam), label the photograph with a timestamp and temperature reading, then write the sample to a CSV. |
| `fswebcam_max31865_scd41/` | Script to sample from an [Adafruit PT1000 RTD Temperature Sensor Amplifier MAX31865](https://www.adafruit.com/product/3328) and [Adafruit SCD-41 - True CO2 Temperature and Humidity Sensor](https://www.adafruit.com/product/5190), label the photograph, then write data samples to CSV. |

[adafruit]: https://www.adafruit.com/
[rpif]: https://www.raspberrypi.org/
