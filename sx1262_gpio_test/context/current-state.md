# Current state — SX1262 GPIO/SPI tests (for agents)

**Start here for this module.** You don't need the whole-project description—this file is the agent entry for this part of the project. It tells you what the code is and does, how it fits in the repo, the rules for working on it, and the current state. Update this file as the module changes.

---

## What this module is

Hardware tests for two **Wio-SX1262** sub‑GHz LoRa modules on one Raspberry Pi. The code is a small driver and several test scripts. **GPIO test:** resets both modules via NRST, drives RF_SW, reads BUSY and DIO1—confirms wiring and that the chips respond. **SPI test:** sends the SX1262 GetStatus command (0xC0) over SPI to each module; confirms SPI and BUSY/NSS discipline. **Ping test:** LoRa A→B (ping), B→A (pong); end-to-end packet exchange. Pins and SPI device mapping come from `pin_config.py` and `context/wiring.md`. Purpose: get both chips talking over SPI and LoRa so we can debug init, TX/RX, and calibration on this host.

---

## How it fits in the project

The repo may have one module or several (e.g. this SX1262 test plus other boards or stacks). Each module is a folder at repo root with its own README, context/, and code. This module is the SX1262 connectivity and LoRa ping test; it doesn't depend on other modules. You only need to understand this module to work on it.

---

## Rules for working on this module

- **Wiring:** Spell out what to connect where (pin numbers, names), in what order (e.g. power off first, GND before signal). Do not assume prior experience. Pin table and as-built notes are in **`context/wiring.md`**; hardware constraints in **`agent/system-environment.md`**.
- **Safety:** Warn about risks: short circuits, 5 V on GPIO, hot-plugging, reversed polarity, current limits. State the risk and how to avoid it. Each module can draw ~125 mA on TX; both on Pi 3.3 V is OK for normal use but watch for brownouts if stressing.
- **SPI / hardware discipline:** Wait for **BUSY** low before and after every SPI transfer. Only one process per module's GPIOs. Use NSS (CE0/CE1) correctly—Module A on CE0, B on CE1. Antenna or 50 Ω load on each radio before TX. Release GPIOs on exit.
- **Driver and tests:** When changing init or TX/RX sequence, align with datasheet and ref code (e.g. Semtech SX126xLib, RadioLib). ClearDeviceErrors payload is 0x00,0x00 (datasheet). CalibrateImage takes two band bytes. Log errors (e.g. decode_device_error) when debugging failures. See **`context/datasheet-and-an-notes.md`** and **`context/ping-test-summary.md`** for what's been tried and what to try next.

---

## Wiring

- Built per `context/wiring.md`. Two Wio-SX1262 on Pi 4: CE0 (Module A), CE1 (Module B), shared SPI, per-module GPIOs (NRST, BUSY, DIO1, RF_SW). Pin table and as-built notes in `context/wiring.md`.

## Code

- `pin_config.py` — BCM pin numbers for Module A and B (from wiring.md).
- `test_connection.py` — GPIO test; resets both modules, reads BUSY/DIO1.
- `test_spi.py` — SPI test; GetStatus (0xC0) to each module.
- `sx1262_driver.py` — LoRa driver (init, TX, RX, IRQ, buffer).
- `test_ping.py` — Ping test (A→B ping, B→A pong).
- `test_status_minimal.py` — Module A only: reset → init_lora → start_tx → status.

## Working

- GPIO test passes; both modules report BUSY low after reset.
- SPI test passes; both modules respond (GetStatus). NSS (CE0/CE1) correct.

## Not working / limitations

- Ping test fails — TX never completes; error 0x200A (RC13M_CALIB_ERR, ADC_CALIB_ERR). Details and next directions in `context/ping-test-summary.md` and WIP doc **Context for next session**.

## Next / refs

- **WIP:** `context/wip-sx1262-ping-test.md` (branch main--sx1262-ping-test). See **Context for next session** there for what's done, current failure, and what to try next.
- **Ping summary:** `context/ping-test-summary.md` — flow, what we learned, next directions.
- **Datasheet/AN:** `context/datasheet-and-an-notes.md` — commands, TCXO, calibration, errors.
- **Hardware:** `agent/system-environment.md` (pinout, 3.3 V, SPI).
