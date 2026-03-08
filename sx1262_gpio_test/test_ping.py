#!/usr/bin/env python3
"""
Ping test: Module A sends "ping", Module B receives and replies "pong", Module A receives.

Both modules are configured for LoRa (868 MHz, SF7, BW 125 kHz, 4-byte payload).
Reports success/failure and round-trip time. Run on Pi with SPI enabled and
both Wio-SX1262 modules wired per sx1262_gpio_test/context/wiring.md.
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
from sx1262_driver import SX1262, decode_device_error

PAYLOAD_LEN = 4
PING = b"ping"
PONG = b"pong"


def _make_radio(pins: dict, bus: int, dev: int) -> SX1262:
    busy = InputDevice(pins["busy"], pull_up=False)
    nrst = OutputDevice(pins["nrst"], initial_value=True)
    rf_sw = OutputDevice(pins["rf_sw"], initial_value=True)

    def busy_read() -> bool:
        return bool(busy.value)

    def nrst_high() -> None:
        nrst.on()

    def nrst_low() -> None:
        nrst.off()

    def rf_sw_rx() -> None:
        rf_sw.on()

    def rf_sw_tx() -> None:
        rf_sw.off()

    return SX1262(
        spi_bus=bus,
        spi_dev=dev,
        busy_read=busy_read,
        nrst_high=nrst_high,
        nrst_low=nrst_low,
        rf_sw_rx=rf_sw_rx,
        rf_sw_tx=rf_sw_tx,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="SX1262 LoRa ping test (A -> B -> A)")
    parser.add_argument("--output", type=Path, default=None, help="Append results to this file")
    parser.add_argument("--freq", type=float, default=868_000_000, help="Frequency in Hz (default 868e6)")
    args = parser.parse_args()

    log: list[str] = []
    log.append("=== SX1262 ping test ===")
    log.append("")

    if not Path("/dev/spidev0.0").exists():
        log.append("Error: /dev/spidev0.0 not found. Enable SPI and reboot.")
        for line in log:
            print(line)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, "a") as f:
                f.write("\n".join(log) + "\n")
        return 1

    # We need to keep GPIO devices alive for the duration of the test.
    busy_a = InputDevice(MODULE_A["busy"], pull_up=False)
    nrst_a = OutputDevice(MODULE_A["nrst"], initial_value=True)
    rf_sw_a = OutputDevice(MODULE_A["rf_sw"], initial_value=True)
    busy_b = InputDevice(MODULE_B["busy"], pull_up=False)
    nrst_b = OutputDevice(MODULE_B["nrst"], initial_value=True)
    rf_sw_b = OutputDevice(MODULE_B["rf_sw"], initial_value=True)

    # Module A = CE0 (spidev0.0), Module B = CE1 (spidev0.1) per wiring.md
    radio_a = SX1262(
        0, 0,  # CE0 -> Module A
        busy_read=lambda: bool(busy_a.value),
        nrst_high=nrst_a.on,
        nrst_low=nrst_a.off,
        rf_sw_rx=rf_sw_a.on,
        rf_sw_tx=rf_sw_a.off,
    )
    radio_b = SX1262(
        0, 1,  # CE1 -> Module B
        busy_read=lambda: bool(busy_b.value),
        nrst_high=nrst_b.on,
        nrst_low=nrst_b.off,
        rf_sw_rx=rf_sw_b.on,
        rf_sw_tx=rf_sw_b.off,
    )

    success = False
    try:
        log.append(f"Resetting and initializing both modules (LoRa {args.freq/1e6:.0f} MHz, SF7, 4-byte payload)...")
        radio_a.reset()
        radio_b.reset()
        if not radio_a.wait_busy(timeout_ms=2000):
            log.append("Module A: BUSY did not go low after reset.")
            raise RuntimeError("Module A BUSY timeout after reset")
        if not radio_b.wait_busy(timeout_ms=2000):
            log.append("Module B: BUSY did not go low after reset.")
            raise RuntimeError("Module B BUSY timeout after reset")
        # Init B first so A's SPI traffic can't glitch B; then A
        radio_b.init_lora(freq_hz=args.freq, payload_len=PAYLOAD_LEN)
        radio_b._close_spi()
        radio_a.init_lora(freq_hz=args.freq, payload_len=PAYLOAD_LEN)
        radio_a._close_spi()
        log.append("OK.")
        time.sleep(0.05)
        try:
            sa0 = radio_a.get_status()
        except RuntimeError:
            sa0 = 0xFF
            log.append("  (A status read skipped: BUSY)")
        try:
            sb0 = radio_b.get_status()
        except RuntimeError:
            sb0 = 0xFF
            log.append("  (B status read skipped: BUSY)")
        log.append(f"  After init: A status=0x{sa0:02X} B status=0x{sb0:02X} (expect 0x02=STBY_XOSC)")
        log.append("")

        # Re-init B so it's idle after A's SPI traffic (shared bus can glitch B)
        radio_b.reset()
        if not radio_b.wait_busy(timeout_ms=2000):
            log.append("Module B: BUSY timeout after re-reset.")
        radio_b.init_lora(freq_hz=args.freq, payload_len=PAYLOAD_LEN)
        radio_b._close_spi()

        # B enters RX first; then A sends ping.
        log.append("Module B: entering RX...")
        radio_b.clear_irq()
        radio_b.start_rx(timeout_rtc=0)
        time.sleep(0.1)

        log.append("Module A: sending 'ping'...")
        t0 = time.monotonic()
        radio_a.clear_error()
        radio_a.clear_irq()
        radio_a.write_buffer(0, PING)
        radio_a.start_tx()
        time.sleep(0.1)  # let chip transition STBY_XOSC -> FS -> TX
        sa, sb = radio_a.get_status(), radio_b.get_status()
        log.append(f"  After SetTx: A status=0x{sa:02X} B status=0x{sb:02X} (0x02=STBY_XOSC 0x20=TX 0x30=RX)")
        if not radio_a.wait_tx_done(timeout_ms=5000):
            log.append("Module A: TX failed (no TxDone).")
            err = radio_a.get_error()
            log.append(f"  Module A IRQ=0x{radio_a.get_irq():04X} status=0x{radio_a.get_status():02X} error=0x{err:04X}")
            if err:
                log.append(f"  Error bits: {', '.join(decode_device_error(err))}")
            success = False
        else:
            radio_a._rf_sw_rx()
            log.append("Module A: TX done.")
            # B should have received.
            if not radio_b.wait_rx_done(timeout_ms=5000):
                log.append("Module B: RX timeout (no packet).")
                success = False
            else:
                plen, start = radio_b.get_rx_buffer_status()
                rx_b = radio_b.read_buffer(start, plen) if plen else []
                rx_bytes_b = bytes(rx_b)
                if rx_bytes_b != PING:
                    log.append(f"Module B: received {rx_bytes_b!r} (expected 'ping').")
                    success = False
                else:
                    log.append("Module B: received 'ping', sending 'pong'...")
                    if not radio_b.send_payload(PONG):
                        log.append("Module B: TX failed.")
                        success = False
                    else:
                        log.append("Module B: TX done.")
                        # A receives pong.
                        radio_a.clear_irq()
                        radio_a.start_rx(timeout_rtc=0)
                        if not radio_a.wait_rx_done(timeout_ms=5000):
                            log.append("Module A: RX timeout (no pong).")
                            success = False
                        else:
                            plen_a, start_a = radio_a.get_rx_buffer_status()
                            rx_a = radio_a.read_buffer(start_a, plen_a) if plen_a else []
                            rx_bytes_a = bytes(rx_a)
                            if rx_bytes_a != PONG:
                                log.append(f"Module A: received {rx_bytes_a!r} (expected 'pong').")
                                success = False
                            else:
                                t1 = time.monotonic()
                                rtt_ms = (t1 - t0) * 1000
                                log.append("Module A: received 'pong'.")
                                log.append("")
                                log.append("--- Result: PASS ---")
                                log.append(f"Round-trip time: {rtt_ms:.1f} ms")
                                success = True

        if not success and "Result:" not in "\n".join(log):
            log.append("")
            log.append("--- Result: FAIL ---")
    except Exception as e:
        log.append(f"Error: {e}")
        import traceback
        log.append(traceback.format_exc())
        log.append("")
        log.append("--- Result: FAIL ---")
        success = False
    finally:
        radio_a._close_spi()
        radio_b._close_spi()
        busy_a.close()
        nrst_a.close()
        rf_sw_a.close()
        busy_b.close()
        nrst_b.close()
        rf_sw_b.close()

    for line in log:
        print(line)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "a") as f:
            f.write("\n".join(log) + "\n")
        print(f"(Appended to {args.output})")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
