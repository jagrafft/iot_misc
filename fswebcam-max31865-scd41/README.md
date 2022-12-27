# Miscellaneous IoT Repository: `fswebcam-max31856-scd41/`

1. Sample from
   - [Adafruit PT1000 RTD Temperature Sensor Amplifier MAX31865](https://www.adafruit.com/product/3328)
   - [Adafruit SCD-41 - True CO2 Temperature and Humidity Sensor](https://www.adafruit.com/product/5190)
2. Take a photo using [`fswebcam`](https://github.com/fsphil/fswebcam)
3. Label the photograph with
   - Temperature (`C`, Max31865)
   - Temperature (`C`, SCD-41)
   - CO<sub>2</sub> (`ppm`, SCD-41)
   - Relative Humidity (`RH`, SCD-41)
4. Write data to [Redis Streams](https://redis.io/docs/data-types/streams/)
   - `max31865_{YYYY-mm-ddTHHMMSS}`
   - `scd41_{YYYY-mm-ddTHHMMSS}`

<!-- include photos/schematic(s)/...? -->
