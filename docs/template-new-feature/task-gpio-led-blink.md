# Task: GPIO LED blink (template example)

**Template:** Copy this folder (and `feature.md`) when starting a new feature; rename folder and files to match. See `docs/new.md` for the convention. Written for both humans and agents.

**Feature details and active state:** See `feature.md` in this folder (wiring, code, what works).

**Branch:** `main--<task-slug>` (e.g. `main--gpio-led-blink`). One branch per task; set when the task is created; cleanup pushes to this branch.

**Hardware context:** `docs/system-environment.md` (pinout, 3.3V only, BCM numbering).

---

## Planned

- Add a second LED and alternate blink pattern.
- Add optional command-line argument for blink rate (e.g. `--interval 0.5`).
- Document wiring in the feature doc or a separate wiring diagram.

---

## In progress

- (nothing right now — move items here when you start working on them)

---

## Completed

- Chose GPIO 17 (physical pin 11) for LED output; verified pin is free on header. See pinout in `docs/system-environment.md`.
- Added script `scripts/blink_led.py` using gpiozero; LED blinks at 1 Hz.
- Tested on board; LED and 330 Ω resistor to GND. Active state recorded in `feature.md` in this folder.
