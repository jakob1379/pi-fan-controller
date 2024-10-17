import logging
import time
from datetime import datetime
from typing import Optional
from gpiozero import OutputDevice
from typer import Option, Typer
from fancy_logging import setup_logging
import os
from pathlib import Path

setup_logging()

app = Typer()

def append_new_line(file_name: Path, text_to_append: str, header: Optional[str] = None):
    """Append given text as a new line at the end of file"""
    # Check if the file exists
    file_exists = file_name.exists()
    
    # Open the file in append & read mode ('a+')
    with file_name.open("a+") as file_object:
        # If the file does not exist, write the header
        if not file_exists and header:
            file_object.write(header + "\n")
        # Append text at the end of file with a new line
        file_object.write(text_to_append + "\n")

def get_temp() -> float:
    """Get the core temperature.

    Read file from /sys to get CPU temp in temp in C *1000

    Returns:
        float: The core temperature in degrees Celsius.
    """
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        temp_str = f.read()

    try:
        return float(temp_str) / 1000
    except (IndexError, ValueError,) as e:
        raise RuntimeError('Could not parse temperature output.')

@app.command()
def main(
    on_threshold: Optional[float] = Option(60, "-on", "--on-threshold", help="The temperature threshold (in degrees Celsius) at which to turn the fan on."),
    off_threshold: Optional[float] = Option(50, "-off", "--off-threshold", help="The temperature threshold (in degrees Celsius) at which to turn the fan off."),
    sleep_interval: Optional[int] = Option(10, "-s", "--sleep-interval", help="The interval (in seconds) at which to check the temperature."),
    gpio_pin: Optional[int] = Option(17, "-p", "--gpio-pin", help="The GPIO pin to use to control the fan."),
    data_dump: Optional[Path] = Option(None, "--data-dump", help="Optional file name to dump temperature data."),
    quiet: bool = Option(False, "-q", "--quiet", help="Disable console output."),
) -> None:
    """Monitor the core temperature of a Raspberry Pi and control a fan based on the temperature."""

    # Set logging level based on verbosity
    if not quiet:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.WARNING)

    # Validate the on and off thresholds
    if off_threshold >= on_threshold:
        raise RuntimeError('OFF_THRESHOLD must be less than ON_THRESHOLD')

    fan = OutputDevice(gpio_pin)

    # Header for the data dump file if provided
    header = "Datetime\tTemperature(C)\tFan State\tOn Threshold\tOff Threshold"

    while True:
        temp = get_temp()
        fan_state = 'on' if fan.value else 'off'
        logging.debug(f"Temperature: {temp:.2f}C\tFan: {fan_state}")

        if data_dump:
            append_new_line(data_dump, f"{datetime.now()}\t{temp}\t{fan.value}\t{on_threshold}\t{off_threshold}", header=header)

        # Start the fan if the temperature has reached the limit and the fan isn't already running.
        if temp > on_threshold and not fan.value:
            logging.info(f"Turning fan on - Temperature: {temp:.2f}C > {on_threshold}C")
            fan.on()

        # Stop the fan if the fan is running and the temperature has dropped to 10 degrees below the limit.
        elif fan.value and temp < off_threshold:
            logging.info(f"Turning fan off - Temperature: {temp:.2f}C < {off_threshold}C")
            fan.off()

        time.sleep(sleep_interval)

if __name__ == "__main__":
    app()
