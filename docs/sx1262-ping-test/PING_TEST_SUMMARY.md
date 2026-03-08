# SX1262 ping test — summary

This document summarizes the **ping test** implementation and current results. **For a new chat:** read `docs/intro.md` → task doc → `feature.md` → this file and `DATASHEET_AND_AN_NOTES.md`; task doc has a **“Context for next session”** section with what’s done and what to try next.

---

## What we learned (for next session)

- **Arduino/RadioLib is trivial:** `radio.begin(868.0)` and `radio.startTransmit(...)` work on similar hardware (e.g. Heltec LoRa V3 SX1262). So the chip and boards can work; our issue is init sequence or Pi/SPI environment.
- **Failure is consistent:** TX never completes; **error = 0x200A** decodes to **RC13M_CALIB_ERR, ADC_CALIB_ERR**. So the **block calibration (Calibrate 0x7F)** is failing on the chip; SetTx then hits those errors.
- **Fixes that were applied (no PASS yet):**
  - **ClearDeviceErrors** payload must be **0x00, 0x00** (datasheet 13.6), not 0x07.
  - **CalibrateImage** takes **two band bytes**; we had been sending one. Use **0xD7, 0xDB** for 863–870 MHz and **0xE1, 0xE9** for 902–928 MHz (both bytes must be odd per RadioLib issue #1096).
  - **RadioLib modSetup order:** reset → retry Standby until BUSY ok → **setTCXO** → **config** (packet type, freq, Calibrate, CalibrateImage) → **setRegulatorDCDC** last. We now do TCXO then config; we set regulator *before* switching to STBY_XOSC so the Wio has DC-DC for XOSC.
  - **Retry standby** after reset (RadioLib: “SX126x often refuses first few commands”).
- **What did *not* fix it:** Calibration from STBY_RC only; longer reset (500 ms) or TCXO delay (10 ms); LDO-only regulator; SetPaConfig; clearing errors after cal or before SetTx; 915 MHz; many timing tweaks.
- **Next directions:** (1) **Hardware:** antennas (50 Ω) on both modules, power quality, try single module (only A) to rule out SPI/contention. (2) **Software:** Run a known-good stack (e.g. RadioLib or Semtech ref) on the *same* Pi + modules; if that works, diff our init. (3) **Ref:** RadioLib `SX126x::modSetup()` and `config()` in `src/modules/SX126x/SX126x.cpp`; their `findChip()` resets and retries standby; regulator is set after `config(modem)`.

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

- **SPI test:** **PASS** — Both modules respond (A often 0xAA, B 0x00). NSS (CE0/CE1) correct.
- **Ping test:** **FAIL** — Reaches “Module A: sending 'ping'…” then **TX fails (no TxDone)**. **Error = 0x200A** → **RC13M_CALIB_ERR, ADC_CALIB_ERR**. Init runs; block calibration appears to fail on the chip.

**Current driver init (RadioLib-aligned):** 50 ms delay → retry Standby(0x00) until BUSY ok (20 tries) → SetTcxoMode 3.0 V, 320 units (5 ms) → Standby(0x00) → SetPacketType LoRa → SetRfFrequency → Calibrate(0x7F) + wait BUSY + 2 ms → **CalibrateImage** with **2 bytes** (868: 0xD7,0xDB; 915: 0xE1,0xE9) + wait BUSY + 2 ms → ClearDeviceErrors → SetRegulatorMode DC-DC → SetStandby(0x01) → ClearDeviceErrors → SetPaConfig → SetTxParams 10 dBm → SetModulationParams → SetPacketParams → SetBufferBaseAddress → SetDioIrqParams. Reset: 20 ms NRST low, **500 ms** after release; ClearDeviceErrors. start_tx: SetStandby(0x01), 5 ms, ClearDeviceErrors, SetTx.

**Datasheet/AN:** See **`DATASHEET_AND_AN_NOTES.md`**. ClearDeviceErrors 0x00,0x00. CalibrateImage band bytes per datasheet/RadioLib (863–870: 0xD7,0xDB; 902–928: 0xE1,0xE9). decode_device_error() logs set bits on TX failure.

**If status still stays 0x00 on real hardware, check:**

- **CE0/CE1 vs physical A/B** — Confirm which module is on spidev0.0 and which on spidev0.1 (and that the labels match the code).  
- **Missing or wrong step** — Compare init/TX sequence with Semtech ref code or RadioLib SX1262.  
- **Hardware** — Antennas on both modules; no PA/overcurrent; try lower TX power (e.g. 10 dBm in `SET_TXPARAMS`) if needed.

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
| Minimal (A only)  | `test_status_minimal.py`             | Reset → init_lora → start_tx → status         |
| SPI test          | `test_spi.py`                         | PASS (both chips respond to GetStatus)         |

Once SetTx/SetRx are fixed (or the correct sequence is found), re-run the ping test on the Pi and update this summary with the new result.

---

## References (forum posts and issues)

People with similar SX1262 problems (mode not changing, TX timeout, error 0x200A-like, Wio-SX1262):

| Source | Symptom | Link |
|--------|---------|------|
| ST Community | CMD_EXEC_FAILURE, chip stays in standby after SetRx/SetTx | [Issue with sx1262 module](https://community.st.com/t5/others-hardware-and-software/issue-with-sx1262-module/td-p/736755) |
| ST Community | LoRa SX1262 TX timeout | [Lora SX1262 Tx Timeout](https://community.st.com/t5/stm32-mcus-wireless/lora-sx1262-tx-timeout/td-p/213681) |
| RadioLib | SX1262 + Raspberry Pico, TX timeout | [Raspberry Pico + SX 1262 #729](https://github.com/jgromes/RadioLib/issues/729) |
| RadioLib | SX1262 TX timeout / no TxDone | [RadioLib #740](https://github.com/jgromes/RadioLib/issues/740), [discussion 1127](https://github.com/jgromes/RadioLib/discussions/1127) |
| RadioLib | CalibrateImage / PLL lock fail (-707) | [SX1262 setup fails at CalibrateImage #100](https://github.com/jgromes/RadioLib/issues/100) |
| LoRaMac-node | TCXO / DIO3 wrong on custom boards | [LoRaMac-node discussion 1044](https://github.com/Lora-net/LoRaMac-node/discussions/1044) |
| RadioLib | SX1262 two-way comms fail (Wio/Core1262) | [Two way communication issue #1196](https://github.com/jgromes/RadioLib/issues/1196) |
| Seeed Forum | Wio-SX1262 + XIAO LoRa error | [XIAO ESP32S3 & Wio-SX1262 LoRa error](https://forum.seeedstudio.com/t/xiao-esp32s3-wio-sx1262-arduino-ide-lora-error/284419) |
| RadioLib | SX1262 + Raspberry Pi 5 not receiving | [Discussion #1218](https://github.com/jgromes/RadioLib/discussions/1218) |

### Obvious solutions from these sources

- **SPI must be full-duplex:** One post (ST 736755) had the chip stuck in standby because the HAL used separate `HAL_SPI_Transmit` and `HAL_SPI_Receive`. SX1262 expects one TransmitReceive per transaction so the status byte is read in the same transfer. Our driver uses `xfer2()` (full-duplex) — already correct; worth confirming every command does one transfer.
- **GPIO / DIO1 / BUSY / NSS:** Several RadioLib and ST threads blame wrong pin numbers (logical vs physical), DIO1 not wired or misused, BUSY or NSS wrong. Double-check pin_config and wiring against the board (BCM numbers, one NSS per module).
- **TCXO / DIO3:** LoRaMac-node and Seeed note that with external TCXO, DIO3 must drive the TCXO supply correctly; on custom boards it can stay LOW. Wio uses DIO3 for TCXO — ensure init (SetTcxoMode) and power to the module are correct; try a longer delay after SetTcxoMode.
- **Frequency band:** RadioLib #100 suggests trying a different band for image calibration (e.g. 915 MHz if 868 MHz fails). Run with `--freq 915000000` to test.
- **Pin definitions and power:** Seeed thread stresses `LoRa.setPins()` (or equivalent) and stable 3.3 V; Wio uses DC-DC and DIO3 for TCXO — antenna 50 Ω and power quality matter.

No single fix is guaranteed; these are the most often cited and worth trying in order (SPI already OK here; then pins/TCXO/frequency).

---

## Additional documentation for setting up SX1262 chips

**Key excerpts from the Semtech SX1262 datasheet, AN1200.59, and Seeed Wio-SX1262-N datasheet are in `DATASHEET_AND_AN_NOTES.md` in this folder** (TCXO command and delay, error register, Tx sequence). The PDFs do not need to remain in the repo.

### Semtech (official)

- **Product page (datasheet, app notes, reference designs):**  
  [Semtech SX1262](https://www.semtech.com/products/wireless-rf/lora-connect/sx1262)  
  From here you can open the **SX1261/SX1262 Datasheet** and application notes (some links may require Semtech login).

- **Application notes (most relevant for setup):**
  - **AN1200.37** – Recommendations for Best Performance (thermal, LoRa packet, crystal behavior, PCB).
  - **AN1200.40** – Reference Design Explanation for SX1261/62 (schematics, matching, layout).
  - **AN1200.59** – Selecting the Optimal Reference Clock (XTAL vs TCXO, useful for Wio’s TCXO).
  - **AN1200.66** – PCB Design Guidelines.

- **User guides:** Same product page lists SX1261/SX1262 datasheet and dev kit / shield docs (e.g. SX1262MB1LDCS switchless reference).

### Seeed Studio (Wio-SX1262 module)

- **Wiki (overview, pinout, reference design):**  
  [Wio-SX1262 Introduction](https://wiki.seeedstudio.com/wio_sx1262)

- **Downloads (from wiki “Resource”):**
  - [Wio-SX1262 symbol and package file](https://files.seeedstudio.com/products/SenseCAP/Wio_SX1262/Wio-SX1262_symbol_and_package_file.zip)
  - [Schematic Diagram (Wio-SX1262 for XIAO)](https://files.seeedstudio.com/products/SenseCAP/Wio_SX1262/Schematic_Diagram_Wio-SX1262_for_XIAO.pdf)
  - [Wio-SX1262-N Module Datasheet](https://files.seeedstudio.com/products/SenseCAP/Wio_SX1262/Wio-SX1262-N_Module_Datasheet.pdf)

- **Kits:** [XIAO ESP32S3 & Wio-SX1262 Kit](https://wiki.seeedstudio.com/wio_sx1262_with_xiao_esp32s3_kit), [LoRaWAN sensor node config](https://wiki.seeedstudio.com/wio_sx1262_xiao_esp32s3_for_lora_sensor_node).

### Software / driver references (command set, init order)

- **RadioLib (C++):** [SX1262 class reference](https://jgromes.github.io/RadioLib/class_s_x1262.html) – init, TX/RX, parameters; useful to compare sequence.
- **ESPHome SX126x:** [SX126x component](https://next.esphome.io/components/sx126x/), [sx126x_reg.h](https://api-docs.esphome.io/sx126x__reg_8h) – register/command opcodes.
- **NuttX:** [SX126x LoRa driver](https://nuttx.apache.org/docs/12.10.0/components/drivers/character/wireless/lpwan/sx126x.html) – another init/TX/RX reference.
- **Mbed:** [SX126xLib](https://os.mbed.com/teams/Semtech/code/SX126xLib/docs/tip/classSX126x.html) – Semtech’s Mbed API.
- **SX126x-Arduino:** [sx126x-board.h](https://beegee-tokyo.github.io/SX126x-Arduino/html/sx126x-board_8h.html) – board/pin and command references.

### Raspberry Pi + SX1262

- **SX126X LoRa HAT (Python):** [basor-dali/SX126X_LoRa_HAT_rasp_pi](https://github.com/basor-dali/SX126X_LoRa_HAT_rasp_pi) – transmit/receive scripts for Pi.
- **LoRa868 (MicroPython, SX1262):** [UIFlow2 LoRa868 module](https://uiflow-micropython.readthedocs.io/en/2.2.6/module/lora_sx1262.html) – usage patterns.

### Other

- **Electrodragon (SX1262 HDK, markdown):** [SX1262-HDK-dat](https://w2.electrodragon.com/Chip-dat/SemTech-dat/SX1262-dat/SX1262-HDK-dat/SX1262-HDK-dat.md) – wiring, NSS/BUSY/DIO, optional DIO2 RF switch.

---

## Latest test run output

**Date:** Captured after NSS wiring was corrected (Module A = CE0, Module B = CE1).

### SPI test (`python3 sx1262_gpio_test/test_spi.py`)

```
=== SX1262 SPI test (GetStatus 0xC0) ===

  Module A: GetStatus -> 0xAA
  Module A: ChipMode bits (6:5) = 1 (0=STBY_RC, 1=STBY_XOSC, 2=FS, 3=RX/TX)

  Module B: GetStatus -> 0x00
  Module B: ChipMode bits (6:5) = 0 (0=STBY_RC, 1=STBY_XOSC, 2=FS, 3=RX/TX)

--- Summary ---
  Module A: PASS
  Module B: PASS
Both modules responded over SPI.
```

**Note:** Module A reports 0xAA (ChipMode 1 = STBY_XOSC); Module B reports 0x00 (STBY_RC). Both chips are reachable over SPI with NSS correct.

### Ping test (`python3 sx1262_gpio_test/test_ping.py`)

The ping test did not complete. It exited with a **GPIO busy** error when claiming the BUSY pin (GPIO 18 / Module A):

```
Traceback (most recent call last):
  ...
  File "/home/mochi/sandbox/NewCursorProject/sx1262_gpio_test/test_ping.py", line 83, in main
    busy_a = InputDevice(MODULE_A["busy"], pull_up=False)
  ...
lgpio.error: 'GPIO busy'
```

**What to do:** Ensure no other process is using the SX1262 GPIOs (BUSY, NRST, RF_SW, DIO1). Run the ping test alone (e.g. close any other script that uses those pins), or run it after a fresh boot. Then re-run and update this section with the new ping output.
