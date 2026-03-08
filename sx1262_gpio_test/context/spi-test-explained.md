# SX1262 SPI test — what it does and what to expect

This document explains the **SPI connection test** (`test_spi.py`) in detail: what the test does, how the SX1262 SPI protocol works, and how to interpret the results.

---

## Purpose

After the **GPIO test** (`test_connection.py`) confirms that NRST, BUSY, DIO1, and RF_SW are wired and that the chips release BUSY low after reset, the **SPI test** checks that the Pi can actually **talk to both modules over SPI**. It sends one SX1262 command (GetStatus) and reads the response. If both modules return a status byte, SPI and the BUSY/NSS discipline are working and you can move on to the ping test (send/receive packets).

---

## What the test does (step by step)

1. **Reset both modules (GPIO)**
   - Drive **NRST** low for 10 ms, then high.
   - Set **RF_SW** high (receiver path; safe idle state).
   - This is the same reset sequence as in the GPIO test.

2. **Wait for chips to be ready**
   - Wait 200 ms so the SX1262 can complete its power‑on/calibration and pull **BUSY** low when idle.

3. **For Module A (spidev0.0 / CE0):**
   - Wait until **BUSY** (GPIO 18) is low.
   - Open **/dev/spidev0.0**. The Pi's SPI driver drives **NSS** (CE0) low when we transfer.
   - Send one byte: **0xC0** (GetStatus command).
   - Read one byte back (the status response).
   - Close the device.
   - Wait until **BUSY** is low again (so the chip is ready for the next command).

4. **For Module B (spidev0.1 / CE1):**
   - Same sequence using **/dev/spidev0.1** and Module B's **BUSY** (GPIO 5).
   - Only the chip select (CE1) and BUSY pin differ; MOSI/MISO/SCK are shared.

5. **Result**
   - The script prints the **status byte** for each module (e.g. `0x02`) and a short summary.
   - If it got a byte from both modules, the test **passes**.
   - If the byte is **0xFF**, the script warns: that often means MISO is floating or no chip is responding (wiring or NSS wrong).
   - Any other value (e.g. 0x00, 0x02) usually means the chip replied; the low bits indicate chip mode and command status.

---

## Why we wait for BUSY

The SX1262 drives **BUSY** high while it is processing a command and pulls it **low** when it is ready for the next one. The datasheet and wiring notes require:

- **Before** every SPI transaction: wait until BUSY is low.
- **After** the transaction: wait until BUSY is low again before sending another command.

If we don't wait, we might clock in a new command while the chip is still handling the previous one, which can corrupt state or return garbage. The test script polls the BUSY GPIO before and after the single GetStatus transfer to follow this rule.

---

## Why we use GetStatus (0xC0)

- **GetStatus** is a simple "are you there?" command: one byte out (0xC0), one byte back (status).
- It doesn't change radio configuration or require any prior setup (e.g. no need to configure TCXO or LoRa params first).
- The response byte encodes chip mode and command status; even a "generic" value (e.g. 0x00 or 0x02) confirms that the chip received the command and drove MISO.

So this one command is enough to verify that SPI, NSS, and BUSY handling are correct for both modules.

---

## NSS (chip select) and spidev

- **Module A** is on **CE0** → Linux device **/dev/spidev0.0**.
- **Module B** is on **CE1** → Linux device **/dev/spidev0.1**.

When we call `spi.open(0, 0)` or `spi.open(0, 1)` and then `spi.xfer2(...)`, the kernel drives the corresponding NSS line low for the duration of the transfer. We do **not** drive NSS from Python; the Pi's SPI driver does it. We only make sure BUSY is low before and after each transfer.

---

## What to expect when it works

- **Console output** looks like:
  - `Module A: GetStatus -> 0x02` (or similar hex value)
  - `Module A: ChipMode bits (6:5) = 0 ...` (optional interpretation)
  - Same for Module B.
  - Summary: `Both modules responded over SPI.`
- **Exit code** is 0.

If you see **0xFF** for one or both modules, the script still reports PASS (it got a byte) but prints a warning: double‑check that module's NSS, MISO, and GND.

---

## What to expect when it doesn't work

- **`/dev/spidev0.0` not found**
  - SPI is not enabled. Add `dtparam=spi=on` to `/boot/firmware/config.txt`, reboot, and run again.

- **Permission denied** on `/dev/spidev0.*`
  - Add your user to the `spi` group: `sudo usermod -aG spi $USER`, then log out and back in (or reboot).

- **BUSY did not go low**
  - Wiring: check the BUSY pin for that module (and GND).
  - Or the chip didn't power up: check 3V3 and GND.

- **0xFF from chip**
  - Often means MISO not connected, wrong NSS (wrong module selected), or chip not powered. Check wiring for that module.

---

## How to run the test

From the repo root, on the Pi, with the two modules wired per `context/wiring.md`:

```bash
python3 sx1262_gpio_test/test_spi.py
```

To append the output to a file:

```bash
python3 sx1262_gpio_test/test_spi.py --output sx1262_gpio_test/spi_results.txt
```

Requires: **gpiozero**, **spidev**, and SPI enabled on the Pi.

---

## Summary

| Step        | What happens |
| ----------- | ------------- |
| Reset       | NRST low 10 ms, then high; RF_SW high. |
| Wait        | 200 ms for BUSY to go low. |
| Module A    | Wait BUSY low → open spidev0.0 → send 0xC0, read 1 byte → close → wait BUSY low. |
| Module B    | Wait BUSY low → open spidev0.1 → send 0xC0, read 1 byte → close → wait BUSY low. |
| Pass        | Both modules return a status byte (preferably not 0xFF). |

Once this test passes, both chips are reachable over SPI and you can implement the ping test (init LoRa, send packet from one, receive and reply from the other, measure round‑trip).
