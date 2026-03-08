# Task: SX1262 ping test (two chips)

**Feature details and active state:** See `feature.md` in this folder (wiring, code, what works).

**Branch:** `main--sx1262-ping-test`. One branch per task; cleanup pushes to this branch.

**Hardware context:** `docs/system-environment.md` (pinout, 3.3V only, BCM numbering, SPI).

---

## Planned

- Get chip/module details from user (pins, SPI vs other interface, host, existing drivers or libraries).
- Define wiring for two SX1262 modules to the host (e.g. one Pi): which GPIO/SPI/CS per chip, power, antenna.
- Implement a ping test: one chip sends a ping packet; the other receives it and sends a reply; first chip receives the reply. Report success/failure (e.g. round-trip time or pass/fail).
- Document wiring and usage in the feature doc (and deeper docs in this folder as needed).

---

## In progress

- (nothing right now — documentation created; waiting on user’s chip details before implementation)

---

## Completed

- Created feature folder `docs/sx1262-ping-test/` with `feature.md` and this task doc.
- Documented the goal: test two SX1262 radios by pinging them off each other. Stopping after documentation; implementation to follow once chip details are provided.
