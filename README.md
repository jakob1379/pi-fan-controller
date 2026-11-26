# Pi Fan Controller

<p align="center">
  <img src=".github/assets/fan-loop.svg" width="100%" alt="pi-fan monitor reading the Raspberry Pi core temperature every 10 seconds: when a reading passes 60 °C, GPIO 17 goes high and the fan spins; the fan stays on while the temperature falls through the 50–60 °C band and switches off once a reading drops below 50 °C, with the matching log lines shown underneath.">
</p>

`pi-fan` keeps a Raspberry Pi cool without keeping it loud. It reads the core temperature, switches a fan on a GPIO pin when the Pi runs hot, and switches it off again once it has cooled down. Run it in a terminal to watch it work, or install it as a systemd user service and forget about it.

## How it works

Every `--sleep-interval` seconds (10 by default), `pi-fan monitor`:

1. reads the CPU temperature from `/sys/class/thermal/thermal_zone0/temp`;
2. turns the fan on if the temperature is above the **on** threshold (60 °C);
3. turns the fan off if the temperature is below the **off** threshold (50 °C).

Between the two thresholds the fan keeps whatever state it is in. That gap stops the fan from flicking on and off around a single set point. The off threshold must be lower than the on threshold, or `monitor` refuses to start.

The fan is driven through [gpiozero](https://gpiozero.readthedocs.io/) as a plain on/off output on GPIO 17 by default. A GPIO pin cannot power a fan by itself, so switch the fan through a transistor or similar driver.

## Installation

Requires Python 3.12 or newer.

```bash
uv tool install pi-fan-controller
pipx install pi-fan-controller
```

## Quick start

Watch it run in the foreground:

```console
$ pi-fan monitor
```

Run it in the background as a service, starting with your user session:

```console
$ pi-fan service install
$ pi-fan service start
```

Pass the same options to `service install` as you would to `monitor` (except `--data-dump`); they are written into the service file.

## Configuration

Every option can also be set with an environment variable.

| Option | Environment variable | Default | Description |
| --- | --- | --- | --- |
| `-on`, `--on-threshold FLOAT` | `ON_THRESHOLD` | `60` | Temperature (°C) at which to turn the fan on. |
| `-off`, `--off-threshold FLOAT` | `OFF_THRESHOLD` | `50` | Temperature (°C) at which to turn the fan off. |
| `-s`, `--sleep-interval INTEGER` | `SLEEP_INTERVAL` | `10` | Seconds between temperature checks. |
| `-p`, `--gpio-pin INTEGER` | `GPIO_PIN` | `17` | GPIO pin that controls the fan. |
| `--log-level [DEBUG\|INFO\|WARNING\|ERROR\|CRITICAL]` | `LOG_LEVEL` | `INFO` | Log level. |
| `--data-dump PATH` | `DATA_DUMP` | none | `monitor` only. Append every reading to a tab-separated file. |

With `--data-dump`, each line holds the time, temperature (°C), fan state (`0` or `1`), on threshold and off threshold. A header row is written when the file is created.

## Commands

```console
$ pi-fan [OPTIONS] COMMAND [ARGS]...
```

### `pi-fan monitor`

Monitor the core temperature of a Raspberry Pi and control a fan based on the temperature.

```console
$ pi-fan monitor [OPTIONS]
```

### `pi-fan service`

Manage the service for this application.

```console
$ pi-fan service [OPTIONS] ACTION:{install|remove|start|stop}
```

| Action | What it does |
| --- | --- |
| `install` | Writes `~/.config/systemd/user/fan_control.service` with your options as environment variables, reloads systemd and enables the service. |
| `start` | Starts the service. |
| `stop` | Stops the service. |
| `remove` | Disables the service. The service file is left in place. |

The service is a systemd *user* service, so it starts with your login session. To have it run at boot without logging in, enable lingering for your user with `loginctl enable-linger`.

Both commands accept `--help`.

## Credits

This project was inspired by the [Howchoo Pi Fan Controller][howchoo-repo]. While the current codebase has undergone significant changes and enhancements, the foundational idea originated from their work.

[howchoo-repo]: https://github.com/Howchoo/pi-fan-controller

## References

- [Control Your Raspberry Pi Fan (and Temperature) with Python](https://howchoo.com/g/ote2mjkzzta/control-raspberry-pi-fan-temperature-python): a detailed guide on controlling a Raspberry Pi fan using Python.
- [Control a Cooling Fan on a Raspberry Pi 3](https://www.instructables.com/Control-a-Cooling-Fan-on-a-Raspberry-Pi-3/): an Instructables project for controlling a cooling fan on a Raspberry Pi.
- [Add a Silent Fan to your Raspberry Pi 4](https://medium.com/home-wireless/add-a-silent-fan-to-your-raspberry-pi-4-e63ec64f8115): insights on fine-grained PWM control for silent operation.

## License

MIT License
