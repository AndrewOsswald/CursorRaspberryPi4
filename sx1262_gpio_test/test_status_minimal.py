#!/usr/bin/env python3
"""Minimal test: Module A only — reset, full LoRa init, SetTx, then read status."""
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from gpiozero import InputDevice, OutputDevice
from pin_config import MODULE_A
from sx1262_driver import SX1262
import time

def main():
    if not Path("/dev/spidev0.0").exists():
        print("No /dev/spidev0.0")
        return 1
    busy_a = InputDevice(MODULE_A["busy"], pull_up=False)
    nrst_a = OutputDevice(MODULE_A["nrst"], initial_value=True)
    rf_sw_a = OutputDevice(MODULE_A["rf_sw"], initial_value=True)
    radio_a = SX1262(
        0, 0,
        busy_read=lambda: bool(busy_a.value),
        nrst_high=nrst_a.on,
        nrst_low=nrst_a.off,
        rf_sw_rx=rf_sw_a.on,
        rf_sw_tx=rf_sw_a.off,
    )
    try:
        radio_a.reset()
        print("After reset: GetStatus = 0x%02X" % radio_a.get_status())
        radio_a.init_lora(payload_len=4)
        print("After init_lora: GetStatus = 0x%02X" % radio_a.get_status())
        radio_a.clear_irq()
        radio_a.write_buffer(0, b"ping")
        radio_a.start_tx()
        time.sleep(0.2)
        s = radio_a.get_status()
        print("After start_tx + 200ms: GetStatus = 0x%02X (0x20=TX)" % s)
        radio_a._close_spi()
    finally:
        busy_a.close()
        nrst_a.close()
        rf_sw_a.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
