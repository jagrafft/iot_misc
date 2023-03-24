CREATE SCHEMA "scd30_fswebcam_leaven_monitor";

CREATE TABLE "scd30_fswebcam_leaven_monitor"."measurement_times" (
  "id" INTEGER PRIMARY KEY,
  "ts" TIMESTAMP WITH TIME ZONE UNIQUE NOT NULL
);

CREATE TABLE "scd30_fswebcam_leaven_monitor"."carbon_dioxide" (
  "ts_id" INTEGER PRIMARY KEY,
  "CO2" NUMERIC(16,10) NOT NULL
);

CREATE TABLE "scd30_fswebcam_leaven_monitor"."relative_humidity" (
  "ts_id" INTEGER PRIMARY KEY,
  "RH" NUMERIC(16,10) NOT NULL
);

CREATE TABLE "scd30_fswebcam_leaven_monitor"."degrees_celcius" (
  "ts_id" INTEGER PRIMARY KEY,
  "C" NUMERIC(16,10) NOT NULL
);

CREATE TABLE "scd30_fswebcam_leaven_monitor"."images" (
  "ts_id" INTEGER PRIMARY KEY,
  "img_blob" BYTEA NOT NULL
);

CREATE UNIQUE INDEX ON "scd30_fswebcam_leaven_monitor"."carbon_dioxide" ("ts_id", "CO2");

CREATE UNIQUE INDEX ON "scd30_fswebcam_leaven_monitor"."relative_humidity" ("ts_id", "RH");

CREATE UNIQUE INDEX ON "scd30_fswebcam_leaven_monitor"."degrees_celcius" ("ts_id", "C");

COMMENT ON TABLE "scd30_fswebcam_leaven_monitor"."measurement_times" IS 'Raspberry Pi clock';

COMMENT ON TABLE "scd30_fswebcam_leaven_monitor"."carbon_dioxide" IS 'SCD30 measurement';

COMMENT ON TABLE "scd30_fswebcam_leaven_monitor"."relative_humidity" IS 'SCD30 measurement';

COMMENT ON TABLE "scd30_fswebcam_leaven_monitor"."degrees_celcius" IS 'SCD30 measurement';

COMMENT ON TABLE "scd30_fswebcam_leaven_monitor"."images" IS 'fswebcam';

ALTER TABLE "scd30_fswebcam_leaven_monitor"."carbon_dioxide" ADD FOREIGN KEY ("ts_id") REFERENCES "scd30_fswebcam_leaven_monitor"."measurement_times" ("id");

ALTER TABLE "scd30_fswebcam_leaven_monitor"."relative_humidity" ADD FOREIGN KEY ("ts_id") REFERENCES "scd30_fswebcam_leaven_monitor"."measurement_times" ("id");

ALTER TABLE "scd30_fswebcam_leaven_monitor"."degrees_celcius" ADD FOREIGN KEY ("ts_id") REFERENCES "scd30_fswebcam_leaven_monitor"."measurement_times" ("id");

ALTER TABLE "scd30_fswebcam_leaven_monitor"."images" ADD FOREIGN KEY ("ts_id") REFERENCES "scd30_fswebcam_leaven_monitor"."measurement_times" ("id");
