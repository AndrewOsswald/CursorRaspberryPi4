# Module: GPIO LED blink

Minimal GPIO example: one LED on a Raspberry Pi, blinking at 1 Hz. For up-to-date state (wiring, code, what works), see **`context/current-state.md`**. Branches are per WIP (see each WIP doc for **Branch:** `main--<wip-slug>`).

---

## Project

This project is for experimenting with GPIO and interfacing with chips on a Raspberry Pi (e.g. Pi 4). The repo may have a single module or several; either is fine. This module is a minimal GPIO example (LED blink).

---

## Best practices

When suggesting wiring or hardware steps: **(1) Wiring** — Give a detailed explanation: what to connect where (pin numbers, names), in what order if it matters (e.g. power off first, GND before signal). Do not assume prior experience. **(2) Safety** — Warn about unsafe behaviors (short circuits, 5 V on GPIO, hot-plugging, reversed polarity, exceeding current). State the risk and how to avoid it. For hardware constraints (3.3 V only, pinout), use **`agent/system-environment.md`**. Release GPIO on exit; only one process should control a given pin at a time.

---

## Overview

Single LED on a GPIO pin, driven by a Python script (gpiozero), blinking at 1 Hz. Purpose: simple example of using GPIO on this Raspberry Pi.

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
python3 gpio-led-blink/blink_led.py
```

The LED blinks at 1 Hz. Stop with **Ctrl+C**; the script releases the GPIO when it exits.

---

## Deeper docs (in context/)

- `context/current-state.md` — Current state (for agents): wiring, code, working, not working, refs.
- `context/wip-gpio-led-blink.md` — WIP progress for this module.

---

## Related WIP doc(s)

- `context/wip-gpio-led-blink.md` — WIP progress for this module.
