# Wio-SX1262 module — description and operation

**Purpose:** Describes the Wio-SX1262 module (not just the bare SX1262 IC): what’s on the module, pinout, interfaces, and how to connect it to a host MCU. For feature context see `feature.md` in this folder.

**Audience:** Humans and AI. Use this when wiring or writing software for the ping test or any feature using this module.

---

## What the Wio-SX1262 is

The **Wio-SX1262** is a compact RF module from Seeed Studio built around the **Semtech SX1262** sub‑GHz transceiver IC. The module adds:

- **Power:** DC-DC power distribution (not LDO), so it can deliver high TX current efficiently.
- **Frequency reference:** A high-precision active **TCXO**; its supply is controlled by the SX1262’s DIO3 (see below).
- **RF path:** Internal RF switch (gate) for TX/RX; control is exposed as **RF_SW** and is tied to the IC’s DIO2 behavior.
- **RF port:** 50 Ω interface — either **IPEX** connector (Wio-SX1262) or **SMT pin** (Wio-SX1262-N). A π-type matching network is recommended on the host board for antenna tuning.

So “how it works” is: host talks to the SX1262 over **SPI**; drives **NRST**, **RF_SW**, and watches **BUSY** and **DIO1**; the module handles DC-DC, TCXO, and the internal RF switch so you get a clean 862–930 MHz (HF band) LoRa/FSK radio with up to 22 dBm output.

---

## Modulations and frequency

- **Modulations:** (G)FSK and **LoRa®**.
- **LoRa bandwidth:** 7.8 kHz to 500 kHz.
- **Frequency range (this module):** **862–930 MHz** (HF band); 22 dBm max output in that range.
- **Receiver sensitivity (typical):** -136.73 dBm @ SF12, BW 125 kHz (862–930 MHz, including line loss).

---

## Pinout (12-pin SMT)


| Pin | Name  | Direction | Description                                                                                                                 |
| --- | ----- | --------- | --------------------------------------------------------------------------------------------------------------------------- |
| 1   | RF_SW | I         | External control of internal RF switch. **High = receiver mode**, low = other (e.g. TX).                                    |
| 2   | MISO  | I/O       | SPI MISO (data from module to MCU).                                                                                         |
| 3   | MOSI  | I/O       | SPI MOSI (data from MCU to module).                                                                                         |
| 4   | SCK   | I/O       | SPI clock.                                                                                                                  |
| 5   | NRST  | I         | Reset, **active low**.                                                                                                      |
| 6   | NSS   | I/O       | SPI slave select (chip select).                                                                                             |
| 7   | GND   | —         | Ground.                                                                                                                     |
| 8   | VCC   | I         | Supply voltage for the module (3.3 V typical).                                                                              |
| 9   | ANT   | I/O       | RF input/output. Wio-SX1262-N: SMT pin; Wio-SX1262: IPEX only (no pin 9 as RF).                                             |
| 10  | GND   | —         | Ground.                                                                                                                     |
| 11  | BUSY  | O         | **Busy** indicator: module is ready for a new SPI command only when BUSY is **low**. Must be checked before/after commands. |
| 12  | DIO1  | I/O       | Multi-purpose digital I/O; **DIO1 of SX1262** — used as the generic **IRQ** line (e.g. RX done, TX done).                   |


**Note on DIO2 / DIO3 (internal to the IC, not brought out as separate pins):**

- **DIO2** is internally connected to the RF switch (logic high = transmitter mode; otherwise low). The module exposes **RF_SW** for external control of the same switch (high = RX). So RX/TX path selection is either via RF_SW or via the IC’s DIO2 configuration.
- **DIO3** is used as the **TCXO voltage supply** output. It must be enabled and configured in software; TCXO voltage should be **200 mV below VCC** for proper operation. Typical TCXO supply range: 1.7–3.3 V.

---

## Host interfaces (summary)

- **SPI:** One group of SPI (NSS, SCK, MOSI, MISO) for all SX1262 register and packet access.
- **DIO1:** Generic IRQ from the SX1262 (e.g. packet RX/TX done); use for interrupt-driven handling.
- **RF_SW:** One external GPIO to control the internal RF switch (e.g. high for RX).
- **BUSY:** Must be read before and after each SPI transaction; only send a new command when BUSY is low.
- **NRST:** Active-low reset; recommended for reliable startup and recovery.
- **RF output:** 50 Ω; IPEX or SMT depending on variant. Reserve a π-type matching network on the host for the antenna.

---

## Electrical characteristics (typical)


| Parameter         | Value                                        |
| ----------------- | -------------------------------------------- |
| Supply voltage    | 3.3 V typical                                |
| Sleep current     | 1.62 µA                                      |
| SX1262 power mode | DC-DC (on this module)                       |
| TCXO supply       | Via SX1262 DIO3; 1.7–3.3 V; 200 mV below VCC |
| TX current (max)  | 125 mA @ 22 dBm, 862–930 MHz                 |
| RX current        | 7.6 mA @ BW 125 kHz, 862–930 MHz             |
| Output power      | 22 dBm max @ 862–930 MHz                     |
| Harmonics (HF)    | ≤ -45 dBm above 1 GHz                        |


---

## Reference design: connecting to an MCU

A typical reference design (e.g. “Figure 10 Reference Design Based on Wio-SX1262” in the module documentation) connects the Wio-SX1262 to a host MCU as follows. The antenna interface uses 50 Ω impedance with a recommended π-type matching network (series inductor, shunt capacitors to GND) to an antenna connector.

**MCU → Module:**


| MCU signal | Module pin | Role                                   |
| ---------- | ---------- | -------------------------------------- |
| SPI_MISO   | 2 (MISO)   | SPI data from module                   |
| SPI_MOSI   | 3 (MOSI)   | SPI data to module                     |
| SPI_CLK    | 4 (SCK)    | SPI clock                              |
| NRST       | 5 (NRST)   | Reset (active low)                     |
| SPI_NSS    | 6 (NSS)    | SPI chip select                        |
| DIO        | 12 (DIO1)  | IRQ / multi-purpose                    |
| BUSY       | 11 (BUSY)  | Busy indicator (read before/after SPI) |
| IO         | 1 (RF_SW)  | RF switch control (high = RX)          |


**Power and RF:**

- **VCC** (pin 8) and **GND** (pins 7, 10) to 3.3 V and ground.
- **ANT** (pin 9 on -N variant; IPEX on standard): through a **π-type matching network** (50 Ω) to the antenna or connector. Matching components (e.g. series inductor, shunt caps) are often left as NC initially and populated for tuning.

**Software sequence (conceptual):**

1. Hold NRST low, then release (or pulse) for a clean reset.
2. Drive RF_SW as needed (e.g. high for RX).
3. Before each SPI command: wait until BUSY is low.
4. Perform SPI transaction (NSS low, then clock data).
5. After command: wait until BUSY is low again before next command.
6. Use DIO1 (IRQ) for RX done / TX done so the host can react without polling only.

---

## Variants

- **Wio-SX1262:** RF via **IPEX** connector (default); no SMT RF pin.
- **Wio-SX1262-N:** RF via **SMT pin** (pin 9 ANT); no IPEX.

Both support 862–930 MHz and 22 dBm in that band.

---

## Physical

- **Size:** 11.6 (W) × 11 (L) × 2.95 (H) mm.
- **Package:** 12 pins, SMT.

---

## References and further reading

- Semtech SX1262 datasheet (SPI, BUSY, DIO1/DIO2/DIO3, command set).
- Seeed Studio Wio-SX1262 product page and wiki for module-specific specs and reference schematic.
- `docs/system-environment.md` for host pinout (e.g. Pi SPI/GPIO) when wiring two modules to one host.

