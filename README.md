# Raspberry Pi GPIO & hardware experiments

This project is for **experimenting with GPIO and interfacing with chips** on a Raspberry Pi (e.g. Pi 4). The repo includes a documentation system so you can track tasks and features, keep a hardware/software baseline, and work with agents in a consistent way.

The **`template` branch** holds the same doc system as a reusable template (minimal project-specific content). The **`main` branch** is this live experiment project.

## What’s in here

- **`docs/`** — The documentation system:
  - **intro.md** — Entry point for agents (and project overview for humans). Read order, context sources, rules, best practices.
  - **new.md** — How to start a new task or create a new feature. Branch naming, two workflows (new feature vs change existing feature).
  - **cleanup.md** — Final pass: sync feature/task docs, update env and index, push to the task branch.
  - **setup.md** — How the docs are set up and how to initialize a new project (e.g. regenerate system-environment after copying).
  - **docs-index.md** — Table of contents for the docs folder.
  - **system-environment.md** — Hardware/software baseline (machine-specific; regenerate via setup when moving to a new machine).
  - **template-new-feature/** — Example feature folder to copy when creating a new feature.

## Using the docs in this project

- **New chat:** Point the agent at `docs/intro.md` and the task doc you're working on (or at `docs/new.md` to start a new task/feature).
- **End of session:** Say e.g. "clean up according to cleanup.md" to sync docs and push to the task branch.
- **Doc map:** See `docs/docs-index.md` for a table of contents.

## Using this as a template for another project

1. **Copy the whole repo** (or at least the `docs/` folder and any config you want) into your new project—or use the **template** branch as the starting point.
2. **Point an agent at `docs/setup.md`** and say “set yourself up.” It will regenerate `docs/system-environment.md` for the new machine and optionally update the docs index.
3. **Start a chat** with intro + a task doc (or use `docs/new.md` to create one). Use `docs/cleanup.md` when you want a final sync and push.

For more detail, read `docs/intro.md` and `docs/setup.md`.
