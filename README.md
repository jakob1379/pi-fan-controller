# Pi Fan Controller

A command-line tool to monitor your Raspberry Pi’s core temperature and control a fan automatically. It offers both a real‑time monitor and a systemd service to manage fan operation based on configurable temperature thresholds.

## Features

- **Temperature Monitoring:** Reads the CPU temperature from `/sys/class/thermal/thermal_zone0/temp`.
- **Fan Control:** Turns the fan on when the temperature exceeds a user-defined "on" threshold and off below an "off" threshold.
- **Service Management:** Easily install, start, stop, or remove the fan control service using the `pi-fan service` command.
- **CLI Interface:** Built with [Typer](https://typer.tiangolo.com/) for a modern, easy-to-use command-line experience.
- **GPIO Control:** Uses [gpiozero](https://gpiozero.readthedocs.io/) to control the fan via a specified GPIO pin.

## Installation
     
```bash
uv tool install pi-fan-controller
pipx install pi-fan-controller
```

# `CLI`

**Usage**:

```console
$ pi-fan [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `service`: Manage the service for this application...
* `monitor`: Monitor the core temperature of a...

## `pi-fan service`

Manage the service for this application (install, start, stop).

**Usage**:

```console
$ pi-fan service [OPTIONS] ACTION:{install|remove|start|stop}
```

**Arguments**:

* `ACTION:{install|remove|start|stop}`: [required]

**Options**:

* `-on, --on-threshold FLOAT`: The temperature threshold (in degrees Celsius) at which to turn the fan on.  [env var: ON_THRESHOLD; default: 60]
* `-off, --off-threshold FLOAT`: The temperature threshold (in degrees Celsius) at which to turn the fan off.  [env var: OFF_THRESHOLD; default: 50]
* `-s, --sleep-interval INTEGER`: The interval (in seconds) at which to check the temperature.  [env var: SLEEP_INTERVAL; default: 10]
* `-p, --gpio-pin INTEGER`: The GPIO pin to use to control the fan.  [env var: GPIO_PIN; default: 17]
* `--log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]`: Set the log level. Available options: DEBUG, INFO, WARNING, ERROR, CRITICAL  [env var: LOG_LEVEL; default: INFO]
* `--help`: Show this message and exit.

## `pi-fan monitor`

Monitor the core temperature of a Raspberry Pi and control a fan based on the temperature.

**Usage**:

```console
$ pi-fan monitor [OPTIONS]
```

**Options**:

* `-on, --on-threshold FLOAT`: The temperature threshold (in degrees Celsius) at which to turn the fan on.  [env var: ON_THRESHOLD; default: 60]
* `-off, --off-threshold FLOAT`: The temperature threshold (in degrees Celsius) at which to turn the fan off.  [env var: OFF_THRESHOLD; default: 50]
* `-s, --sleep-interval INTEGER`: The interval (in seconds) at which to check the temperature.  [env var: SLEEP_INTERVAL; default: 10]
* `-p, --gpio-pin INTEGER`: The GPIO pin to use to control the fan.  [env var: GPIO_PIN; default: 17]
* `--data-dump PATH`: Optional file name to dump temperature data.  [env var: DATA_DUMP]
* `--log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]`: Set the log level. Available options: DEBUG, INFO, WARNING, ERROR, CRITICAL  [env var: LOG_LEVEL; default: INFO]
* `--help`: Show this message and exit.

## Credits

This project was inspired by the [Howchoo Pi Fan Controller][howchoo-repo]. While the current codebase has undergone significant changes and enhancements, the foundational idea originated from their work.

[howchoo-repo]: https://github.com/Howchoo/pi-fan-controller


## References

- **Fan Control with Python:** A detailed guide on controlling a Raspberry Pi fan using Python.  
  [Control Your Raspberry Pi Fan (and Temperature) with Python](https://howchoo.com/g/ote2mjkzzta/control-raspberry-pi-fan-temperature-python) citeturn0search0
- **Instructables Tutorial:** An example project for controlling a cooling fan on a Raspberry Pi.  
  [Control a Cooling Fan on a Raspberry Pi 3](https://www.instructables.com/Control-a-Cooling-Fan-on-a-Raspberry-Pi-3/) citeturn0search6
- **Silent Fan on Raspberry Pi 4:** Insights on achieving fine-grained PWM control for a silent operation.  
  [Add a Silent Fan to your Raspberry Pi 4](https://medium.com/home-wireless/add-a-silent-fan-to-your-raspberry-pi-4-e63ec64f8115) citeturn0search7

## License

[MIT License](LICENSE)

