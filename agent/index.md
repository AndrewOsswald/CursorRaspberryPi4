# index.md — project index (with descriptions)

**For agents:** This index lists paths **and short descriptions of what's in each file**. Use it instead of inferring from the file structure: you can choose which files to open (e.g. "need test results" → test-summary; "need connection or config details" → wiring or config doc) without opening several files to find the right one. That saves steps and tokens, especially when there are many modules or many context files. Read **intro.md** first; intro gives read order.

**Humans:** Table of contents with one-line summaries so humans and agents can find the right doc quickly.

---

## Agent docs (shared context)

| Path | What's in it |
|------|--------------|
| agent/intro.md | Entry point. Where to get WIP state, module state, execution env; read order; paths; rules. Read first when user points you here. |
| agent/new.md | How to start a new WIP or create a new module. Module layout, WIP doc format, branch naming, step-by-step workflows. Use when user says to start a WIP or create a module. |
| agent/system-environment.md | Run environment for this project (OS, interfaces, config). Regenerated per machine. Use when WIP involves host, hardware, or run environment. |
| agent/cleanup.md | End-of-session pass: sync module README and WIP doc, update env/index, push to WIP branch. Use when user says "clean up according to cleanup.md". |
| agent/setup.md | Initialize a new project after copying agent folder. Regenerate system-environment; update this index if needed. Use when user says to set yourself up. |
| agent/index.md | This file. Paths and descriptions of agent docs and each module's key files. |

## Modules (path + what's in each key file)

Modules live at repo root. Each has a **README** (main doc), **context/** (WIP docs and notes), and code. When you need to choose what to read, use the descriptions below instead of opening files to peek.

### gpio-led-blink

| Path | What's in it |
|------|--------------|
| gpio-led-blink/README.md | For humans: overview, best practices, how to wire and run. Single-LED blink (gpiozero). |
| gpio-led-blink/context/current-state.md | For agents: start here for this module. What the code is and does, how it fits in the project, rules (best practices, what not to do), then wiring/code/working/not/next. |
| gpio-led-blink/context/wip-gpio-led-blink.md | WIP progress (Planned / In progress / Completed). Branch main--gpio-led-blink. Read order for fresh agent. |

### sx1262_gpio_test

| Path | What's in it |
|------|--------------|
| sx1262_gpio_test/README.md | For humans: overview, best practices, how to run each test. SX1262 GPIO/SPI/ping tests. |
| sx1262_gpio_test/context/current-state.md | For agents: start here for this module. What the code is and does, how it fits in the project, rules (SPI/BUSY discipline, safety, driver refs), then wiring/code/working/not/next. |
| sx1262_gpio_test/context/wip-sx1262-ping-test.md | WIP progress for ping test (Planned / In progress / Completed). Branch main--sx1262-ping-test. Context for next session. |
| sx1262_gpio_test/context/ping-test-summary.md | Ping test results, what was tried, failures and notes. |
| sx1262_gpio_test/context/spi-test-explained.md | How the SPI test works (GetStatus 0xC0), what to expect, BUSY/NSS. |
| sx1262_gpio_test/context/datasheet-and-an-notes.md | Datasheet and application note references and excerpts. |
| sx1262_gpio_test/context/wiring.md | Pin connections (BCM), what goes where; used by pin_config.py. |
| sx1262_gpio_test/context/wio-sx1262-module.md | Wio-SX1262 module details (pins, breakout). |

Code in each module folder (scripts, services, configs—README and current-state point to it).

---

When you add a new module or new context files: add a row here with path and a one-line description so the index stays useful for choosing what to read.
