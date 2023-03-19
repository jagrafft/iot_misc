# Miscellaneous IoT Repository: `fswebcam-scd30/`

1. Sample from
   - [Adafruit SCD-30 - NDIR CO2 Temperature and Humidity Sensor](https://www.adafruit.com/product/4867)
2. Take a photo using [`fswebcam`](https://github.com/fsphil/fswebcam)
3. Label the photograph with
   - Temperature (`C`, SCD-30)
   - CO<sub>2</sub> (`ppm`, SCD-30)
   - Relative Humidity (`rH`, SCD-30)
4. Write data to [Redis Streams](https://redis.io/docs/data-types/streams/)
   - `scd30_{YYYY-mm-ddTHHMMSS}`

<!-- include photos/schematic(s)/...? -->
