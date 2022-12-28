import adafruit_max31865
import adafruit_scd4x
import board
import digitalio
import logging

from itertools import zip_longest
from os import makedirs
from pathlib import Path
from redis import Redis
from signal import SIGINT, signal
from subprocess import call
from sys import exit
from time import localtime, sleep, strftime

# Sensor Object Instantiation #
# SCD 41
i2c = board.I2C()
scd41_sensor = adafruit_scd4x.SCD4X(i2c)
scd41_sensor.start_periodic_measurement()

sleep(1)

# MAX31865
spi = board.SPI()
d5 = digitalio.DigitalInOut(board.D5)
max31865_sensor = adafruit_max31865.MAX31865(
    spi,
    d5,
    rtd_nominal=1000.0,
    ref_resistor=4300.0,
    wires=3,
)

# Paths and Directories #
script_start_time = strftime("%Y-%m-%dT%H%M%S", localtime())

output_path = Path(Path.home() / f"max31865_fswebcam_{script_start_time}")

image_path = Path(output_path / "images")

makedirs(image_path)

# Redis #
redis_con = Redis(host="127.0.0.1", port=6379)
redis_con.select(7)
print("## Redis ##")
print("DATABASE: 7")

# Logger #
logger = logging.getLogger("max31865_fswebcam_logger")
logger.setLevel(logging.DEBUG)
log_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler = logging.FileHandler(Path(output_path / "max31865_fswebcam.log"))
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
):

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

    res = call(cmd)
    return res


def sample_max31865(sensor: adafruit_max31865.MAX31865) -> dict:
    while True:
        data_sample = {}
        data_sample["timestamp"] = strftime("%Y-%m-%dT%H:%M:%S", localtime())

        if sensor.resistance:
            data_sample["ohm"] = sensor.resistance

        if sensor.temperature:
            data_sample["C"] = sensor.temperature

        yield data_sample


def sample_scd41(sensor: adafruit_scd4x.SCD4X) -> dict:
    while True:
        data_sample = {}

        if sensor.data_ready:
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

max31865_stream = sample_max31865(max31865_sensor)
scd41_stream = sample_scd41(scd41_sensor)

print("## Redis ##")
print(f"STREAM: max31865_{script_start_time}")
print(f"STREAM: scd41_{script_start_time}")

for (max31865_sample, scd41_sample) in zip_longest(max31865_stream, scd41_stream):
    ts = localtime()
    timestamp = strftime("%Y-%m-%dT%H:%M:%S", ts)

    image_output_path = Path(
        image_path / f"{strftime('%Y-%m-%dT%H%M%S', ts)}.{img_format}"
    )

    # Format banner text for photograph
    banner_text = {"max": [], "scd": []}

    if "C" in max31865_sample:
        banner_text["max"].append(f"{max31865_sample['C']:.2f}C")

    if "C" in scd41_sample:
        banner_text["scd"].append(f"{scd41_sample['C']:.2f}C")

    if "CO2" in scd41_sample:
        banner_text["scd"].append(f"{scd41_sample['CO2']}ppm(CO2)")

    if "RH" in scd41_sample:
        banner_text["scd"].append(f"{scd41_sample['RH']:.2f}RH")

    data_banner = ""

    if banner_text["max"]:
        data_banner += "max: "
        data_banner += ", ".join(banner_text["max"])

    if banner_text["scd"]:
        if len(data_banner) > 0:
            data_banner += "; "

        data_banner += "scd: "
        data_banner += ", ".join(banner_text["scd"])

    # Take photograph, capture exit code
    fswebcam_exit_code = fswebcam_snapshot(
        "/dev/video0",
        0,
        "960x720",
        img_format,
        85,
        timestamp,
        "arial",
        18,
        data_banner,
        image_output_path,
    )

    # Log result of `fswebcam` call
    if fswebcam_exit_code == 0:
        logger.info(
            f"SUCCESS: {{ exit code = {fswebcam_exit_code}, path = {image_output_path} }}"
        )
    else:
        logger.error(
            f"PROBLEM: {{ exit code = {fswebcam_exit_code}, path = {image_output_path} }}"
        )

    # Write data to Redis Streams
    if max31865_sample:
        redis_con.xadd(f"max31865_{script_start_time}", max31865_sample)

    if scd41_sample:
        redis_con.xadd(f"scd41_{script_start_time}", scd41_sample)

    sleep(sample_rate)
