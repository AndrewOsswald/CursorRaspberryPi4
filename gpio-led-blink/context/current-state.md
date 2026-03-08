# Current state — GPIO LED blink (for agents)

**Start here for this module.** You don't need the whole-project description—this file is the agent entry for this part of the project. It tells you what the code is and does, how it fits in the repo, the rules for working on it, and the current state. Update this file as the module changes.

---

## What this module is

A minimal GPIO example: one LED on a single Raspberry Pi GPIO pin, driven by a Python script (gpiozero), blinking at 1 Hz. The code is one script: `blink_led.py`. It sets the pin to output, toggles it on a 1 s timer, and releases the GPIO on exit. Purpose: simple, runnable example of using GPIO on this board so you can verify wiring and tooling before doing more complex hardware (e.g. SPI, multiple pins).

---

## How it fits in the project

The repo may have one module or several (e.g. this blink example plus other hardware or software modules). Each module is a folder at repo root with its own README, context/, and code. This module is the minimal GPIO example; others might add chips, radios, or different stacks. You only need to understand this module to work on it.

---

## Rules for working on this module

- **Wiring:** Spell out what to connect where (pin numbers, names), in what order (e.g. power off first, GND before signal). Do not assume prior experience.
- **Safety:** Warn about risks: short circuits, 5 V on GPIO (not 5 V tolerant), hot-plugging, reversed polarity, exceeding current. State the risk and how to avoid it. For pinout and 3.3 V constraints, use **`agent/system-environment.md`**.
- **GPIO discipline:** Release GPIO on exit (set to input or close handle). Only one process should control a given pin at a time. Don't connect or disconnect wires while the pin is active—power off or set pin to input first.
- **Coding:** Keep the script small and readable; use gpiozero (or rpi-lgpio) as in this project; avoid legacy RPi.GPIO on current OS.

---

## Wiring

- LED anode → 330 Ω resistor → GPIO 17 (BCM; physical pin 11). LED cathode → GND (e.g. pin 9). Pi powered off when changing wires.

## Code

- `gpio-led-blink/blink_led.py` — gpiozero, 1 Hz blink on GPIO 17; GPIO released on exit.

## Working

- Script and docs in place; ready to wire and run on board.

## Not working / limitations

- Not yet tested on board until wiring is done.

## Next / refs

- **WIP:** `context/wip-gpio-led-blink.md` (branch main--gpio-led-blink).
- **Run:** `python3 gpio-led-blink/blink_led.py` from repo root. Wiring steps and safety in `../README.md`.
- **Hardware:** `agent/system-environment.md` (pinout, 3.3 V).
