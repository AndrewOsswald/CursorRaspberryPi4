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
- **Code:** None yet. Next: bring up SPI (wait BUSY, drive NSS, reset via RST; see `wiring.md` Software notes and `wio-sx1262-module.md`), then implement ping (one chip sends, other replies, first receives).
- **Working:** Hardware wired; SPI and ping not yet verified.
- **Not working / limitations:** Chips have not been confirmed talking over SPI (user had trouble on ESP32; Pi 4 chosen as host; wiring complete, software next).

---

## Deeper docs (in this folder)

- **`wio-sx1262-module.md`** — Wio-SX1262 module description: pinout, SPI/BUSY/DIO1/RF_SW, TCXO and DIO3, RF switch and DIO2, electrical specs, reference design for connecting to an MCU, and variants (IPEX vs -N).
- **`wiring.md`** — Wiring two Wio-SX1262 modules to a Raspberry Pi 4: pin table, step-by-step procedure, safety, SPI enable, and software notes (BUSY, NSS, NRST, RF_SW).

---

## Related task doc(s)

- `task-sx1262-ping-test.md` in this folder — task progress (planned / in progress / completed) for the initial ping-test feature.
