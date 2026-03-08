# Feature: SX1262 radio ping test

**Written for both humans and AI.** Branches are per task (see each task doc for **Branch:** `main--<task-slug>`). Cleanup pushes to the active task’s branch.

---

## Overview

- **What it is:** A test that uses two SX1262 sub‑GHz radio chips to verify they can talk to each other by “pinging” one from the other (send a packet, receive a reply).
- **Purpose:** Validate that both chips are wired and driven correctly before building higher-level radio features.

---

## Active state

Update this section as the feature changes (wiring, code paths, host setup, what’s working or broken).

- **Wiring:** **Done.** Two **Wio-SX1262 for XIAO** carrier boards wired to Pi 4 per **`wiring.md`** (SPI0 shared, CE0/CE1 for NSS; GPIOs per module for RST, BUSY, DIO1, RF_SW; breadboard, wire colors as built). Module labels used: 3V3, GND, MOSI, MISO, SCK, NSS, RST, BUSY, DIO1, RF_SW, DO. Antennas on DO.
- **Code:** **`sx1262_gpio_test/`** at repo root: (1) **GPIO test** — `test_connection.py`. (2) **SPI test** — `test_spi.py`; see `docs/sx1262-ping-test/SPI_TEST_EXPLAINED.md`. (3) **Ping test** — `sx1262_driver.py` (LoRa init/TX/RX) and `test_ping.py` (A sends ping, B replies pong); see `docs/sx1262-ping-test/PING_TEST_SUMMARY.md`.
- **Working:** Hardware wired (NSS fixed: A = CE0, B = CE1); GPIO test passed; SPI test passed (A often 0xAA, B 0x00). Ping test runs through init and reaches “Module A: sending 'ping'…”.
- **Not working / limitations:** Ping test **fails (no TxDone)**; **error 0x200A** → RC13M_CALIB_ERR, ADC_CALIB_ERR (block calibration fails on chip). Driver uses Semtech init order (Calibrate+CalibrateImage before SetPacketType/SetRfFrequency), 2-byte CalibrateImage, regulator before XOSC; same error after reorder. See `PING_TEST_SUMMARY.md` **“What we learned (for next session)”** and task doc **“Context for next session”** for full handoff. Next: hardware (antennas, one-module test), or run known-good stack on same Pi and diff.

---

## Deeper docs (in this folder)

- **`wio-sx1262-module.md`** — Wio-SX1262 module description: pinout, SPI/BUSY/DIO1/RF_SW, TCXO and DIO3, RF switch and DIO2, electrical specs, reference design for connecting to an MCU, and variants (IPEX vs -N).
- **`wiring.md`** — Wiring two Wio-SX1262 modules to a Raspberry Pi 4: pin table, step-by-step procedure, safety, SPI enable, and software notes (BUSY, NSS, NRST, RF_SW).
- **`SPI_TEST_EXPLAINED.md`** — What the SPI test does (GetStatus 0xC0), BUSY/NSS discipline, and how to interpret results.
- **`PING_TEST_SUMMARY.md`** — Ping test flow, where the code lives, how to run it, current result (FAIL: SetTx/SetRx not changing mode), and next steps for a new agent.
- **`DATASHEET_AND_AN_NOTES.md`** — Key SX1262/Wio details extracted from Semtech datasheet, AN1200.59 (reference clock), and Seeed Wio-SX1262-N datasheet (TCXO delay formula, error register, Tx sequence, command order). Use when changing the driver or debugging; PDFs need not remain in the repo.

---

## Related task doc(s)

- `task-sx1262-ping-test.md` in this folder — task progress (planned / in progress / completed) for the initial ping-test feature.
