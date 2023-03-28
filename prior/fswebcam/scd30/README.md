# Miscellaneous IoT Repository: `fswebcam-scd30/`

## Functionality

1. Sample from
   - [Adafruit SCD-30 - NDIR CO2 Temperature and Humidity Sensor](https://www.adafruit.com/product/4867)
2. Take a photo using [`fswebcam`](https://github.com/fsphil/fswebcam)
3. Label the photograph with
   - Temperature (`C`, SCD-30)
   - CO<sub>2</sub> (`ppm`, SCD-30)
   - Relative Humidity (`rH`, SCD-30)
4. Write sensor data to
   - [NeonDB](https://neon.tech) database for persistent storage
     - Images to `BYTEA` table
   - [Redis Stream](https://redis.io/docs/data-types/streams/) for "hot" data store (failsafe)
     - Images to local disk

## Schema

[dbdiagram.io][dbio_schema]

## ToDos

- [ ] Refactor script
  - [ ] Modularize with `async` functions
  - [ ] `async` runtime
- [x] [dbdiagram.io][dbio_schema] Schema
- [x] "Dump" Redis Stream to Apache Parquet on `Ctrl-C` (code commented out)
  - _NB. Pyarrow does not compile on (my) Raspberry Pi 4. It has been done, but so far is not working for me._
- [x] Write to SQL database
  - [x] Image `BLOB`s
  - [x] Session indexing
    - [x] Extend NeonDB schema
    - [x] Extend script to write to appropriate tables

[dbio_schema]: https://dbdiagram.io/d/641dc4665758ac5f1723edb0
