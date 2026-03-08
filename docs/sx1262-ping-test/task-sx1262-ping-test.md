# Task: SX1262 ping test (two chips)

**Feature details and active state:** See `feature.md` in this folder (wiring, code, what works).

**Branch:** `main--sx1262-ping-test`. One branch per task; cleanup pushes to this branch.

**Hardware context:** `docs/system-environment.md` (pinout, 3.3V only, BCM numbering, SPI).

---

## Planned

- Implement a ping test: one chip sends a ping packet; the other receives it and sends a reply; first chip receives the reply. Report success/failure (e.g. round-trip time or pass/fail).
- Document code paths and usage in the feature doc when done.

---

## In progress

- **Get SPI communication working** with both Wio-SX1262 modules on the Pi 4. Wiring is complete (see `wiring.md`). Software must: wait for BUSY low before/after each SPI transaction; drive NSS (CE0 for module A, CE1 for B); use RST for reset, RF_SW for RX/TX. Once the host can talk to both chips over SPI, implement the ping test. (User had difficulty with ESP32; Pi 4 + this wiring is the current setup.)

---

## Completed

- Created feature folder and docs (`feature.md`, task doc, `wio-sx1262-module.md`, `wiring.md`).
- Documented Wio-SX1262 module (pinout, BUSY/DIO1/RF_SW/TCXO, reference design) in `wio-sx1262-module.md`.
- Defined and documented wiring for two modules to Pi 4 (pin tables, board labels for XIAO carrier, wire colors, step-by-step) in `wiring.md`.
- **Wiring built:** two Wio-SX1262 for XIAO carriers on Pi 4 via breadboard; as-built notes (GND rail, grey/white for A/B DIO1 and RF_SW, kit antennas) in `wiring.md`.
