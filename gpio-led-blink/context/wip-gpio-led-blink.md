# WIP: GPIO LED blink

**Module details and current state:** See **`context/current-state.md`** in this folder (wiring, code, what works). README in parent folder is for humans (overview, how to run).

**Branch:** `main--gpio-led-blink`. One branch per WIP; cleanup pushes to this branch.

**Hardware context:** `agent/system-environment.md` (pinout, 3.3V only, BCM numbering).

**For a fresh agent:** Read `agent/intro.md`, then this WIP doc and **`context/current-state.md`** (and `../README.md` for overview/run if needed). For wiring and pins, read `agent/system-environment.md`. That set gives you the context needed to continue.

---

## Planned

- Wire LED and resistor to GPIO 17 and GND; run script on board and verify blink.

---

## In progress

- (nothing)

---

## Completed

- Created module folder `gpio-led-blink/` with README and this WIP doc in context/.
- Added `gpio-led-blink/blink_led.py` (gpiozero, GPIO 17, 1 Hz blink, GPIO released on exit).
- Updated `agent/index.md` with gpio-led-blink module.
- Added "How to wire and run" section to README (wiring steps, safety, run command).
