# SX1262 connection tests (GPIO and SPI)

**GPIO test:** Quick check that the Pi’s GPIO lines to both Wio-SX1262 modules are connected and that the chips respond after reset.

**SPI test:** Sends the SX1262 GetStatus command (0xC0) over SPI to each module and reads the response. Confirms SPI and BUSY/NSS discipline. See **`docs/sx1262-ping-test/SPI_TEST_EXPLAINED.md`** for a detailed description of the SPI test and what to expect.

## What it does

- **NRST:** Drives reset low for 10 ms then high. Both modules are reset.
- **BUSY:** After reset, waits up to 150 ms for BUSY to go low. When the chip is idle it pulls BUSY low; if we see low, the BUSY wire and chip are likely OK.
- **RF_SW:** Set high (receiver mode). Exercises the pin only.
- **DIO1:** Read once after reset. Confirms we can read the line (chip drives it).

Pins are defined in `pin_config.py` from `docs/sx1262-ping-test/wiring.md` (BCM).

## Run on the Pi

```bash
# From repo root
python3 sx1262_gpio_test/test_connection.py

# Append this run to a log file
python3 sx1262_gpio_test/test_connection.py --output sx1262_gpio_test/results.txt
```

Requires **gpiozero** and running on a Raspberry Pi with the two modules wired per `docs/sx1262-ping-test/wiring.md`. Exit code 0 if both modules’ BUSY went low; 1 otherwise.

## SPI test (after GPIO test passes)

```bash
python3 sx1262_gpio_test/test_spi.py
python3 sx1262_gpio_test/test_spi.py --output sx1262_gpio_test/spi_results.txt
```

Requires **spidev** (`pip install spidev` if needed) and SPI enabled (`dtparam=spi=on`, reboot). See **`docs/sx1262-ping-test/SPI_TEST_EXPLAINED.md`** for a full explanation of what the test does and how to interpret results.

## Files

- `pin_config.py` — BCM pin numbers for Module A and B (NRST, BUSY, DIO1, RF_SW).
- `test_connection.py` — GPIO test; resets both modules and reads BUSY/DIO1.
- `test_spi.py` — SPI test; sends GetStatus (0xC0) to each module and reads the status byte.
- `docs/sx1262-ping-test/SPI_TEST_EXPLAINED.md` — Detailed explanation of the SPI test and what to expect.
- `results.txt` / `spi_results.txt` — Optional; created when you pass `--output ...`.
