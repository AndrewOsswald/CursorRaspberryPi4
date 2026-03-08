#!/usr/bin/env python3
"""
GPIO connection test for two Wio-SX1262 modules on a Raspberry Pi 4.

Verifies that the Pi can drive and read the control lines (NRST, BUSY, DIO1, RF_SW)
for each module. Use this to confirm wiring before bringing up SPI.

Tests performed:
  - Reset: drive NRST low then high; chip should release internal reset.
  - BUSY: after reset, wait for BUSY to go low (chip ready). If we can read
    a stable low after a short wait, the BUSY line is likely connected.
  - RF_SW: drive high (RX mode); no electrical check, just exercises the pin.
  - DIO1: read once after reset; chip drives it (we only check we get a reading).

Usage:
  python3 test_connection.py [--output FILE]
  If --output is given, appends a timestamped run to that file (e.g. results.txt).

Requires: gpiozero, run on Pi with modules wired per docs/sx1262-ping-test/wiring.md.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

# Allow running from repo root: python3 sx1262_gpio_test/test_connection.py
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from gpiozero import InputDevice, OutputDevice

from pin_config import MODULE_A, MODULE_B

# Timing: NRST hold low (datasheet typ. > 2 ms), then wait for chip to become ready.
NRST_LOW_MS = 10
READY_WAIT_MS = 150
READY_POLL_MS = 5


def _ms(ms: float) -> None:
    time.sleep(ms / 1000.0)


def test_module(
    name: str,
    pins: dict[str, int],
    log: list[str],
) -> bool:
    """
    Test one module: reset, then read BUSY and DIO1.
    Returns True if BUSY went low within the wait window (suggests connection).
    """
    nrst = OutputDevice(pins["nrst"], initial_value=True)  # Release reset by default
    # pull_up=False: no pull-up; chip drives BUSY/DIO1. Disconnected = read as low.
    busy = InputDevice(pins["busy"], pull_up=False)
    dio1 = InputDevice(pins["dio1"], pull_up=False)
    rf_sw = OutputDevice(pins["rf_sw"], initial_value=True)  # RX mode

    try:
        # --- Reset ---
        nrst.off()
        _ms(NRST_LOW_MS)
        nrst.on()
        log.append(f"  {name}: NRST pulsed low for {NRST_LOW_MS} ms")

        # --- RF_SW high (RX) ---
        rf_sw.on()
        log.append(f"  {name}: RF_SW set high (RX)")

        # --- Wait for BUSY to go low (chip ready) ---
        deadline = time.monotonic() + (READY_WAIT_MS / 1000.0)
        busy_low = False
        while time.monotonic() < deadline:
            if not busy.value:
                busy_low = True
                break
            _ms(READY_POLL_MS)

        busy_val = busy.value
        dio1_val = dio1.value
        log.append(f"  {name}: BUSY={int(busy_val)} (after reset wait {READY_WAIT_MS} ms) -> {'OK (low)' if busy_low else 'still high or floating'}")
        log.append(f"  {name}: DIO1={int(dio1_val)} (read once)")

        return busy_low
    finally:
        # Release GPIO so pins are not left driving (per system-environment.md)
        nrst.close()
        busy.close()
        dio1.close()
        rf_sw.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="GPIO connection test for two SX1262 modules")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Append results to this file (e.g. results.txt)",
    )
    args = parser.parse_args()

    log: list[str] = []
    log.append("=== SX1262 GPIO connection test ===")
    log.append("")

    try:
        ok_a = test_module("Module A", MODULE_A, log)
        log.append("")
        ok_b = test_module("Module B", MODULE_B, log)
    except Exception as e:
        log.append(f"Error: {e}")
        for line in log:
            print(line)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, "a") as f:
                f.write("\n".join(log) + "\n")
        return 1

    log.append("")
    log.append("--- Summary ---")
    log.append(f"  Module A: {'PASS (BUSY went low)' if ok_a else 'CHECK (BUSY did not go low or wire issue)'}")
    log.append(f"  Module B: {'PASS (BUSY went low)' if ok_b else 'CHECK (BUSY did not go low or wire issue)'}")
    log.append("")
    if ok_a and ok_b:
        log.append("Both modules responded; wiring likely OK for SPI next.")
    else:
        log.append("If BUSY stayed high: check BUSY wire and GND. Then try SPI.")

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
