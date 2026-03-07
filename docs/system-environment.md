# System environment

Hardware and software baseline for this Raspberry Pi GPIO/chip-interfacing project. Generated from live system queries.

**For AI context:** Use this file when answering questions that depend on hardware, GPIO, or interfaces.

---

## Critical constraints (don’t violate)

- **GPIO logic level:** 3.3 V only. GPIO pins are **not** 5 V tolerant; connecting 5 V to a pin can damage the SoC.
- **Power pins:** 3.3 V (pin 1, 17) and 5 V (2, 4) are output only; use for powering external logic at 3.3 V or 5 V. GND: 6, 9, 14, 20, 25, 30, 34, 39.
- **Current:** Per-pin max ~16 mA; total from all 3.3 V pins combined should stay within board limits. Use external drivers (e.g. level shifters, MOSFETs) for higher current or 5 V logic.
- **Boot / special pins:** Avoid using GPIO 3 (I2C SDA), 5 (I2C SCL), 27 (EEPROM ID) for unrelated outputs; they have pull-ups and boot-time roles. Prefer other GPIO for generic outputs.

---

## Config file path

- **Firmware/boot config:** `/boot/firmware/config.txt` (Pi OS / Debian on Pi). Edit with `sudo`; changes take effect after reboot unless noted otherwise.

---

## Pinout quick reference (Pi 4, 40-pin header)

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

- **Pin numbering in code:** BCM (Broadcom) = GPIO number in Linux and in gpiozero/lgpio by default. BOARD = physical pin 1–40. When suggesting code, prefer BCM unless the user specifies BOARD.
- **I2C (default):** SDA = GPIO 2 (pin 3), SCL = GPIO 3 (pin 5). Device usually `/dev/i2c-1`.
- **SPI0:** MOSI 10, MISO 9, SCLK 11, CE0 8, CE1 7. Device `/dev/spidev0.0`, `/dev/spidev0.1`.

---

## Hardware

### Board

| Property | Value |
|----------|--------|
| **Model** | Raspberry Pi 4 Model B Rev 1.4 |
| **Revision** | c03114 |
| **Serial** | 100000005b98b44e |

### CPU

| Property | Value |
|----------|--------|
| **Architecture** | ARMv8 (aarch64), 64-bit |
| **Cores** | 4 |
| **Implementer** | ARM (0x41) |
| **Part** | Cortex-A72 (0xd08) |
| **BogoMIPS** | 108.00 per core |
| **Features** | fp, asimd, evtstrm, crc32, cpuid |

### Memory

| Property | Value |
|----------|--------|
| **Total RAM** | 3.7 GiB (4096 MB) |
| **Swap** | 2.0 GiB (zram) |
| **Config** | `total_mem=4096` |

### Storage

| Property | Value |
|----------|--------|
| **Root** | `/dev/mmcblk0p2` (14.4 GiB partition, ~9.4 GiB free) |
| **Boot** | `/dev/mmcblk0p1` @ `/boot/firmware` (512 MiB) |
| **Media** | SD card (mmcblk0, 14.9 GiB total) |

### Firmware / config (vcgencmd)

| Setting | Value |
|---------|--------|
| **arm_64bit** | 1 |
| **arm_boost** | 1 |
| **arm_freq** | 1800 MHz |
| **core_freq** | 500 MHz |
| **gpu_freq** | 500 MHz |
| **enable_uart** | 1 |
| **throttled** | 0x0 (no throttling) |
| **Temperature** | 52.5°C (at time of query) |

---

## Software

### Operating system

| Property | Value |
|----------|--------|
| **OS** | Debian GNU/Linux 13 (trixie) |
| **Version** | 13.2 (Debian 13.2) |
| **Codename** | trixie |
| **Hostname** | mochi |

### Kernel

| Property | Value |
|----------|--------|
| **Version** | 6.12.47+rpt-rpi-v8 |
| **Build** | #1 SMP PREEMPT Debian 1:6.12.47-1+rpt1 (2025-09-16) |
| **Architecture** | aarch64 GNU/Linux |
| **Toolchain** | gcc 14.2.0, GNU ld 2.44 |

This is a Raspberry Pi–specific kernel (rpt-rpi-v8).

### Python

| Property | Value |
|----------|--------|
| **Python 3** | 3.13.5 (`/usr/bin/python3`) |
| **python3-gpiozero** | 2.0.1 (GPIO control API) |
| **python3-rpi-lgpio** | 0.6 (lgpio-based RPi.GPIO compatibility) |

### User and permissions

| Property | Value |
|----------|--------|
| **User** | mochi (uid 1000) |
| **Groups** | adm, dialout, cdrom, sudo, audio, video, plugdev, games, users, netdev, **gpio**, **i2c**, **spi**, render, input |

Membership in `gpio`, `i2c`, and `spi` allows access to GPIO, I2C, and SPI without root for typical use.

---

## GPIO and interfaces

### GPIO (sysfs)

- **Path**: `/sys/class/gpio/`
- **Chips**: `gpiochip512` (main SoC GPIO), `gpiochip570` (firmware GPIO)
- **Devices**: `/dev/gpiochip0`, `/dev/gpiochip1`, `/dev/gpiochip4`, `/dev/gpiomem`
- **Kernel module**: `raspberrypi_gpiomem`

GPIO is available; the `gpio` group has access to the gpio sysfs and device nodes.

### UART (serial)

- **Primary UART**: `serial0` → `ttyS0` (`/dev/ttyS0`)
- **Permissions**: group `dialout` (user `mochi` is in `dialout`)
- **Config**: `enable_uart=1`

Use `/dev/serial0` or `/dev/ttyS0` for serial (e.g. USB–serial adapters or on-board UART).

### I2C and SPI

- **Kernel**: `i2c_brcmstb` loaded (I2C support present)
- **User groups**: `i2c`, `spi` (user `mochi` is in both)
- **Devices**: No `/dev/i2c*` or `/dev/spi*` were present at query time.

If I2C/SPI devices are missing, enable them with `raspi-config` (Interface Options → I2C / SPI) or by adding to `/boot/firmware/config.txt`:

- I2C: `dtparam=i2c_arm=on`
- SPI: `dtparam=spi=on`

Then reboot. After that, `/dev/i2c-1` and `/dev/spidev0.*` (and related) should appear when the interfaces are in use.

---

## Documentation folder

This file lives in the project’s **`docs/`** folder. You can add more markdown files here to describe:

- Overall project plan and goals
- Each hardware module or chip and how it’s connected
- Software components (e.g. scripts, libraries, services)
- Pinouts, wiring, and interface notes (I2C addresses, SPI modes, etc.)
- Build/run steps and troubleshooting

Keeping one file per “part” (e.g. `system-environment.md`, `project-overview.md`, `chip-xyz.md`) keeps things easy to navigate and update.
