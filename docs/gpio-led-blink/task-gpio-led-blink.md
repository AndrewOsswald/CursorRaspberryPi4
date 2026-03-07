# Task: GPIO LED blink

**Feature details and active state:** See `feature.md` in this folder (wiring, code, what works).

**Branch:** `main--gpio-led-blink`. Cleanup pushes to this branch.

**Hardware context:** `docs/system-environment.md` (pinout, 3.3V only, BCM numbering).

---

## Planned

- Wire LED and resistor to GPIO 17 and GND; run script on board and verify blink.

---

## In progress

- (nothing)

---

## Completed

- Created feature folder `docs/gpio-led-blink/` with feature.md and this task doc.
- Added `scripts/blink_led.py` (gpiozero, GPIO 17, 1 Hz blink, GPIO released on exit).
- Updated `docs/docs-index.md` with gpio-led-blink folder.
- Added "How to wire and run" section to `feature.md` (wiring steps, safety, run command).
