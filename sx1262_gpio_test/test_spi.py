#!/usr/bin/env python3
"""
SPI connection test for two Wio-SX1262 modules on a Raspberry Pi 4.

Sends the SX1262 GetStatus command (0xC0) to each module and reads the
1-byte response. Confirms that SPI and the BUSY/NSS discipline work.

Protocol (per sx1262_gpio_test/context/wiring.md and SX1262 datasheet):
  - Wait until BUSY is low before any SPI transaction.
  - Assert NSS (chip select) low; send 0xC0; receive 1 byte; release NSS.
  - Wait until BUSY is low again before next command.

NSS is handled by the Pi SPI driver (spidev0.0 = CE0 for Module A,
spidev0.1 = CE1 for Module B). We control NRST, RF_SW, and BUSY via GPIO.

Usage:
  python3 test_spi.py [--output FILE]

Requires: gpiozero, spidev; run on Pi with SPI enabled and modules wired.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from gpiozero import InputDevice, OutputDevice

from pin_config import MODULE_A, MODULE_B

# SX1262 GetStatus command (RADIO_GET_STATUS); response is 1 byte.
CMD_GET_STATUS = 0xC0

# SPI: Mode 0 (CPOL=0, CPHA=0); conservative speed for first test.
SPI_MODE = 0
SPI_MAX_HZ = 2_000_000

# Timing
NRST_LOW_MS = 10
READY_WAIT_MS = 200
BUSY_POLL_MS = 2


def _ms(ms: float) -> None:
    time.sleep(ms / 1000.0)


def wait_busy_low(busy: InputDevice, timeout_ms: float) -> bool:
    """Wait until BUSY is low or timeout. Returns True if BUSY went low."""
    deadline = time.monotonic() + (timeout_ms / 1000.0)
    while time.monotonic() < deadline:
        if not busy.value:
            return True
        _ms(BUSY_POLL_MS)
    return False


def reset_module(
    nrst: OutputDevice,
    rf_sw: OutputDevice,
) -> None:
    """Pulse NRST low and set RF_SW high (RX)."""
    nrst.off()
    _ms(NRST_LOW_MS)
    nrst.on()
    rf_sw.on()


def get_status_spi(spi_path: str, busy: InputDevice, timeout_ms: float) -> tuple[int | None, str]:
    """
    Send GetStatus (0xC0) and return (response_byte, message).
    If BUSY never goes low or transfer fails, returns (None, error_message).
    """
    if not wait_busy_low(busy, timeout_ms):
        return None, "BUSY did not go low before transfer"

    try:
        import spidev
    except ImportError:
        return None, "spidev not installed (pip install spidev)"

    # Open the correct spidev device (NSS is driven by the driver).
    bus, dev = (0, 0) if "spidev0.0" in spi_path else (0, 1)
    spi = spidev.SpiDev()
    spi.open(bus, dev)
    try:
        spi.mode = SPI_MODE
        spi.max_speed_hz = SPI_MAX_HZ
        # Full duplex: send 1 byte, receive 1 byte.
        tx = [CMD_GET_STATUS]
        rx = spi.xfer2(tx)
        if not rx:
            return None, "SPI transfer returned no data"
        status_byte = rx[0] & 0xFF
    except OSError as e:
        return None, f"SPI error: {e}"
    finally:
        spi.close()

    if not wait_busy_low(busy, timeout_ms):
        return status_byte, f"Got 0x{status_byte:02X} but BUSY did not go low after (chip may still be OK)"

    return status_byte, f"0x{status_byte:02X}"


def test_module_spi(
    name: str,
    pins: dict[str, int],
    spi_path: str,
    log: list[str],
) -> bool:
    """
    Reset module, then run GetStatus over SPI. Returns True if we got a
    status byte (any value; 0xFF often means no chip / MISO floating).
    """
    nrst = OutputDevice(pins["nrst"], initial_value=True)
    busy = InputDevice(pins["busy"], pull_up=False)
    rf_sw = OutputDevice(pins["rf_sw"], initial_value=True)

    try:
        reset_module(nrst, rf_sw)
        _ms(READY_WAIT_MS)

        status_byte, msg = get_status_spi(spi_path, busy, timeout_ms=READY_WAIT_MS)
        log.append(f"  {name}: GetStatus -> {msg}")

        if status_byte is None:
            return False
        # 0xFF often indicates floating MISO or no device; any other value suggests chip replied.
        if status_byte == 0xFF:
            log.append(f"  {name}: WARNING 0xFF can mean MISO floating or no chip; check wiring.")
        else:
            # Status byte: bits 6:5 = ChipMode (e.g. 0=STBY_RC, 1=STBY_XOSC, 2=FS, 3=RX, 4=TX, ...)
            chip_mode = (status_byte >> 5) & 0x03
            log.append(f"  {name}: ChipMode bits (6:5) = {chip_mode} (0=STBY_RC, 1=STBY_XOSC, 2=FS, 3=RX/TX)")
        return True
    finally:
        nrst.close()
        busy.close()
        rf_sw.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="SPI test for two SX1262 modules (GetStatus)")
    parser.add_argument("--output", type=Path, default=None, help="Append results to this file")
    args = parser.parse_args()

    log: list[str] = []
    log.append("=== SX1262 SPI test (GetStatus 0xC0) ===")
    log.append("")

    # Must run on Pi with SPI enabled (dtparam=spi=on in /boot/firmware/config.txt).
    if not Path("/dev/spidev0.0").exists():
        log.append("Error: /dev/spidev0.0 not found. Enable SPI (dtparam=spi=on) and reboot.")
        for line in log:
            print(line)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, "a") as f:
                f.write("\n".join(log) + "\n")
        return 1

    try:
        ok_a = test_module_spi("Module A", MODULE_A, "/dev/spidev0.0", log)
        log.append("")
        ok_b = test_module_spi("Module B", MODULE_B, "/dev/spidev0.1", log)
    except Exception as e:
        log.append(f"Error: {e}")
        import traceback
        log.append(traceback.format_exc())
        for line in log:
            print(line)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, "a") as f:
                f.write("\n".join(log) + "\n")
        return 1

    log.append("")
    log.append("--- Summary ---")
    log.append(f"  Module A: {'PASS' if ok_a else 'FAIL'}")
    log.append(f"  Module B: {'PASS' if ok_b else 'FAIL'}")
    if ok_a and ok_b:
        log.append("Both modules responded over SPI.")
    else:
        log.append("Check BUSY/NSS/SPI wiring and that SPI is enabled (dtparam=spi=on).")

    for line in log:
        print(line)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "a") as f:
            f.write("\n".join(log) + "\n")
        print(f"(Appended to {args.output})")

    return 0 if (ok_a and ok_b) else 1


if __name__ == "__main__":
    sys.exit(main())
