# Agent context template

This branch contains **only the agent context files**—no module folders. Use it as a starting point for a new project: copy this repo (or clone and checkout `template`), then have an agent run **`agent/setup.md`** to initialize for your machine.

## What's in here

- **`agent/`** — Shared agent context:
  - **intro.md** — Entry point for agents. Read order, context sources, rules.
  - **new.md** — How to start a new WIP or create a new module.
  - **cleanup.md** — Final pass: sync docs, push to the WIP branch.
  - **setup.md** — Initialize a new project (regenerate system-environment, update index).
  - **index.md** — Project index (paths and descriptions). Update when you add modules.
  - **system-environment.md** — Run environment for this project (regenerate via setup when moving to a new machine).

## Using this as a template

1. Copy this repo or clone and checkout the **template** branch.
2. Point an agent at **`agent/setup.md`** and say "set yourself up." It will regenerate `agent/system-environment.md` for your run environment and optionally update the index.
3. Use **`agent/new.md`** to create your first module and WIP doc.
4. For new chats, point the agent at **`agent/intro.md`** and your WIP doc path.

See **`agent/intro.md`** and **`agent/setup.md`** for full detail.
