"""
Minimal SX1262 LoRa driver for Raspberry Pi: SPI + GPIO (BUSY, NRST, RF_SW).

Uses spidev for one chip (CE0 or CE1). Caller manages which module; this class
holds spi (bus, dev), busy, nrst, rf_sw and implements wait_busy, cmd, and
LoRa init/TX/RX helpers. All commands wait for BUSY low before/after SPI.
"""

from __future__ import annotations

import time
from typing import Callable

# SX1262 command opcodes (from Semtech / ESPHome)
CMD_GET_STATUS = 0xC0
CMD_SET_STANDBY = 0x80
CMD_SET_RX = 0x82
CMD_SET_TX = 0x83
CMD_SET_PACKETTYPE = 0x8A
CMD_SET_RFFREQUENCY = 0x86
CMD_SET_TXPARAMS = 0x8E
CMD_SET_MODULATIONPARAMS = 0x8B
CMD_SET_PACKETPARAMS = 0x8C
CMD_SET_DIOIRQPARAMS = 0x08
CMD_GET_IRQSTATUS = 0x12
CMD_CLR_IRQSTATUS = 0x02
CMD_WRITE_BUFFER = 0x0E
CMD_READ_BUFFER = 0x1E
CMD_GET_RXBUFFERSTATUS = 0x13
CMD_SET_TCXOMODE = 0x97
CMD_SET_REGULATORMODE = 0x96
CMD_CALIBRATE = 0x89
CMD_CALIBRATEIMAGE = 0x98
CMD_SET_BUFFERBASEADDRESS = 0x8F
CMD_GET_ERROR = 0x17
CMD_CLR_ERROR = 0x07

# LoRa
PACKET_TYPE_LORA = 0x01
LORA_BW_125000 = 0x04
LORA_CR_4_5 = 0x01
IRQ_TX_DONE = 0x0001
IRQ_RX_DONE = 0x0002

# 32 MHz XTAL: freq_reg = freq_Hz * 2^25 / 32e6
def freq_to_reg(freq_hz: float) -> int:
    return int(freq_hz * (1 << 25) / 32_000_000) & 0xFFFFFF


def _ms(ms: float) -> None:
    time.sleep(ms / 1000.0)


class SX1262:
    """One SX1262 on a given spidev (bus, dev) with GPIO for BUSY, NRST, RF_SW."""

    def __init__(
        self,
        spi_bus: int,
        spi_dev: int,
        busy_read: Callable[[], bool],
        nrst_high: Callable[[], None],
        nrst_low: Callable[[], None],
        rf_sw_rx: Callable[[], None],
        rf_sw_tx: Callable[[], None],
        spi_max_hz: int = 2_000_000,
    ) -> None:
        self._bus = spi_bus
        self._dev = spi_dev
        self._busy_read = busy_read
        self._nrst_high = nrst_high
        self._nrst_low = nrst_low
        self._rf_sw_rx = rf_sw_rx
        self._rf_sw_tx = rf_sw_tx
        self._spi_max_hz = spi_max_hz
        self._spi = None

    def _open_spi(self) -> None:
        import spidev
        if self._spi is None:
            self._spi = spidev.SpiDev()
            self._spi.open(self._bus, self._dev)
            self._spi.mode = 0
            self._spi.max_speed_hz = self._spi_max_hz

    def _close_spi(self) -> None:
        if self._spi is not None:
            try:
                self._spi.close()
            except Exception:
                pass
            self._spi = None

    def wait_busy(self, timeout_ms: float = 500) -> bool:
        deadline = time.monotonic() + (timeout_ms / 1000.0)
        while time.monotonic() < deadline:
            if not self._busy_read():
                return True
            _ms(2)
        return False

    def cmd(self, tx: list[int], read_len: int = 0) -> list[int]:
        """Send command tx; optionally read read_len bytes. Waits BUSY before and after."""
        if not self.wait_busy():
            raise RuntimeError("BUSY did not go low before cmd")
        self._open_spi()
        if read_len > 0:
            tx = tx + [0] * read_len
        rx = self._spi.xfer2(tx)
        if not self.wait_busy():
            pass  # non-fatal
        if read_len > 0:
            return list(rx[-read_len:])
        return list(rx)

    def reset(self) -> None:
        self._nrst_low()
        _ms(10)
        self._nrst_high()
        _ms(150)
        self._rf_sw_rx()
        self.cmd([CMD_CLR_ERROR, 0x07])  # clear all errors

    def init_lora(
        self,
        freq_hz: float = 868_000_000,
        sf: int = 7,
        bw: int = LORA_BW_125000,
        cr: int = LORA_CR_4_5,
        preamble_len: int = 8,
        payload_len: int = 4,
    ) -> None:
        """Configure LoRa: packet type, frequency, modulation, packet params. Enables TCXO."""
        # Standby RC (0x00); XOSC (0x01) can be used but RC often used before TX)
        self.cmd([CMD_SET_STANDBY, 0x00])
        # TCXO: 3.0 V, 0 ms delay (Wio module needs TCXO)
        self.cmd([CMD_SET_TCXOMODE, 0x06, 0x00, 0x00, 0x00])
        _ms(1)
        # Regulator: DC-DC (datasheet for high power)
        self.cmd([CMD_SET_REGULATORMODE, 0x01])
        # Packet type LoRa
        self.cmd([CMD_SET_PACKETTYPE, PACKET_TYPE_LORA])
        # Frequency
        r = freq_to_reg(freq_hz)
        self.cmd([CMD_SET_RFFREQUENCY, (r >> 24) & 0xFF, (r >> 16) & 0xFF, (r >> 8) & 0xFF, r & 0xFF])
        # Calibrate all blocks (mask 0x7F)
        self.cmd([CMD_CALIBRATE, 0x7F])
        if not self.wait_busy(1000):
            raise RuntimeError("Calibrate BUSY timeout")
        # Image calibration for 862–930 MHz (band 0)
        self.cmd([CMD_CALIBRATEIMAGE, 0x00])
        if not self.wait_busy(1000):
            raise RuntimeError("CalibrateImage BUSY timeout")
        # TX params: +14 dBm, 200 us ramp
        self.cmd([CMD_SET_TXPARAMS, 14, 0x01])
        # Modulation: SF, BW, CR, LDRO=0
        self.cmd([CMD_SET_MODULATIONPARAMS, sf, bw, cr, 0x00])
        # Packet: preamble, header type 0 (explicit), payload len, CRC on, invert IQ 0
        self.cmd([CMD_SET_PACKETPARAMS, preamble_len >> 8, preamble_len & 0xFF, 0x00, payload_len, 0x01, 0x00])
        # TX/RX buffer base address 0
        self.cmd([CMD_SET_BUFFERBASEADDRESS, 0x00, 0x00])
        # DIO1 on TxDone and RxDone
        self.cmd([CMD_SET_DIOIRQPARAMS, (IRQ_TX_DONE | IRQ_RX_DONE) >> 8, (IRQ_TX_DONE | IRQ_RX_DONE) & 0xFF, 0, 0])

    def clear_irq(self) -> None:
        self.cmd([CMD_CLR_IRQSTATUS, 0xFF, 0xFF])

    def get_error(self) -> int:
        r = self.cmd([CMD_GET_ERROR, 0x00, 0x00], read_len=2)
        if len(r) < 2:
            return 0
        return (r[0] << 8) | r[1]

    def get_status(self) -> int:
        # GetStatus: send 2 bytes (cmd + dummy), chip returns [status, dummy]
        r = self.cmd([CMD_GET_STATUS, 0x00])
        return r[0] if len(r) >= 1 else 0

    def get_irq(self) -> int:
        r = self.cmd([CMD_GET_IRQSTATUS, 0x00, 0x00], read_len=2)
        if len(r) < 2:
            return 0
        return (r[0] << 8) | r[1]

    def write_buffer(self, offset: int, data: bytes | list[int]) -> None:
        if isinstance(data, bytes):
            data = list(data)
        self.cmd([CMD_WRITE_BUFFER, offset & 0xFF] + data)

    def read_buffer(self, offset: int, length: int) -> list[int]:
        r = self.cmd([CMD_READ_BUFFER, offset & 0xFF, length & 0xFF] + [0] * length, read_len=length)
        return r[:length] if len(r) >= length else r

    def get_rx_buffer_status(self) -> tuple[int, int]:
        r = self.cmd([CMD_GET_RXBUFFERSTATUS, 0x00, 0x00], read_len=2)
        if len(r) < 2:
            return 0, 0
        payload_len = r[0]
        rx_start = r[1]
        return payload_len, rx_start

    def start_tx(self, timeout_rtc: int = 0) -> None:
        """Start TX. timeout_rtc: 0 = single shot (no timeout); else RTC steps (15.625 us)."""
        self._rf_sw_tx()
        self.cmd([CMD_SET_TX, (timeout_rtc >> 16) & 0xFF, (timeout_rtc >> 8) & 0xFF, timeout_rtc & 0xFF])

    def start_rx(self, timeout_rtc: int = 0) -> None:
        """timeout_rtc: 0 = no timeout (single RX until packet or manual stop)."""
        self._rf_sw_rx()
        self.cmd([CMD_SET_RX, (timeout_rtc >> 16) & 0xFF, (timeout_rtc >> 8) & 0xFF, timeout_rtc & 0xFF])

    def wait_tx_done(self, timeout_ms: float = 5000) -> bool:
        _ms(50)  # allow chip to enter TX and start sending
        deadline = time.monotonic() + (timeout_ms / 1000.0)
        while time.monotonic() < deadline:
            irq = self.get_irq()
            if irq & IRQ_TX_DONE:
                self.clear_irq()
                return True
            _ms(5)
        return False

    def wait_rx_done(self, timeout_ms: float = 10000) -> bool:
        deadline = time.monotonic() + (timeout_ms / 1000.0)
        while time.monotonic() < deadline:
            irq = self.get_irq()
            if irq & IRQ_RX_DONE:
                self.clear_irq()
                return True
            if irq & 0x40:  # CRC error
                self.clear_irq()
                return False
            _ms(5)
        return False

    def receive_payload(self, timeout_ms: float = 10000) -> bytes | None:
        self.clear_irq()
        self.start_rx(timeout_rtc=0)
        if not self.wait_rx_done(timeout_ms):
            return None
        plen, start = self.get_rx_buffer_status()
        if plen == 0:
            return None
        data = self.read_buffer(start, plen)
        return bytes(data)

    def send_payload(self, payload: bytes | list[int], timeout_ms: float = 5000) -> bool:
        if isinstance(payload, bytes):
            payload = list(payload)
        self.clear_irq()
        self.write_buffer(0, payload)
        self.start_tx()
        ok = self.wait_tx_done(timeout_ms)
        self._rf_sw_rx()
        return ok
