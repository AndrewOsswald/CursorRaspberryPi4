# WIP: SX1262 ping test (two chips)

**Module details and current state:** See **`context/current-state.md`** in this folder (wiring, code, what works). README in parent folder is for humans (overview, how to run).

**Branch:** `main--sx1262-ping-test`. One branch per WIP; cleanup pushes to this branch.

**Hardware context:** `agent/system-environment.md` (pinout, 3.3V only, BCM numbering, SPI).

---

## Planned

- Implement a ping test: one chip sends a ping packet; the other receives it and sends a reply; first chip receives the reply. Report success/failure (e.g. round-trip time or pass/fail).
- Document code paths and usage in the module README when done.

---

## In progress

- **Ping test:** Run `python3 sx1262_gpio_test/test_ping.py` on the Pi. Test reaches "Module A: sending 'ping'…" then **TX fails (no TxDone)**, **error = 0x200A**, status 0xAA. See **"Context for next session"** below and `ping-test-summary.md`.

---

## Context for next session

**For a fresh agent:** Read `agent/intro.md`, then this WIP doc and **`context/current-state.md`** (and `../README.md` for overview/run if needed), then `ping-test-summary.md` and `datasheet-and-an-notes.md` in this folder. For hardware (pinout, SPI), read `agent/system-environment.md`. That set gives you the context needed to continue. **Terminal runs on the Pi** (intro.md Execution environment); run `python3 sx1262_gpio_test/test_ping.py` on the Pi to reproduce.

**What's done:** NSS wiring was wrong (user fixed: Module A = CE0, B = CE1). SPI test passes (A 0xAA, B 0x00). Ping test flow: reset both → wait BUSY → init **B first**, then A → re-init B before RX → A clear_error, write buffer, start_tx. Driver: STBY_XOSC, SetTcxoMode with **delay 320** (5 ms, 15.625 µs units), **ClearDeviceErrors** right after SetStandby(0x01) in init_lora (XOSC_START_ERR at POR expected), ClearDeviceErrors payload **0x00, 0x00**, SetStandby before SetTx, 10 dBm, clear_error(), BUSY retry. **decode_device_error()** added; test logs error bits on TX failure. Datasheet/AN excerpts are in `datasheet-and-an-notes.md` (PDFs removed). Forum/post references and "obvious solutions" are in `ping-test-summary.md`.

**Current failure:** Module A never gets TxDone. **Error = 0x200A** decodes to **RC13M_CALIB_ERR, ADC_CALIB_ERR** — block calibration (Calibrate 0x7F) fails on the chip.

**What we learned:** Arduino/RadioLib (begin + startTransmit) works on similar hardware, so the chip can work. Driver: retry Standby, TCXO then config, CalibrateImage **2-byte** band params, ClearDeviceErrors 0x00,0x00, regulator before STBY_XOSC. Semtech init order (Calibrate before SetPacketType/SetRfFrequency) tried; same 0x200A. See ping-test-summary.md **"What we learned (for next session)"** for full list.

**Next to try:** (1) **Hardware:** 50 Ω antennas on both modules; power quality; one module only (A) to rule out SPI contention. (2) Run known-good stack on same Pi; diff init. (3) **Ref:** RadioLib SX126x; Semtech SX126xLib Init() in os.mbed.com/teams/Semtech/code/SX126xLib.

---

## Completed

- **Semtech init order tried:** Driver reordered so Calibrate(0x7F) and CalibrateImage run immediately after SetStandby(STDBY_RC)+SetTcxoMode, before SetPacketType/SetRfFrequency (Semtech SX126xLib order). Ping test re-run; still FAIL, same error 0x200A (RC13M_CALIB_ERR, ADC_CALIB_ERR). datasheet-and-an-notes updated with Section 0 (quick reference, no PDF in repo).
- **Cleanup handoff:** Docs updated for next session: ping-test-summary.md has **"What we learned (for next session)"** (Arduino works so chip can work; CalibrateImage 2 bytes; RadioLib order; what didn't fix it; next directions). WIP doc and README point to it. Driver state: RadioLib-aligned init, CalibrateImage 0xD7/0xDB (868) or 0xE1/0xE9 (915), regulator before XOSC.
- **Calibration from STBY_RC, 915 MHz, RadioLib:** init_lora now does SetStandby(0x00) before Calibrate/CalibrateImage, then SetStandby(0x01) after (datasheet: Calibrate from STDBY_RC). Ran ping at 868 and 915 MHz — both FAIL, same error bits (RC13M_CALIB_ERR, ADC_CALIB_ERR). RadioLib comparison noted in ping-test-summary and datasheet-and-an-notes.
- **Error decode and ClearDeviceErrors fix:** ClearDeviceErrors payload set to 0x00,0x00 (datasheet 13.6). init_lora clears device errors immediately after SetStandby(0x01) to clear expected XOSC_START_ERR at POR. Added decode_device_error() in driver; test_ping logs "Error bits: …" on TX failure. Docs updated (datasheet-and-an-notes, ping-test-summary, README, WIP doc).
- **Ping test implemented and documented:** LoRa driver and `test_ping.py` (A→B ping, B→A pong); summary in `context/ping-test-summary.md`. Test currently fails (mode-change commands not taking effect); doc lists next steps.
- **SPI test verified on hardware:** Ran `test_spi.py` on Pi after enabling SPI and reboot. Module A and Module B both returned GetStatus 0x00 (ChipMode STBY_RC). Both modules are reachable over SPI.
- **SPI test added:** `test_spi.py` sends GetStatus (0xC0) to both modules; waits BUSY before/after transfer; uses spidev0.0 / spidev0.1. Detailed explanation in `context/spi-test-explained.md`. (Run on Pi with SPI enabled; terminal is on Pi per intro.md.)
- **GPIO connection test:** Added `sx1262_gpio_test/` at repo root (see README). Script resets both modules via NRST, drives RF_SW, reads BUSY and DIO1; both modules reported BUSY low after reset on Pi — wiring likely OK for SPI.
- Created module folder and docs (README, WIP doc, `wio-sx1262-module.md`, `wiring.md` in context/).
- Documented Wio-SX1262 module (pinout, BUSY/DIO1/RF_SW/TCXO, reference design) in `wio-sx1262-module.md`.
- Defined and documented wiring for two modules to Pi 4 (pin tables, board labels for XIAO carrier, wire colors, step-by-step) in `wiring.md`.
- **Wiring built:** two Wio-SX1262 for XIAO carriers on Pi 4 via breadboard; as-built notes (GND rail, grey/white for A/B DIO1 and RF_SW, kit antennas) in `wiring.md`.
