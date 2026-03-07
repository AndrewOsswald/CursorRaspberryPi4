# Feature: GPIO LED blink

**Feature details and active state:** This doc. Branches are per task (see each task doc for **Branch:** `main--<task-slug>`). Cleanup pushes to the active task’s branch.

---

## Overview

- **What it is:** Single LED on a GPIO pin, driven by a Python script (gpiozero), blinking at 1 Hz.
- **Purpose:** Simple example of using GPIO on this Raspberry Pi.

---

## Active state

Update this section as the feature changes (wiring, code paths, what's working or broken).

- **Wiring:** LED anode → 330 Ω resistor → GPIO 17 (BCM; physical pin 11). LED cathode → GND (e.g. pin 9). Pi powered off when changing wires.
- **Code:** `scripts/blink_led.py` (gpiozero, 1 Hz blink). GPIO 17 set to output; released on exit.
- **Working:** Script and docs in place; ready to wire and run on board.
- **Not working / limitations:** Not yet tested on board until wiring is done.

---

## How to wire and run

**What you need:** One LED, one 330 Ω resistor (or 220–470 Ω), and two jumper wires. Use 3.3 V–compatible parts; do not connect 5 V to any GPIO.

**Safety:** Power the Pi off before connecting or disconnecting wires. Only one process should control GPIO 17 at a time. Do not short 3.3 V or 5 V to GND or to another pin.

**Wiring (Pi off):**

1. **Identify pins:** GPIO 17 = BCM 17 = **physical pin 11** (first pin on the left side of the header, second row). GND = **physical pin 9** (or 6, 14, 20, 25, 30, 34, 39).
2. **LED cathode (short leg, minus)** → connect to **GND** (e.g. pin 9).
3. **LED anode (long leg, plus)** → connect to one leg of the **330 Ω resistor**. Connect the other leg of the resistor to **GPIO 17 (pin 11)**.

So the path is: **Pin 11 (GPIO 17)** → resistor → LED anode; **LED cathode** → **Pin 9 (GND)**.

**Run the script:**

```bash
python3 scripts/blink_led.py
```

The LED blinks at 1 Hz. Stop with **Ctrl+C**; the script releases the GPIO when it exits.

---

## Deeper docs (in this folder)

- *(None yet; add e.g. `wiring.md` and reference here if needed.)*

---

## Related task doc(s)

- `task-gpio-led-blink.md` in this folder — task progress for this feature.
