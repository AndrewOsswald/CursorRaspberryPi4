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

- **Ping test:** Code is in place (`sx1262_driver.py`, `test_ping.py`); run `python3 sx1262_gpio_test/test_ping.py`. Currently fails (chip does not leave STBY_RC on SetTx/SetRx). See `docs/sx1262-ping-test/PING_TEST_SUMMARY.md` for summary and next steps (CE mapping, init order, ref code).

---

## Completed

- **Ping test implemented and documented:** LoRa driver and `test_ping.py` (A→B ping, B→A pong); summary in `docs/sx1262-ping-test/PING_TEST_SUMMARY.md`. Test currently fails (mode-change commands not taking effect); doc lists next steps.
- **SPI test verified on hardware:** Ran `test_spi.py` on Pi after enabling SPI and reboot. Module A and Module B both returned GetStatus 0x00 (ChipMode STBY_RC). Both modules are reachable over SPI.
- **SPI test added:** `test_spi.py` sends GetStatus (0xC0) to both modules; waits BUSY before/after transfer; uses spidev0.0 / spidev0.1. Detailed explanation in `docs/sx1262-ping-test/SPI_TEST_EXPLAINED.md`. (Run on Pi with SPI enabled; this environment has no /dev/spidev.)
- **GPIO connection test:** Added `sx1262_gpio_test/` at repo root (see `feature.md`). Script resets both modules via NRST, drives RF_SW, reads BUSY and DIO1; both modules reported BUSY low after reset on Pi — wiring likely OK for SPI.
- Created feature folder and docs (`feature.md`, task doc, `wio-sx1262-module.md`, `wiring.md`).
- Documented Wio-SX1262 module (pinout, BUSY/DIO1/RF_SW/TCXO, reference design) in `wio-sx1262-module.md`.
- Defined and documented wiring for two modules to Pi 4 (pin tables, board labels for XIAO carrier, wire colors, step-by-step) in `wiring.md`.
- **Wiring built:** two Wio-SX1262 for XIAO carriers on Pi 4 via breadboard; as-built notes (GND rail, grey/white for A/B DIO1 and RF_SW, kit antennas) in `wiring.md`.
