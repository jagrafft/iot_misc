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

# Paths and Directories #
script_start_time = strftime("%Y-%m-%dT%H%M%S", localtime())

output_path = Path(Path.home() / f"max31865_fswebcam_{script_start_time}")

image_path = Path(output_path / "images")

makedirs(image_path)


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
    log_logger: logging.Logger,
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

    subprocess_exit_code = call(cmd)

    if subprocess_exit_code == 0:
        log_logger.info(
            f"SUCCESS: {{ exit code = {subprocess_exit_code}, path = {image_output_path} }}"
        )
    else:
        log_logger.error(
            f"PROBLEM: {{ exit code = {subprocess_exit_code}, path = {image_output_path} }}"
        )


def sample_max31865(sensor: adafruit_max31865.MAX31865) -> dict:
    while True:
        data_sample = {}
        data_sample["timestamp"] = strftime("%Y-%m-%dT%H:%M:%S", localtime())

        if sensor.resistance:
            data_sample["ohm"] = sensor.resistance

        if sensor.temperature:
            data_sample["C"] = sensor.temperature

        return data_sample


def sample_scd41(sensor: adafruit_scd4x.SCD4X) -> dict:
    while True:
        data_sample = {}
        data_sample["timestamp"] = strftime("%Y-%m-%dT%H:%M:%S", localtime())

        if sensor.CO2:
            data_sample["CO2"] = sensor.CO2

        if sensor.temperature:
            data_sampe["C"] = sensor.temperature

        if sensor.relative_humidity:
            data_sample["RH"] = sensor.relative_humidity

        return data_sample


# Data Files #
# max31865_session_data_file = open(
#     Path(output_path / "max31865_readings.csv"), "w", encoding="utf-8"
# )
# max31865_session_data_file.write("timestamp,C,ohm\n")

# scd41_session_data_file = open(
#     Path(output_path / "scd41_readings.csv"), "w", encoding="utf-8"
# )
# scd41_session_data_file.write("timestamp,CO2,C,RH\n")

# Program and File Close #
def halt_sampling(signum, frame):
    log_logger.info("SIGINT: {{ signum = {signum}, frame = {frame} }}")
    print("Closing...")
    print(f"signum: {signum}")
    print(f"frame: {frame}")

    # max31865_session_data_file.close()
    # scd41_session_data_file.close()
    exit()


# Listen for SIGINT
signal(SIGINT, halt_sampling)


# Sensor Object Instantiation #
# SCD 41
scd41_sensor = adafruit_scd4x.SCD4X(board.I2C())
scd41_sensor.start_periodic_measurement()

sleep(1)

# MAX31865
max31865_sensor = adafruit_max31865.MAX31865(
    board.SPI(),
    digitalio.DigitalInOut(board.D5),
    rtd_nominal=1000.0,
    ref_resistor=4300.0,
    wires=3,
)


# Data Sample Loop #
# `sample_rate` must be >= 1.0 to avoid filename collisions
sample_rate = 28.9  # seconds, accounts for ~1s execution time of `fswebcam`
img_format = "jpeg"

max31865_stream = sample_max31865(max31865_sensor)
scd41_stream = sample_scd41(scd41_sensor)

for (max31865_sample, scd41_sample) in zip_longest(max31865_stream, scd41_stream):
    timestamp = strftime("%Y-%m-%dT%H:%M:%S", localtime())

    image_output_path = Path(
        image_path / f"{strftime('%Y-%m-%dT%H%M%S', ts)}.{img_format}"
    )

    banner_text = []

    if max31865_sample["C"]:
        banner_text.append(f"{max31865_sample['C']:.2f}C")

    if scd41_sample["CO2"]:
        banner_text.append(f"{scd41_sample['CO2']}ppm (CO2)")

    if scd41_sample["RH"]:
        banner_text.append(f"{scd41_sample['RH']:.2f}RH")

    # No return value
    fswebcam_snapshot(
        "/dev/video0",
        0,
        "1024x768",
        img_format,
        85,
        timestamp,
        "arial",
        18,
        ",".join(banner_text),
        image_output_path,
        logger,
    )

    # max31865_row = ",".join(
    #     [
    #         timestamp,
    #         str(max31865_sample["C"]),
    #         str(max31865_sample["ohm"]),
    #     ]
    # )

    # scd41_row = ",".join(
    #     [
    #         timestamp,
    #         str(scd41_sample["CO2"]),
    #         str(scd41_sample["C"]),
    #         str(scd41_sample["RH"]),
    #     ]
    # )

    # max31865_session_data_file.writelines([max31865_row, "\n"])
    # scd41_session_data_file.writelines([scd41_row, "\n"])

    redis_con.xadd(f"max31865_{script_start_time}", max31865_row)
    redis_con.xadd(f"scd41_{script_start_time}", scd41_row)

    sleep(sample_rate)
