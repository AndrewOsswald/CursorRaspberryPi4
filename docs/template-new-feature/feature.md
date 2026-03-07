# Feature: GPIO LED blink (template example)

**Template:** Copy this folder when starting a new feature; rename folder and update docs. See `docs/new.md` for conventions. Written for both humans and agents.

Branches are per task (see each task doc for **Branch:** `main--<task-slug>`). Cleanup pushes to the active task’s branch.

---

## Overview

- **What it is:** Single LED on a GPIO pin, driven by a Python script (gpiozero), blinking at 1 Hz.
- **Purpose:** Template for a minimal GPIO output feature and its docs.

---

## Active state

Update this section as the feature changes (wiring, code paths, what's working or broken).

- **Wiring:** LED anode → 330 Ω resistor → GPIO 17 (BCM; physical pin 11). LED cathode → GND (e.g. pin 9). Pi powered off when changing wires.
- **Code:** `scripts/blink_led.py` (gpiozero, 1 Hz blink). GPIO 17 set to output; released on exit.
- **Working:** Blink runs on board; no errors. Pin and resistor within current limits (see `docs/system-environment.md`).
- **Not working / limitations:** (none for this template)

---

## Deeper docs (in this folder)

- *(none for this template; add e.g. `wiring.md`, `design-notes.md` and reference them here when you create deeper docs)*

---

## Related task doc(s)

- `task-gpio-led-blink.md` in this folder — task progress (planned / in progress / completed) for this feature. (A feature can have multiple task docs; list each here.)
