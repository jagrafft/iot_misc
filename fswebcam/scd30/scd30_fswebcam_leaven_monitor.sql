CREATE SCHEMA "rpi";

CREATE SCHEMA "scd30";

CREATE TABLE "rpi"."images" (
  "ts_id" INTEGER PRIMARY KEY,
  "img_blob" BYTEA NOT NULL
);

CREATE TABLE "rpi"."sample_times" (
  "id" INTEGER PRIMARY KEY,
  "ts" TIMESTAMP WITH TIME ZONE UNIQUE NOT NULL
);

CREATE TABLE "rpi"."sessions" (
  "session_id" INTEGER PRIMARY KEY,
  "start_ts_id" INTEGER NOT NULL,
  "end_ts_id" INTEGER NOT NULL
);

CREATE TABLE "rpi"."session_ids" (
  "id" INTEGER PRIMARY KEY,
  "label" TEXT UNIQUE NOT NULL
);

CREATE TABLE "scd30"."carbon_dioxide" (
  "ts_id" INTEGER PRIMARY KEY,
  "CO2" NUMERIC(16,9) NOT NULL
);

CREATE TABLE "scd30"."degrees_celsius" (
  "ts_id" INTEGER PRIMARY KEY,
  "C" NUMERIC(16,9) NOT NULL
);

CREATE TABLE "scd30"."relative_humidity" (
  "ts_id" INTEGER PRIMARY KEY,
  "RH" NUMERIC(16,9) NOT NULL
);

CREATE UNIQUE INDEX ON "rpi"."sessions" ("session_id", "start_ts", "end_ts");

CREATE UNIQUE INDEX ON "scd30"."carbon_dioxide" ("ts_id", "CO2");

CREATE UNIQUE INDEX ON "scd30"."degrees_celsius" ("ts_id", "C");

CREATE UNIQUE INDEX ON "scd30"."relative_humidity" ("ts_id", "RH");

COMMENT ON TABLE "rpi"."images" IS 'fswebcam utlity';

COMMENT ON TABLE "rpi"."sample_times" IS 'Raspberry Pi clock';

COMMENT ON TABLE "rpi"."sessions" IS 'Timestamp range for each session';

COMMENT ON TABLE "rpi"."session_ids" IS 'Integer ids and text labels for sessions';

COMMENT ON TABLE "scd30"."carbon_dioxide" IS 'Adafruit SCD30';

COMMENT ON TABLE "scd30"."degrees_celsius" IS 'Adafruit SCD30';

COMMENT ON TABLE "scd30"."relative_humidity" IS 'Adafruit SCD30';

ALTER TABLE "rpi"."images" ADD FOREIGN KEY ("ts_id") REFERENCES "rpi"."sample_times" ("id");

ALTER TABLE "rpi"."sessions" ADD FOREIGN KEY ("session_id") REFERENCES "rpi"."session_ids" ("id");

ALTER TABLE "rpi"."sessions" ADD FOREIGN KEY ("start_ts_id") REFERENCES "rpi"."sample_times" ("id");

ALTER TABLE "rpi"."sessions" ADD FOREIGN KEY ("end_ts_id") REFERENCES "rpi"."sample_times" ("id");

ALTER TABLE "scd30"."carbon_dioxide" ADD FOREIGN KEY ("ts_id") REFERENCES "rpi"."sample_times" ("id");

ALTER TABLE "scd30"."degrees_celsius" ADD FOREIGN KEY ("ts_id") REFERENCES "rpi"."sample_times" ("id");

ALTER TABLE "scd30"."relative_humidity" ADD FOREIGN KEY ("ts_id") REFERENCES "rpi"."sample_times" ("id");
