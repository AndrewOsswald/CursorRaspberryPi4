# Wiring: Two Wio-SX1262 modules to Raspberry Pi 4

**Purpose:** Connect both Wio-SX1262 modules to the same Pi 4 over SPI so you can get them talking (and later run the ping test from one host). Each module gets its own chip select (NSS) and its own GPIOs for NRST, BUSY, DIO1, and RF_SW.

**Hardware context:** Pi 4 pinout and 3.3 V constraints in `docs/system-environment.md`. Module pinout in `wio-sx1262-module.md` in this folder.

---

## Is it possible?

Yes. The Pi 4 has **SPI0** with two chip-select outputs (CE0 and CE1). You share MOSI, MISO, and SCLK between both modules and use CE0 for module A and CE1 for module B. Each module also needs four dedicated GPIOs: NRST, BUSY, DIO1, RF_SW. The Pi has enough free GPIOs for that.

---

## Safety (read first)

- **Power off the Pi** (shutdown, then unplug power) before connecting or changing any wires. Do not hot-plug the modules.
- **3.3 V only.** Pi GPIO and the modules are 3.3 V. Do not connect 5 V to any module pin or GPIO; it can damage the Pi and the module.
- **Polarity:** Double-check VCC and GND. Reversed power can damage the module.
- **Current:** Each module can draw up to ~125 mA when transmitting. Both on Pi 3.3 V is OK for normal use (e.g. one TX at a time). If you stress-test with both transmitting at once, the Pi’s 3.3 V rail may be marginal; use an external 3.3 V supply for the radios if you see brownouts.
- **Connect GND first** between Pi and each module, then power and signals, so you don’t float signals during wiring.

---

## Pin assignment summary

| Function   | Pi 4 (BCM) | Physical pin | Module A pin | Module B pin | Wire color |
|-----------|------------|--------------|--------------|---------------|------------|
| SPI MOSI  | 10         | 19           | 3 (MOSI)     | 3 (MOSI)      | Orange     |
| SPI MISO  | 9          | 21           | 2 (MISO)     | 2 (MISO)      | Yellow     |
| SPI SCLK  | 11         | 23           | 4 (SCK)      | 4 (SCK)       | Green      |
| NSS (CS)  | 8 (CE0)    | 24           | 6 (NSS)      | —             | Blue (A)   |
| NSS (CS)  | 7 (CE1)    | 26           | —            | 6 (NSS)       | Violet (B) |
| NRST      | 17         | 11           | 5 (NRST)     | —             | Blue (A)   |
| NRST      | 25         | 22           | —            | 5 (NRST)      | Violet (B) |
| BUSY      | 18         | 12           | 11 (BUSY)    | —             | Blue (A)   |
| BUSY      | 5          | 29           | —            | 11 (BUSY)     | Violet (B) |
| DIO1      | 22         | 15           | 12 (DIO1)    | —             | Blue (A)   |
| DIO1      | 6          | 31           | —            | 12 (DIO1)     | Violet (B) |
| RF_SW     | 23         | 16           | 1 (RF_SW)    | —             | Blue (A)   |
| RF_SW     | 12         | 32           | —            | 1 (RF_SW)     | Violet (B) |
| 3.3 V     | —          | 1 or 17      | 8 (VCC)      | 8 (VCC)       | Red        |
| GND       | —          | 6, 9, 14, 20, 25, 30, 34, 39 | 7, 10 (GND) | 7, 10 (GND)   | Black      |

SPI and power can be shared; NSS, NRST, BUSY, DIO1, and RF_SW are per-module.

---

## Board labels: Wio-SX1262 for XIAO carrier

If your module is the **Wio-SX1262 for XIAO** (carrier board with pin headers and labels on the back), there are no pin numbers—use the **labels** instead. Mapping from board label to the same Pi connections (wire colors unchanged):

| Board label (on back) | Same as | Pi connection (see tables above) |
|----------------------|---------|-----------------------------------|
| **3V3** | VCC | Pi 3.3 V (pin 1 or 17) — **use 3V3, not VIN, when powering from Pi** |
| **GND** | GND | Pi GND |
| **MOSI** | SPI MOSI | Pi pin 19 (Orange) |
| **MISO** | SPI MISO | Pi pin 21 (Yellow) |
| **SCK** | SPI SCLK | Pi pin 23 (Green) |
| **NSS** | Chip select | Module A: Pi pin 24 (Blue). Module B: Pi pin 26 (Violet). |
| **RST** | NRST (reset) | Module A: Pi pin 11 (Blue). Module B: Pi pin 22 (Violet). |
| **BUSY** | Busy | Module A: Pi pin 12 (Blue). Module B: Pi pin 29 (Violet). |
| **DIO1** | DIO1 / IRQ | Module A: Pi pin 15 (Blue). Module B: Pi pin 31 (Violet). |
| **RF_SW** | RF switch | Module A: Pi pin 16 (Blue). Module B: Pi pin 32 (Violet). |
| **DO** | RF out / ANT | Antenna or 50 Ω load (do not leave open). |
| **VIN** | — | Unused when powering from Pi 3.3 V; use **3V3** only. |
| **D6**, **D7** | — | Not needed for this wiring. |

So for each wire: same Pi pin and color as in the step-by-step below; on the module side, connect to the **labeled header** (e.g. Module A **RST**, **BUSY**, **DIO1**, **RF_SW**, **NSS**, **3V3**, **GND**, and **MOSI** / **MISO** / **SCK**).

---

## Wire color code

Use the same color for each signal so you can trace and debug easily. Suggested scheme:

| Color    | Signal / use |
|----------|----------------|
| **Red**  | 3.3 V (VCC) |
| **Black**| GND |
| **Orange** | SPI MOSI (shared) |
| **Yellow**  | SPI MISO (shared) |
| **Green**   | SPI SCLK (shared) |
| **Blue**    | Module A — NSS, NRST, BUSY, DIO1, RF_SW (use one shade, or blue + stripe for one of them) |
| **Violet/Purple** | Module B — NSS, NRST, BUSY, DIO1, RF_SW |

If you don’t have enough shades to give every control line a unique color, keep **power (red/black)** and **SPI (orange/yellow/green)** consistent, and use **blue for Module A** and **violet for Module B** for all four control wires per module; label the ends (e.g. tape + marker: “A-NRST”, “B-BUSY”) so you don’t mix them.

---

## Step-by-step wiring

*(Module side uses the **board labels** on the Wio-SX1262 for XIAO carrier—3V3, GND, MOSI, MISO, SCK, NSS, RST, BUSY, DIO1, RF_SW, DO. If you have the raw 12-pin SMT module instead, see the Board labels table above for pin-number mapping.)*

**1. Power off the Pi** (shutdown, then disconnect power).

**2. On each module, find the labeled pads/headers** on the back: **3V3**, **GND**, **MOSI**, **MISO**, **SCK**, **NSS**, **RST**, **BUSY**, **DIO1**, **RF_SW**, **DO**.

**3. Connect grounds first (black).**  
- **Black:** Pi physical pin 6 (GND) → Module A **GND**.  
- **Black:** Pi physical pin 9 (GND) → Module A **GND** (second pad if present).  
- **Black:** Pi physical pin 14 (GND) → Module B **GND**.  
- **Black:** Pi physical pin 20 (GND) → Module B **GND** (second pad if present).  
(Or use a single GND rail on a breadboard; ensure Pi GND and both modules’ GND are tied together.)

**4. Connect 3.3 V (red).**  
- **Red:** Pi physical pin 1 (3.3 V) → Module A **3V3**.  
- **Red:** Pi physical pin 17 (3.3 V) → Module B **3V3**.  
(Use **3V3** only—not VIN—when powering from the Pi.)

**5. Connect shared SPI (orange, yellow, green — to both modules).**  
- **Orange:** Pi pin 19 (GPIO 10, MOSI) → Module A **MOSI** and Module B **MOSI**.  
- **Yellow:** Pi pin 21 (GPIO 9, MISO) → Module A **MISO** and Module B **MISO**.  
- **Green:** Pi pin 23 (GPIO 11, SCLK) → Module A **SCK** and Module B **SCK**.

**6. Connect chip select (NSS).**  
- **Blue:** Pi pin 24 (GPIO 8, CE0) → **only** Module A **NSS**.  
- **Violet:** Pi pin 26 (GPIO 7, CE1) → **only** Module B **NSS**.

**7. Connect Module A control pins (blue — label ends A-RST, A-BUSY, A-DIO1, A-RF_SW).**  
- **Blue:** Pi pin 11 (GPIO 17) → Module A **RST**.  
- **Blue:** Pi pin 12 (GPIO 18) → Module A **BUSY**.  
- **Blue:** Pi pin 15 (GPIO 22) → Module A **DIO1**.  
- **Blue:** Pi pin 16 (GPIO 23) → Module A **RF_SW**.

**8. Connect Module B control pins (violet — label ends B-RST, B-BUSY, B-DIO1, B-RF_SW).**  
- **Violet:** Pi pin 22 (GPIO 25) → Module B **RST**.  
- **Violet:** Pi pin 29 (GPIO 5) → Module B **BUSY**.  
- **Violet:** Pi pin 31 (GPIO 6) → Module B **DIO1**.  
- **Violet:** Pi pin 32 (GPIO 12) → Module B **RF_SW**.

**9. Antenna.**  
Connect an antenna (or 50 Ω load) to each module’s **DO** (RF output). Do not run the radios without an antenna or load; it can damage the PA.

**10. Double-check.**  
- No 5 V on any module or GPIO.  
- All GNDs common.  
- No shorts between pins.  
- NSS/CE0 only to module A, NSS/CE1 only to module B.

**11. Power on the Pi** and enable SPI if needed (see below).

---

## SPI on the Pi

- **Devices:** Module A = `/dev/spidev0.0` (CE0), Module B = `/dev/spidev0.1` (CE1).
- **Enable SPI:** In `/boot/firmware/config.txt` ensure `dtparam=spi=on` is present (no `#`). Reboot. Then `ls /dev/spidev0.*` should show `spidev0.0` and `spidev0.1`.
- **Permissions:** Your user needs access to SPI (e.g. in group `spi`). Check with `groups`; add with `sudo usermod -aG spi $USER` and log out/in if needed.

---

## Software notes (for when you add code)

- **BUSY:** Before and after every SPI transaction to a module, read the BUSY GPIO for that module; only send a command when BUSY is low.
- **NSS:** Drive the correct CE (8 for A, 7 for B) low for the module you’re talking to; leave the other high so only one module is selected.
- **NRST:** Hold low for a few ms, then release (high) for a clean reset before init.
- **RF_SW:** High = receiver mode; drive as needed for RX/TX (or match your driver’s expectations).

---

## Quick reference: Pi physical pins used

| Pin | Use        | Color  | Pin | Use        | Color  |
|-----|------------|--------|-----|------------|--------|
| 1   | 3.3 V (A)  | Red    | 2   | 5 V (unused) | —      |
| 6   | GND        | Black  | 9   | GND        | Black  |
| 11  | GPIO 17 (A NRST) | Blue  | 12 | GPIO 18 (A BUSY) | Blue  |
| 14  | GND        | Black  | 15  | GPIO 22 (A DIO1) | Blue  |
| 16  | GPIO 23 (A RF_SW) | Blue | 17 | 3.3 V (B)  | Red    |
| 19  | MOSI       | Orange| 20  | GND        | Black  |
| 21  | MISO       | Yellow| 22  | GPIO 25 (B NRST) | Violet |
| 23  | SCLK       | Green | 24  | CE0 (A NSS) | Blue   |
| 25  | GND        | Black | 26  | CE1 (B NSS) | Violet |
| 29  | GPIO 5 (B BUSY) | Violet | 31 | GPIO 6 (B DIO1) | Violet |
| 32  | GPIO 12 (B RF_SW) | Violet |   |            |        |
