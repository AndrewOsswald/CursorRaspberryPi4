# Feature: SX1262 radio ping test

**Written for both humans and AI.** Branches are per task (see each task doc for **Branch:** `main--<task-slug>`). Cleanup pushes to the active task’s branch.

---

## Overview

- **What it is:** A test that uses two SX1262 sub‑GHz radio chips to verify they can talk to each other by “pinging” one from the other (send a packet, receive a reply).
- **Purpose:** Validate that both chips are wired and driven correctly before building higher-level radio features.

---

## Active state

Update this section as the feature changes (wiring, code paths, host setup, what’s working or broken). Chip-specific details (pins, SPI, host, libraries) will be filled in once provided.

- **Wiring:** Two Wio-SX1262 modules to Pi 4 GPIO: see **`wiring.md`** in this folder (SPI0 shared, CE0/CE1 for NSS, dedicated GPIOs per module for NRST, BUSY, DIO1, RF_SW).
- **Code:** TBD — script or program that initiates ping from one chip and replies from the other; paths to be added here.
- **Working:** (none yet)
- **Not working / limitations:** Feature not implemented yet; documentation only.

---

## Deeper docs (in this folder)

- **`wio-sx1262-module.md`** — Wio-SX1262 module description: pinout, SPI/BUSY/DIO1/RF_SW, TCXO and DIO3, RF switch and DIO2, electrical specs, reference design for connecting to an MCU, and variants (IPEX vs -N).
- **`wiring.md`** — Wiring two Wio-SX1262 modules to a Raspberry Pi 4: pin table, step-by-step procedure, safety, SPI enable, and software notes (BUSY, NSS, NRST, RF_SW).

---

## Related task doc(s)

- `task-sx1262-ping-test.md` in this folder — task progress (planned / in progress / completed) for the initial ping-test feature.
