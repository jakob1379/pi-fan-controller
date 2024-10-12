import logging
import time
from datetime import datetime
from typing import Optional
from gpiozero import OutputDevice
from typer import Option, Typer
from fancy_logging import setup_logging

setup_logging()

app = Typer()

def append_new_line(file_name, text_to_append):
    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)

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
) -> None:
    """Monitor the core temperature of a Raspberry Pi and control a fan based on the temperature."""

    # Validate the on and off thresholds
    if off_threshold >= on_threshold:
        raise RuntimeError('OFF_THRESHOLD must be less than ON_THRESHOLD')

    fan = OutputDevice(gpio_pin)

    while True:
        temp = get_temp()
        fan_state = 'on' if fan.value else 'off'
        logging.info(f"Temperature: {temp:.2f}C\tFan: {fan_state}")
        append_new_line("temp.dat", f"{datetime.now()}\t{temp}\t{fan.value}\t{on_threshold}\t{off_threshold}")
        
        # Start the fan if the temperature has reached the limit and the fan isn't already running.
        if temp > on_threshold and not fan.value:
            fan.on()

        # Stop the fan if the fan is running and the temperature has dropped to 10 degrees below the limit.
        elif fan.value and temp < off_threshold:
            fan.off()

        time.sleep(sleep_interval)

if __name__ == "__main__":
    app()    

