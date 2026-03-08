# SX1262 and Wio-SX1262 notes from datasheets and app notes

**Purpose:** Preserve the key setup and debug information from the Semtech SX1261/2 Datasheet, AN1200.59 (Reference Clock), and Seeed Wio-SX1262-N Module Datasheet so the PDFs do not need to stay in the repo. **The SX1262 datasheet PDF is not in the repo;** everything needed for the driver and troubleshooting is here or in the cited sources. Use this when changing the driver or debugging TX/RX/TCXO/errors.

**Sources (obtain from Semtech / Seeed if needed):**
- *SX1261/2 Data Sheet* DS.SX1261-2.W.APP Rev. 1.2 June 2019 (Semtech) — [semtech.com SX1262 product page](https://www.semtech.com/products/wireless-rf/lora-connect/sx1262)
- *AN1200.59* Selecting the Optimal Reference Clock Rev. 1.3 April 2022 (Semtech)
- *Wio-SX1262 / Wio-SX1262-N Module Datasheet* (Seeed)

---

## 0. Quick reference (no PDF needed)

**Command opcodes used in this project:** GetStatus 0xC0, SetStandby 0x80, SetRx 0x82, SetTx 0x83, SetPacketType 0x8A, SetRfFrequency 0x86, SetTxParams 0x8E, SetModulationParams 0x8B, SetPacketParams 0x8C, SetDioIrqParams 0x08, GetIrqStatus 0x12, ClrIrqStatus 0x02, WriteBuffer 0x0E, ReadBuffer 0x1E, GetRxBufferStatus 0x13, SetTcxoMode 0x97, SetRegulatorMode 0x96, SetPaConfig 0x95, Calibrate 0x89, CalibrateImage 0x98, SetBufferBaseAddress 0x8F, GetDeviceErrors 0x17, ClearDeviceErrors 0x07.

**SetStandby:** 0x00 = STDBY_RC (internal RC clock), 0x01 = STDBY_XOSC (32 MHz from TCXO/crystal). After reset the chip is in STDBY_RC.

**GetStatus (0xC0):** Returns 1 byte. ChipMode in bits [6:5]: 0 = STBY_RC, 1 = STBY_XOSC, 2 = FS, 3 = RX or TX. Wait for BUSY low before/after every SPI command.

**RF frequency:** freq_reg = (freq_Hz × 2^25) / 32_000_000 (24-bit); 32 MHz reference.

**Calibrate (0x89) param:** 0x7F = calibrate all blocks (RC64K, RC13M, PLL, ADC). Image calibration is separate (CalibrateImage 0x98).

**SetTx / SetRx:** 3-byte timeout in RTC steps (1 step = 15.625 µs). Timeout 0 = single shot (TX) or no timeout (RX).

---

## 1. SetDIO3AsTCXOCtrl (SetTcxoMode) — SX1262 datasheet Section 13.3.6

- **Opcode:** 0x97  
- **SPI transaction:** Byte 0 = 0x97, Byte 1 = tcxoVoltage, Bytes 2–4 = delay(23:0) (3 bytes, MSB first).

**tcxoVoltage (Byte 1):**

| Value | DIO3 output (TCXO supply) |
|-------|----------------------------|
| 0x00  | 1.6 V                      |
| 0x01  | 1.7 V                      |
| 0x02  | 1.8 V                      |
| 0x03  | 2.2 V                      |
| 0x04  | 2.4 V                      |
| 0x05  | 2.7 V                      |
| 0x06  | 3.0 V                      |
| 0x07  | 3.3 V                      |

Regulation is 200 mV below supply: VDDop > VTCXO + 200 mV.

**delay(23:0):**

- **Duration = Delay(23:0) × 15.625 µs.**
- If delay is **0**, the chip does **not** wait for the TCXO; the 32 MHz is not gated. If the 32 MHz from the TCXO is not detected at the end of the delay period, the error **XOSC_START_ERR** is flagged.
- Datasheet: *“The time needed for the 32 MHz to appear and stabilize can be controlled through the parameter delay(23:0).”* *“Most TCXO will not be immediately ready … the delay value will internally gate the 32 MHz coming from the TCXO to give enough time for this initial drift to stabilize.”*
- **Note:** *“The user should take the delay period into account when going into Tx or Rx mode from STDBY_RC mode. … To avoid increasing the switching mode time, the user can first set the device in STDBY_XOSC which will switch on the TCXO and wait for the delay period. Then, the user can set the device into Tx or Rx mode without suffering from any delay additional to the internal processing.”*

**XOSC_START_ERR at POR:** *“The XOSC_START_ERR flag will be raised at POR or at wake-up from Sleep mode in a cold-start condition, when a TCXO is used. It is an expected behaviour since the chip is not yet aware of being clocked by a TCXO. The user should simply clear this flag with the ClearDeviceErrors command.”*

---

## 2. TCXO start-up time — AN1200.59

- **Table 1 (SX1262 EVK 915 MHz):** Crystal start-up **150 µs** (with oscillator in SX1262); TCXO start-up **2 ms**.
- Use a **non-zero delay** in SetDIO3AsTCXOCtrl so the chip waits at least ~2 ms (e.g. 128 × 15.625 µs = 2 ms, or 320 = 5 ms) before using the 32 MHz clock.

---

## 3. Device errors — SX1262 datasheet Section 13.6

- **GetDeviceErrors:** Opcode **0x17**. Returns OpError(15:0) (2 bytes).
- **ClearDeviceErrors:** Opcode **0x07**, then **0x00, 0x00** (clears all errors; cannot clear independently).

**OpError bits (Table 13-85):**

| Bit | Name             | Meaning                    |
|-----|------------------|----------------------------|
| 0   | RC64K_CALIB_ERR  | RC64k calibration failed   |
| 1   | RC13M_CALIB_ERR  | RC13M calibration failed   |
| 2   | PLL_CALIB_ERR    | PLL calibration failed     |
| 3   | ADC_CALIB_ERR    | ADC calibration failed     |
| 4   | IMG_CALIB_ERR    | Image calibration failed   |
| 5   | **XOSC_START_ERR** | **XOSC failed to start** |
| 6   | PLL_LOCK_ERR     | PLL failed to lock          |
| 7   | RFU              | —                          |
| 8   | PA_RAMP_ERR      | PA ramping failed          |
| 15:9| RFU              | —                          |

Interpretation of a 16-bit error value (e.g. 0x0A20 or 0x200A depending on byte order): check which of these bits are set.

---

## 4. Basic Tx sequence — SX1262 datasheet Section 14.2

After power up or hard reset the chip is in STDBY_RC (BUSY low). Steps for basic Tx:

1. If not in STDBY_RC: SetStandby(0x00).  
2. SetPacketType (LoRa or FSK).  
3. SetRfFrequency.  
4. SetPaConfig.  
5. SetTxParams (power, ramp time).  
6. SetBufferBaseAddress.  
7. WriteBuffer (payload).  
8. SetModulationParams.  
9. SetPacketParams.  
10. SetDioIrqParams (e.g. TxDone on DIO1).  
11. WriteReg (sync word if needed).  
12. SetTx (with timeout param).  
13. Wait for IRQ TxDone or timeout; then chip goes to STDBY_RC.  
14. Clear IRQ TxDone.

**Command order (Section 14.4):** SetPacketType **must** be the **first** radio configuration command. Then SetModulationParams, then SetPacketParams. *“If this order is not respected, the behaviour of the device could be unexpected.”*

---

## 5. Other SX1262 datasheet details

- **SetRegulatorMode (0x96):** 0 = LDO only; 1 = DC_DC+LDO for STBY_XOSC, FS, RX, TX. Wio module uses DC-DC.
- **Calibrate (0x89):** Must be launched from **STDBY_RC**. BUSY high during calibration. Total time for all blocks **3.5 ms**. **Semtech SX126xLib Init()** runs **Calibrate(0x7F) right after SetStandby(STDBY_RC) and SetDio3AsTcxoCtrl**, with **no** SetPacketType or SetRfFrequency before it. If RC13M_CALIB_ERR/ADC_CALIB_ERR occur, run Calibrate (and CalibrateImage) before any packet type or RF frequency configuration.
- **CalibrateImage (0x98):** Takes **2 bytes** (band coefficients). 863–870 MHz: **0xD7, 0xDB**; 902–928 MHz: **0xE1, 0xE9** (both odd). Band-dependent; see “Image Calibration for Specific Frequency Bands” in datasheet.
- **GetStatus (0xC0):** Returns 1 byte (Status). Used to read chip mode and command status.

---

## 6. Wio-SX1262-N module (Seeed datasheet)

- **TCXO:** Supplied by SX1262 **DIO3**; configure in software. **TCXO voltage should be 200 mV below VCC** for proper operation. TCXO supply range 1.7–3.3 V.
- **Power:** DC-DC mode. Supply 3.3 V typical.
- **DIO2:** Internally connected to RF switch; logic high = transmitter mode. Module exposes **RF_SW** for external control (high = RX).
- **Frequency:** HF 862–930 MHz; 22 dBm max.
- Pinout and interfaces: see **wio-sx1262-module.md** in this folder (already aligned with Seeed datasheet).

---

## 7. Driver implementation notes (this project)

- **Init order:** Calibrate and CalibrateImage are run **before** SetPacketType and SetRfFrequency (Semtech SX126xLib order) to avoid RC13M/ADC calibration failures.
- TCXO: **SetTcxoMode** with tcxoVoltage **0x06** (3.0 V) and **delay = 320** (320 × 15.625 µs = 5 ms) so the chip gates the 32 MHz until the TCXO is stable. Delay 0 would cause XOSC_START_ERR.
- After **SetStandby(0x01)** (STDBY_XOSC), call **ClearDeviceErrors** once to clear XOSC_START_ERR (expected at POR with TCXO per datasheet); also in reset and before TX (clear_error()).
- **ClearDeviceErrors** payload: opcode **0x07** then **0x00, 0x00** (datasheet 13.6; clears all errors).
- After init, use **SetStandby(0x01)** (STDBY_XOSC) so the TCXO is on and delay has been applied before SetTx/SetRx; **start_tx()** also does SetStandby(0x01) + 5 ms before SetTx.
- Error register is read via get_error(); **decode_device_error()** returns a list of set bit names (OpError table above) for logging.
