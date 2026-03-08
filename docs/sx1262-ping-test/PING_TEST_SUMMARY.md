# SX1262 ping test — summary

This document summarizes the **ping test** implementation and current results.

---

## What the ping test does

The test uses two Wio-SX1262 modules (A and B) on one Raspberry Pi 4:

1. **Initialize both** — Reset, TCXO, LoRa config (868 MHz, SF7, BW 125 kHz, CR 4/5, 4-byte payload, explicit header).
2. **Module B** enters RX (waits for a packet).
3. **Module A** sends the 4-byte payload `"ping"`.
4. **Module B** receives it, then sends the 4-byte payload `"pong"`.
5. **Module A** receives `"pong"`.
6. **Result** — PASS and round-trip time (ms), or FAIL with a short reason.

So “ping” is: A → B (ping), B → A (pong). Success means both radios received and sent as expected.

---

## Where the code lives

- **Driver:** `sx1262_gpio_test/sx1262_driver.py`  
  - Low-level: `wait_busy()`, `cmd()`, reset, clear/read error.  
  - LoRa: `init_lora()` (packet type, frequency, calibration, modulation/packet params, buffer base, DIO IRQ), `write_buffer()`, `read_buffer()`, `start_tx()`, `start_rx()`, `wait_tx_done()`, `wait_rx_done()`, `get_rx_buffer_status()`.

- **Test script:** `sx1262_gpio_test/test_ping.py`  
  - Builds two `SX1262` instances (Module A = spidev0.0 + GPIO for BUSY/NRST/RF_SW, Module B = spidev0.1 + GPIO).  
  - Runs the sequence above and prints/appends a short log.  
  - Optional: `--output FILE` to append the run to a file; `--freq FREQ` for frequency in Hz (default 868e6).

- **Pins:** Same as GPIO/SPI tests — `sx1262_gpio_test/pin_config.py` and `docs/sx1262-ping-test/wiring.md`.

---

## How to run

On the Pi, from the repo root, with both modules wired and SPI enabled:

```bash
python3 sx1262_gpio_test/test_ping.py
python3 sx1262_gpio_test/test_ping.py --output sx1262_gpio_test/ping_results.txt
```

Requires: **gpiozero**, **spidev**, and the same hardware setup as the SPI test.

---

## Current result (as of this doc)

- **Ping test:** **FAIL** — Module A never sees TxDone; chip status stays in STBY_RC (0x00) after SetTx (and after SetRx).  
- **SPI test:** **PASS** — GetStatus (0xC0) returns 0x00 for both modules, so SPI and BUSY discipline are OK.  
- **GPIO test:** **PASS** — BUSY goes low after reset on both modules.

So the radios are reachable over SPI and the control lines behave, but the LoRa mode-change commands (SetRx / SetTx) do not appear to change the reported chip mode. Possible causes to check:

- **CE0/CE1 vs physical A/B** — Confirm which module is on spidev0.0 and which on spidev0.1 (and that the labels match the code).  
- **Missing or wrong step** — e.g. entering FS (frequency synthesis) before TX, or a different init/command order (compare with Semtech ref code or another known-good driver).  
- **Hardware** — Antennas on both modules; no PA/overcurrent protection tripping (e.g. try lower TX power in the driver if needed).

When the test passes, the script will print something like:

- `--- Result: PASS ---`  
- `Round-trip time: XX.X ms`

and exit with code 0.

---

## Summary table

| Item              | Location / command                    | Status / note                                  |
|-------------------|----------------------------------------|------------------------------------------------|
| LoRa driver       | `sx1262_gpio_test/sx1262_driver.py`   | Implements init, TX, RX, IRQ, buffer access   |
| Ping test script  | `sx1262_gpio_test/test_ping.py`       | A sends ping, B replies pong, A receives      |
| Run               | `python3 sx1262_gpio_test/test_ping.py`| Currently FAIL (SetTx/SetRx not changing mode)|
| SPI test          | `test_spi.py`                         | PASS (both chips respond to GetStatus)         |

Once SetTx/SetRx are fixed (or the correct sequence is found), re-run the ping test and update this summary with the new result and, if desired, a sample of the output.
