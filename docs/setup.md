# setup.md — how the docs work and how to initialize a new project

**Humans:** After copying this docs folder to a new project, tell the agent to read this file and set itself up; it will regenerate system-environment for the new machine.

Use this file when you’ve copied this `docs/` folder into a **new project** and the user says to set yourself up (e.g. “read setup.md and set yourself up”). It explains how the documentation is organized and what you need to do so the project is ready.

---

## How the documentation is set up

- **intro.md** — First thing to read in a new chat (user points you here). Gives read order (task doc → feature doc → system-environment if hardware), context sources, how to read feature docs, keeping docs in sync, paths, rules, best practices. One branch per task; cleanup pushes to it.
- **new.md** — When the user wants to start a new task or create a new feature. Defines what a task is, feature folders, task doc format, branch naming (`main--<task-slug>`), and two workflows: create a new feature (new folder) or add a new task to an existing feature.
- **cleanup.md** — When the user says to clean up (e.g. “clean up according to cleanup.md”). Final pass: update feature and task docs, update env and index if needed, push to the task’s branch.
- **system-environment.md** — Hardware and software baseline for **this** machine: constraints, config path, pinout, GPIO/I2C/SPI/UART, hardware and software reference tables. **This file is machine- and project-specific**; it was generated for another environment. In a new project you must regenerate it (see below).
- **docs-index.md** — Map of all docs and current folder structure. Update it if you add or remove top-level docs (e.g. after adding this setup.md).
- **template-new-feature/** — Template folder and files to copy when creating a new feature. Leave as-is.
- **Feature folders** — Created under `docs/` when you start features (see new.md). Each has `feature.md` and one or more `task-<slug>.md`. None exist until you create them.

Intro, new, cleanup, and the template are **generic**. Only **system-environment.md** (and optionally docs-index) must be updated when you initialize a new project.

---

## What to do when initializing a new project

You’ve copied this docs folder into a new project folder. To set yourself up:

### 1. Regenerate `docs/system-environment.md`

That file currently describes a different machine. Regenerate it for **this** machine:

1. **Read the current `docs/system-environment.md`** to see its structure: sections (Critical constraints, Config path, Pinout, GPIO and interfaces, Hardware reference, Software reference), table formats, and the best-practices paragraph. Keep the same structure and formatting; only the **values** will change.
2. **Run system commands** to gather this machine’s data. If a command isn’t available (e.g. `vcgencmd` on non-Pi), skip it and omit or adapt that section in the output. Examples of what you need (adjust for OS/hardware):
   - **OS:** `cat /etc/os-release` (or equivalent)
   - **Kernel:** `uname -a`, `cat /proc/version`
   - **CPU / board:** `cat /proc/cpuinfo` (model, revision, serial if Pi), `cat /proc/device-tree/model` if present
   - **Memory:** `free -h`, `cat /proc/meminfo` (head)
   - **Storage:** `df -h /`, `lsblk`
   - **Firmware/config (Raspberry Pi):** `vcgencmd get_throttled`, `vcgencmd measure_temp`, `vcgencmd get_config int` (and config path: `/boot/firmware/config.txt` on Pi OS / Debian)
   - **GPIO / interfaces:** `ls -la /sys/class/gpio/`, `ls /dev/gpio* /dev/i2c* /dev/spi* /dev/tty*`, `lsmod | grep -E 'i2c|spi|gpio'`
   - **User / permissions:** `whoami`, `id`, `hostname`
   - **Python:** `python3 --version`, `which python3`, and any gpiozero/lgpio or similar packages
   - **Git:** `git --version`, optionally `gh --version`
3. **Rewrite `docs/system-environment.md`** with the new data. Keep: the opening line (when to use the file), Critical constraints and best practices (edit only if this machine has different constraints, e.g. different Pi or non-Pi), Config path (adjust if different), Pinout table (update if different board; Pi 4 40-pin is in the current template), GPIO and interfaces bullets, Hardware reference table, Software reference table. Remove or adapt sections that don’t apply (e.g. no vcgencmd on non-Pi).

If this is not a Raspberry Pi, adjust constraints and pinout accordingly (or drop pinout and keep only what applies).

### 2. Update `docs/docs-index.md` if needed

If you added or removed any top-level doc (for example, this setup.md), update the **Core docs** table and the **Current structure** tree in `docs/docs-index.md` so they list the actual files. After copying, you may have added `setup.md`; add it to the index.

### 3. You’re done

- **Don’t** change intro.md, new.md, cleanup.md, or the template unless the new project has different rules.
- The user can now start a chat with intro + a task doc, or use new.md to start a task/feature, or cleanup.md to clean up. system-environment.md now correctly describes this project’s machine.
