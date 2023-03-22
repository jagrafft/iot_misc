import adafruit_scd30
import board
import busio
import digitalio
import logging
import redis

from io import BytesIO
from os import makedirs
from pathlib import Path
from signal import SIGINT, signal
from subprocess import PIPE, Popen
from sys import exit
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

# Redis #
redis_con = redis.ConnectionPool(host="127.0.0.1", port=6379, db=7)
print("## Redis ##")
print("DATABASE: 7")

# Logger for Program #
logger = logging.getLogger("scd30_fswebcam_logger")
logger.setLevel(logging.DEBUG)
log_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler = logging.FileHandler(Path(output_path / "scd30_fswebcam.log"))
file_handler.setFormatter(log_formatter)

logger.addHandler(file_handler)

# Sampling Functions #
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
        with Popen(cmd, stdout=PIPE, bufsize=1) as p, BytesIO() as buf:
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


# Program and File Close #
def halt_sampling(signum, frame):
    logger.info(f"SIGINT: {{ signum = {signum}, frame = {frame} }}")
    print("Halting...")
    print(f"signum: {signum}")
    print(f"frame: {frame}")

    exit()


# Listen for SIGINT
signal(SIGINT, halt_sampling)


# Data Sample Loop #
# `sample_rate` must be >= 1.0 to avoid filename collisions
sample_rate = 28.9  # seconds, accounts for ~1s execution time of `fswebcam`
img_format = "jpeg"

scd30_stream = sample_scd30(scd30_sensor)

sleep(5)

print("## Redis ##")
print(f"STREAM: scd30_{script_start_time}")

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

    # Write data to Redis Streams
    if scd30_sample:
        try:
            redis_con.xadd(f"scd30_{script_start_time}", scd30_sample)
            logger.info("SUCCESS: sensor data written to Redis Stream")
        except Exception:
            logger.exception("Could not write to Redis Stream")

    sleep(sample_rate)
