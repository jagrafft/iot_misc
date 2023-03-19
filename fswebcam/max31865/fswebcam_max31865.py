import adafruit_max31865
import board
import digitalio
import logging

from os import makedirs
from pathlib import Path
from signal import SIGINT, signal
from subprocess import call
from sys import exit
from time import localtime, sleep, strftime

# Paths and Directories #
output_path = Path(
    Path.home() / f"max31865_fswebcam_{strftime('%Y-%m-%dT%H%M%S', localtime())}"
)

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
    log_logger: Logging.Logger,
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
            f"SUCCESS: {{ exit code = {subprocess_exit_code}, path = {img_path} }}"
        )
    else:
        log_logger.error(
            f"PROBLEM: {{ exit code = {subprocess_exit_code}, path = {img_path} }}"
        )


def sample_max31865(sensor: adafruit_max31865.MAX31865, rate: float) -> dict:
    while True:
        yield {"ohm": sensor.resistance, "C": sensor.temperature}
        sleep(rate)


# Data File #
session_data_file = open(
    Path(output_path / "max31865_readings.csv"), "w", encoding="utf-8"
)
session_data_file.write("timestamp,C,ohm\n")


# Program and File Close #
def stop_sampling_close_file(signum, frame):
    print("Closing...")
    print(f"signum: {signum}")
    print(f"frame: {frame}")

    session_data_file.close()
    exit()


# Listen for SIGINT
signal(SIGINT, stop_sampling_close_file)


# Sensor Object Instantiation #
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

for sample in sample_max31865(max31865_sensor, sample_rate):
    ts = localtime()
    timestamp = strftime("%Y-%m-%dT%H:%M:%S", ts)
    image_output_path = Path(
        image_path / f"{strftime('%Y-%m-%dT%H%M%S', ts)}.{_format}"
    )

    # No return value
    fswebcam_snapshot(
        "/dev/video0",
        0,
        "1024x768",
        "jpeg",
        85,
        timestamp,
        "arial",
        24,
        f"{sample['C']:.2f}C",
        image_output_path,
        logger,
    )

    row = ",".join(
        [
            timestamp,
            str(sample["C"]),
            str(sample["ohm"]),
        ]
    )

    session_data_file.writelines([row, "\n"])
