# SX1262 connection tests (GPIO and SPI)

This module tests two Wio-SX1262 sub‑GHz modules on a Raspberry Pi: a **GPIO test** (reset, BUSY, DIO1), a **SPI test** (GetStatus over SPI), and a **ping test** (LoRa A→B→A). For up-to-date state (wiring, what works, what doesn’t), see **`context/current-state.md`**.

---

## Project

This project is for experimenting with GPIO and interfacing with chips on a Raspberry Pi (e.g. Pi 4). The repo may have a single module or several; either is fine. This module adds SX1262 sub‑GHz radio tests (GPIO, SPI, LoRa ping) using two Wio-SX1262 modules.

---

## Best practices

When suggesting wiring or hardware steps: **(1) Wiring** — Spell out what to connect where (pin numbers, names), in what order (e.g. power off first, GND before signal). Do not assume prior experience. **(2) Safety** — Warn about risks (short circuits, 5 V on GPIO, hot-plugging, reversed polarity, current limits). State the risk and how to avoid it. For pinout and 3.3 V constraints, use **`agent/system-environment.md`**. **(3) SPI/hardware** — Respect BUSY and NSS discipline; wait for BUSY low before/after each SPI transfer. One process per module’s GPIOs. Antenna or 50 Ω load on each radio before TX. Release GPIOs on exit.

---

## Overview

- **GPIO test** — Resets both modules via NRST, drives RF_SW, reads BUSY and DIO1. Confirms wiring and that the chips respond.
- **SPI test** — Sends GetStatus (0xC0) to each module over SPI. Confirms SPI and BUSY/NSS discipline. See **`context/spi-test-explained.md`** for details.
- **Ping test** — LoRa: Module A sends "ping", B receives and replies "pong", A receives. See **`context/ping-test-summary.md`** for flow and current result.

Pins are defined in `pin_config.py` from **`context/wiring.md`** (BCM).

---

## How to run

From the repo root, on a Pi with both modules wired per **`context/wiring.md`**:

**GPIO test** (needs gpiozero):

```bash
python3 sx1262_gpio_test/test_connection.py
python3 sx1262_gpio_test/test_connection.py --output sx1262_gpio_test/results.txt
```

**SPI test** (after GPIO test passes; needs spidev, SPI enabled):

```bash
python3 sx1262_gpio_test/test_spi.py
python3 sx1262_gpio_test/test_spi.py --output sx1262_gpio_test/spi_results.txt
```

See **`context/spi-test-explained.md`** for what the test does and how to interpret results.

**Ping test** (LoRa A→B→A):

```bash
python3 sx1262_gpio_test/test_ping.py
python3 sx1262_gpio_test/test_ping.py --output sx1262_gpio_test/ping_results.txt
```

See **`context/ping-test-summary.md`** for flow and current result.

**Minimal status test** (Module A only):

```bash
python3 sx1262_gpio_test/test_status_minimal.py
```

Resets Module A, runs full LoRa init, calls `start_tx()`, then prints GetStatus.

---

## Deeper docs (in context/)

- `context/current-state.md` — Current state (for agents): wiring, code, working, not working, refs.
- `context/wip-sx1262-ping-test.md` — WIP progress and **Context for next session** handoff.
- `context/ping-test-summary.md` — Ping test flow, current result, what we learned, next directions.
- `context/spi-test-explained.md` — What the SPI test does and how to interpret GetStatus.
- `context/wiring.md` — Pin table (Pi ↔ Module A/B), safety, as-built notes.
- `context/wio-sx1262-module.md` — Module pinout and operation (TCXO, RF_SW, BUSY).
- `context/datasheet-and-an-notes.md` — Datasheet/AN excerpts (commands, TCXO, calibration, errors).

---

## Related WIP doc(s)

- `context/wip-sx1262-ping-test.md` — WIP progress for ping test (branch main--sx1262-ping-test).
