# Raspberry Pi GPIO & hardware experiments

This project is for **experimenting with GPIO and interfacing with chips** on a Raspberry Pi (e.g. Pi 4). The repo includes a documentation system so you can track WIPs and modules, keep a hardware/software baseline, and work with agents in a consistent way.

The **`template` branch** holds the same doc system as a reusable template (minimal project-specific content). The **`main` branch** is this live experiment project.

## What's in here

- **`agent/`** — Main agent context (entry point for agents and project index):
  - **intro.md** — Entry point for agents (and project overview for humans). Read order, context sources, rules, best practices.
  - **new.md** — How to start a new WIP or create a new module. Branch naming, two workflows (new module vs change existing module).
  - **cleanup.md** — Final pass: sync module README/WIP docs, update env and index, push to the WIP branch.
  - **setup.md** — How the doc system is set up and how to initialize a new project (e.g. regenerate system-environment after copying).
  - **index.md** — Index of the whole project (agent docs and module folders with their context/).
  - **system-environment.md** — Hardware/software baseline (machine-specific; regenerate via setup when moving to a new machine).
- **Module folders** (e.g. **sx1262_gpio_test/**, **gpio-led-blink/**) — Each has a **README** (main module doc) and a **context/** subfolder with WIP doc(s), test summaries, and notes.

## Using the docs in this project

- **New chat:** Point the agent at `agent/intro.md` and the WIP doc you're working on (or at `agent/new.md` to start a new WIP/module).
- **End of session:** Say e.g. "clean up according to cleanup.md" to sync docs and push to the WIP branch.
- **Project index:** See `agent/index.md` for a map of the project.

## Using this as a template for another project

1. **Copy the whole repo** (or at least the `agent/` folder and any config you want) into your new project—or use the **template** branch as the starting point.
2. **Point an agent at `agent/setup.md`** and say "set yourself up." It will regenerate `agent/system-environment.md` for the new machine and optionally update the index.
3. **Start a chat** with intro + a WIP doc (or use `agent/new.md` to create one). Use `agent/cleanup.md` when you want a final sync and push.

For more detail, read `agent/intro.md` and `agent/setup.md`.
