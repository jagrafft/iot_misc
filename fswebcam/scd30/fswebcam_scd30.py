import adafruit_scd30
import board
import busio
import digitalio
import logging
import redis

# Apache Arrow fails to compile on Raspberry Pi 4
# import pyarrow as py
# import pyarrow.parquet as pq

from io import BytesIO
from os import makedirs
from pathlib import Path
from psycopg_pool import ConnectionPool
from signal import SIGINT, signal
from subprocess import PIPE, Popen
from sys import exit, stdout
from time import localtime, sleep, strftime

# Sensor Object Instantiation #
# SCD-30
i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
scd30_sensor = adafruit_scd30.SCD30(i2c)

# Paths and Directories #
script_start_time = strftime("%Y-%m-%dT%H%M%S", localtime())
output_path = Path(Path.home() / f"scd30_fswebcam_{script_start_time}")
image_path = Path(output_path / "images")

makedirs(image_path)

# Logger #
logger = logging.getLogger("scd30_fswebcam_logger")
logger.setLevel(logging.DEBUG)
log_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler = logging.FileHandler(Path(output_path / "scd30_fswebcam.log"))
stream_handler = logging.StreamHandler(stdout)

file_handler.setFormatter(log_formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# NeonDB #
neon_db = {
    "db": "",
    "host": "",
    "port": 5432,
    "user": "",
    "password": "",
}

# Global variables (:vomit:) for tracking session indices
neondb_session_index = 1
neond_session_start_ts_id = 1

try:
    logger.info(
        f"Create Psycopg connection pool for NeonDB instance at '{neon_db['host']}:{neon_db['port']}', database '{neon_db['db']}'..."
    )
    pool = ConnectionPool(
        f"dbname={neon_db['db']} user={neon_db['user']} host={neon_db['host']} port={neon_db['port']}"
    )
    logger.info("SUCCESS")
except:
    logger.exception("Failed to create connection pool")
    logger.critical("EXIT")
    exit()

# Redis #
try:
    logger.info("Connect to Redis instance at 'localhost:6379', database 7...")
    redis_con = redis.Redis(host="127.0.0.1", port=6379, db=7)
    logger.info("CONNECTED")
    logger.info(f"XSTREAM: scd30_{script_start_time}")
except:
    logger.exception("Failed to connect to Redis instance")
    logger.critical("EXIT")
    exit()

# Functions #
def fswebcam_snapshot(
    device: str,
    _input: int,
    resolution: str,
    _format: str,
    quality: int,
    timestamp: str,
    font: str,
    font_size: int,
    label: str,
    img_path: Path,
) -> BytesIO:

    cmd = [
        "fswebcam",
        "-d",
        device,
        "-i",
        str(_input),
        "-r",
        resolution,
        f"--{_format}",
        f"{quality}",
        "--timestamp",
        timestamp,
        "--font",
        f"{font}:{font_size}",
        "--info",
        f"{label}",
        img_path,
    ]

    try:
        with Popen(cmd, stdout=PIPE) as p, BytesIO() as buf:
            for line in p.stdout:
                buf.write(line)

            return buf.getvalue()
    except:
        return b""


def sample_scd30(sensor: adafruit_scd30.SCD30) -> dict:
    while True:
        data_sample = {}

        if sensor.data_available:
            data_sample["timestamp"] = strftime("%Y-%m-%dT%H:%M:%S", localtime())
            data_sample["CO2"] = sensor.CO2
            data_sample["C"] = sensor.temperature
            data_sample["RH"] = sensor.relative_humidity

        yield data_sample


"""
def xstream_to_parquet(stream: str) -> pa.Table:
    rows = {
        x[0].decode(): {k.decode(): v.decode() for (k, v) in x[1].items()}
        for x in redis_con.xrange(f"{stream}")
    }

    d = {"timestamp": [], "CO2": [], "C": [], "RH": []}

    for row in rows.items():
        for k in row[1].keys():
            d[k].append(row[1][k])

    d["timestamp"] = pa.array(d["timestamp"], pa.string())
    d["CO2"] = pa.array([float(v) for v in d["CO2"]], type=pa.float64())
    d["C"] = pa.array([float(v) for v in d["C"]], type=pa.float64())
    d["RH"] = pa.array([float(v) for v in d["RH"]], type=pa.float64())

    return pa.table(d)
"""


# Program and File Close #
def halt_sampling(signum, frame):
    logger.info("SIGINT issued, halting...")

    # Apache Arrow fails to compile on Raspberry Pi 4
    """
    stream = f"scd30_{script_start_time}"
    pq_path = Path(output_path / f"{stream}.parquet")

    try:
        logger.info(f"Generating Apache Parquet Table from Redis Stream '{stream}'...")
        pq_table = xstream_to_parquet(stream)
        logger.info("SUCCESS")

        try:
            logger.info(f"Writing Parquet file to '{pq_path}'...")
            pq.write_table(pq_table, pq_path)
            logger.info("SUCCESS")
        except:
            logger.exception(f"Failed to write Parquet file")
    except:
        logger.exception("Failed to generate Parquet")
    """

    # Write session information to Neon database
    try:
        logger.info(
            f"Write session information to '{neon_db['host']}:{neon_db['port']}', database '{neon_db['db']}'..."
        )
        conn = pool.getconn()
        cur = conn.cursor()

        cur.execute("SELECT MAX(id) FROM rpi.sample_times;")
        neondb_session_end_ts_id = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO rpi.sessions (session_id,start_ts_id,end_ts_id) VALUES (%s,%s,%s);",
            (
                neondb_session_index,
                neondb_session_start_ts_id,
                neondb_session_end_ts_id,
            ),
        )
    except BaseException:
        logging.exception("Could not write session info")
        logging.critical("EXIT")
        exit()
    else:
        conn.commit()
        logger.info("SUCCESS")
    finally:
        cur.close()
        pool.putconn(conn)

    # Close Psycopg connection pool
    pool.close()

    logger.info("'Graceful' shutdown complete")
    logger.info(f"signum: {signum}")
    logger.info(f"frame: {frame}")
    logger.info("HALTED")

    exit()


# Listen for SIGINT
signal(SIGINT, halt_sampling)


# Data Sample Loop #
# `sample_rate` must be >= 1.0 to avoid filename collisions
sample_rate = 27.9  # seconds
img_format = "jpeg"

scd30_stream = sample_scd30(scd30_sensor)

# Initialize Neon database for session #
# Determine Starting Index for Timestamps
next_ts_id = 1
try:
    logger.info(
        f"Get index of most recent timestamp in '{neon_db['host']}:{neon_db['port']}', database '{neon_db['db']}'..."
    )
    conn = pool.getconn()
    cur = conn.cursor()
    cur.execute("SELECT MAX(id) FROM rpi.sample_times;")
    max_sample_time_id = cur.fetchone()

    if not isinstance(max_sample_time_id[0], type(None)):
        neondb_session_start_ts_id = max_sample_time_id[0]
        next_ts_id = max_sample_time_id[0] + 1

except BaseException:
    logging.exception("Could not query index")
    logging.critical("EXIT")
    exit()
else:
    conn.commit()
    logger.info("SUCCESS")
finally:
    cur.close()
    pool.putconn(conn)

# Write session identifier to Neon database
try:
    logger.info(
        f"Write session info to '{neon_db['host']}:{neon_db['port']}', database '{neon_db['db']}'..."
    )
    conn = pool.getconn()
    cur = conn.cursor()

    cur.execute("SELECT MAX(id) FROM rpi.session_ids;")
    max_session_id = cur.fetchone()

    if not isinstance(max_session_id[0], type(None)):
        neondb_session_index = max_session_id[0] + 1

    cur.execute(
        "INSERT INTO rpi.session_ids (id,label) VALUES (%s,%s);",
        (neondb_session_index, f"scd_{script_start_time}"),
    )
except BaseException:
    logging.exception("Could not write session info")
    logging.critical("EXIT")
    exit()
else:
    conn.commit()
    logger.info("SUCCESS")
finally:
    cur.close()
    pool.putconn(conn)

#

sleep(5)

for scd30_sample in scd30_stream:
    logging.info("Perform post processing on sample...")
    ts = localtime()
    timestamp = strftime("%Y-%m-%dT%H:%M:%S", ts)

    image_output_path = Path(
        image_path / f"{strftime('%Y-%m-%dT%H%M%S', ts)}.{img_format}"
    )

    # Format banner text for photograph
    banner_text = []

    if "C" in scd30_sample:
        banner_text.append(f"{scd30_sample['C']:.2f}C")

    if "CO2" in scd30_sample:
        banner_text.append(f"{scd30_sample['CO2']:.2f}ppm(CO2)")

    if "RH" in scd30_sample:
        banner_text.append(f"{scd30_sample['RH']:.2f}RH")

    data_banner = ""

    if banner_text:
        if len(data_banner) > 0:
            data_banner += "; "

        data_banner += "scd30: "
        data_banner += ", ".join(banner_text)

    # Take photograph, capture exit code
    logging.info("Take photograph with 'fswebcam'...")
    fswebcam_raw_data = fswebcam_snapshot(
        "/dev/video0",
        0,
        "960x720",
        img_format,
        85,
        timestamp,
        "arial",
        18,
        data_banner,
        "-",  # output to `stdout`
    )

    # Write file, if appropriate, and log result of `fswebcam` call
    if len(fswebcam_raw_data) > 0:
        try:
            with open(image_output_path, "wb") as img_out:
                img_out.write(fswebcam_raw_data)

            logger.info(f"SUCCESS: image written to '{image_output_path}'")
        except Exception:
            logger.exception(f"Could not write to '{image_output_path}'")
    else:
        logger.error(
            f"ERROR: zero (0) bytes returned, nothing written to '{image_output_path}'"
        )

    if scd30_sample:
        # Write data to Redis Streams
        try:
            logger.info(f"Write data to Redis Stream 'scd30_{script_start_time}'")
            redis_con.xadd(f"scd30_{script_start_time}", scd30_sample)
            logger.info("SUCCESS")
        except Exception:
            logger.exception("Could not write to Redis Stream")

        # Write to NeonDB database
        try:
            logger.info(f"Committing data to NeonDB database '{neon_db['db']}'...")
            conn = pool.getconn()
            cur = conn.cursor()

            cur.execute("SELECT MAX(id) FROM rpi.sample_times;")
            max_sample_time_id = cur.fetchone()

            if not isinstance(max_sample_time_id[0], type(None)):
                next_ts_id = max_sample_time_id[0] + 1

            cur.execute(
                "INSERT INTO rpi.sample_times VALUES (%s,%s);",
                (next_ts_id, f"{strftime('%Y-%m-%d %H:%M:%S', ts)} {ts.tm_zone}"),
            )

            if "C" in scd30_sample:
                cur.execute(
                    "INSERT INTO scd30.degrees_celsius VALUES (%s,%s);",
                    (next_ts_id, scd30_sample["C"]),
                )

            if "CO2" in scd30_sample:
                cur.execute(
                    "INSERT INTO scd30.carbon_dioxide VALUES (%s,%s);",
                    (next_ts_id, scd30_sample["CO2"]),
                )

            if "RH" in scd30_sample:
                cur.execute(
                    "INSERT INTO scd30.relative_humidity VALUES (%s,%s);",
                    (next_ts_id, scd30_sample["RH"]),
                )

            if len(fswebcam_raw_data) > 0:
                cur.execute(
                    "INSERT INTO rpi.images VALUES (%s,%s);",
                    (next_ts_id, fswebcam_raw_data),
                )
        except BaseException:
            logging.exception("Error with Psycopg connection or cursor, rolling back")
            conn.rollback()
        else:
            conn.commit()
            logger.info("SUCCESS")
        finally:
            cur.close()
            pool.putconn(conn)

    sleep(sample_rate)
