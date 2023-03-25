# Miscellaneous IoT Repository: `fswebcam-scd30/`

1. Sample from
   - [Adafruit SCD-30 - NDIR CO2 Temperature and Humidity Sensor](https://www.adafruit.com/product/4867)
2. Take a photo using [`fswebcam`](https://github.com/fsphil/fswebcam)
3. Label the photograph with
   - Temperature (`C`, SCD-30)
   - CO<sub>2</sub> (`ppm`, SCD-30)
   - Relative Humidity (`rH`, SCD-30)
4. Write data to
   - [NeonDB](https://neon.tech) (persistent storage)
   - [Redis Stream](https://redis.io/docs/data-types/streams/) ("hot" data store)

## Work-in-Progress Items

- [ ] `async` runtime
  - [ ] Refactor to use `async` functions
- [ ] Session indexing
  - [x] Extend NeonDB schema
  - [ ] Extend script to write to appropriate tables
- [x] "Dump" Redis Stream to Apache Parquet on `Ctrl-C` (code commented out)
  - _NB. Pyarrow does not compile on (my) Raspberry Pi 4. It has been done, so far not working for me._
- [x] Write to SQL database
  - [x] Image `BLOB`s
  - [x] [dbdiagram.io](https://dbdiagram.io/d/641dc4665758ac5f1723edb0) Schema
<!-- include photos/schematic(s)/...? -->
