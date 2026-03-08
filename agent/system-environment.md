# system-environment.md — run environment (this project)

**For agents:** This file describes the **run environment** for this project—e.g. laptop, server, container, or embedded host. Use it when the WIP involves host, hardware, interfaces, or config. Do not guess; read the values here. *(Regenerate via `agent/setup.md` when moving to a new machine or run target.)*

## Critical constraints (don't violate)

- **GPIO logic level:** 3.3 V only. GPIO pins are **not** 5 V tolerant; connecting 5 V to a pin can damage the SoC.
- **Power pins:** 3.3 V (pin 1, 17) and 5 V (2, 4) are output only. GND: 6, 9, 14, 20, 25, 30, 34, 39.
- **Current:** Per-pin max ~16 mA; total from all 3.3 V pins within board limits. Use external drivers for higher current or 5 V logic.
- **Boot / special pins:** Avoid GPIO 3 (I2C SDA), 5 (I2C SCL), 27 (EEPROM ID) for unrelated outputs. Prefer other GPIO for generic outputs.

**Best practices (Pi GPIO):** Release GPIO on exit (set to input or close handle) so pins aren't left driving or floating. Set pull-up/pull-down for inputs (e.g. buttons) so state isn't undefined. Don't connect or disconnect wires while a pin is active—power off or set pin to input first. Only one process should control a given GPIO at a time. Prefer gpiozero or rpi-lgpio (installed); avoid legacy RPi.GPIO on this OS.

## Config path

- **Firmware/boot:** `/boot/firmware/config.txt`. Edit with `sudo`; changes take effect after reboot.

## Pinout (Pi 4, 40-pin header)

| Physical | BCM | Notes        | Physical | BCM | Notes        |
|----------|-----|--------------|----------|-----|--------------|
| 1        | —   | 3.3 V        | 2        | —   | 5 V          |
| 3        | 2   | SDA1 (I2C)   | 4        | —   | 5 V          |
| 5        | 3   | SCL1 (I2C)   | 6        | —   | GND          |
| 7        | 4   | GPCLK0       | 8        | 14  | TXD0 (UART)  |
| 9        | —   | GND          | 10       | 15  | RXD0 (UART)  |
| 11       | 17  |              | 12       | 18  | PCM_CLK      |
| 13       | 27  |              | 14       | —   | GND          |
| 15       | 22  |              | 16       | 23  |              |
| 17       | —   | 3.3 V        | 18       | 24  |              |
| 19       | 10  | MOSI (SPI)   | 20       | —   | GND          |
| 21       | 9   | MISO (SPI)   | 22       | 25  |              |
| 23       | 11  | SCLK (SPI)   | 24       | 8   | CE0 (SPI)    |
| 25       | —   | GND          | 26       | 7   | CE1 (SPI)    |
| 27       | 0   | EEPROM ID    | 28       | 1   | EEPROM ID    |
| 29       | 5   |              | 30       | —   | GND          |
| 31       | 6   |              | 32       | 12  |              |
| 33       | 13  |              | 34       | —   | GND          |
| 35       | 19  | MISO (SPI1)  | 36       | 16  |              |
| 37       | 26  |              | 38       | 20  | MOSI (SPI1)  |
| 39       | —   | GND          | 40       | 21  | SCLK (SPI1)  |

- **Code:** BCM = GPIO number (gpiozero/lgpio default). BOARD = physical 1–40. Prefer BCM unless user says BOARD.
- **I2C:** SDA GPIO 2 (pin 3), SCL GPIO 3 (pin 5). Device `/dev/i2c-1`.
- **SPI0:** MOSI 10, MISO 9, SCLK 11, CE0 8, CE1 7. Devices `/dev/spidev0.0`, `/dev/spidev0.1`.

## GPIO and interfaces

- **GPIO:** `/sys/class/gpio/`. Chips: gpiochip512 (SoC), gpiochip570 (firmware). Devices: `/dev/gpiochip0`, `/dev/gpiochip1`, `/dev/gpiochip4`, `/dev/gpiomem`. Group `gpio` has access.
- **UART:** `serial0` → `/dev/ttyS0`. Group `dialout`. Config `enable_uart=1`. Use `/dev/serial0` or `/dev/ttyS0`.
- **I2C/SPI:** User in groups `i2c`, `spi`. If `/dev/i2c*` or `/dev/spi*` missing, add to `/boot/firmware/config.txt`: `dtparam=i2c_arm=on`, `dtparam=spi=on`; reboot. Then `/dev/i2c-1`, `/dev/spidev0.*` appear.

## Hardware (reference)

| Board | Pi 4 Model B Rev 1.4. Revision c03114. Serial 100000005b98b44e |
| CPU | ARMv8 (aarch64), 4 cores, Cortex-A72 (0xd08) |
| Memory | 3.7 GiB RAM, 2 GiB swap (zram) |
| Storage | Root `/dev/mmcblk0p2` (~9.4 GiB free), boot `/boot/firmware` |
| Firmware | arm_freq 1800 MHz, enable_uart=1, throttled=0x0 |

## Software (reference)

| OS | Debian 13 (trixie), hostname mochi |
| Kernel | 6.12.47+rpt-rpi-v8 (aarch64) |
| Python | 3.13.5. gpiozero 2.0.1, rpi-lgpio 0.6 |
| Git | 2.47.3. gh 2.46.0. Default branch main, remote GitHub HTTPS (PAT). |
| User | mochi (uid 1000), groups include gpio, i2c, spi, dialout |
