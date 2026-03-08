# setup.md — initialize a new project

**For agents:** Use when the user says to set yourself up after copying `agent/` into a new project. Main action: regenerate **`agent/system-environment.md`** for this run environment (e.g. laptop, server, container, or embedded host). Optionally update **`agent/index.md`**.

**Humans:** After copying the agent folder to a new project, tell the agent to read setup.md and set itself up.

---

## How the documentation is set up

- **intro.md** — First thing to read in a new chat (user points you here). Gives read order (WIP doc → module current-state → system-environment when relevant), context sources, how to read module docs, keeping docs in sync, paths, rules. Rules and best practices are in each module's context/current-state.md. One branch per WIP; cleanup pushes to it.
- **new.md** — When the user wants to start a new WIP or create a new module. Defines what a WIP is, module layout (one folder per module, each with README + context/), WIP doc format, branch naming (`main--<wip-slug>`), and two workflows: create a new module (new folder) or add a new WIP to an existing module.
- **cleanup.md** — When the user says to clean up (e.g. "clean up according to cleanup.md"). Final pass: update module README and WIP doc, update env and index if needed, push to the WIP's branch.
- **system-environment.md** — Run environment for **this** project (e.g. laptop, server, container, embedded host): OS, interfaces when applicable, config path, reference tables. **Regenerated per machine or run target**; in a new project you must regenerate it (see below).
- **index.md** — Paths and one-line descriptions of what's in each doc (agent docs + each module's README and context files). Agents use it to choose what to read without opening the file tree. Update it when you add/remove docs or modules so the descriptions stay accurate.
- **Module folders** — Created at repo root when you start modules (see new.md). Each has a README and a context/ subfolder. New-module structure is described in new.md; there is no separate template folder. There is no module-specific context stored inside agent/.

Intro, new, and cleanup are **generic**. Only **system-environment.md** (and optionally index.md) must be updated when you initialize a new project.

---

## What to do when initializing a new project

You've copied this agent folder into a new project folder. To set yourself up:

### 1. Regenerate `agent/system-environment.md`

That file currently describes a different machine. Regenerate it for **this** machine:

1. **Read the current `agent/system-environment.md`** to see its structure: when to use; constraints (if any); config path; pinout or interfaces (if applicable); hardware/software reference tables. Keep the same structure and formatting; only the **values** will change.
2. **Run system commands** to gather this run environment's data. If a command isn't available on this platform (e.g. `vcgencmd` only on Raspberry Pi), skip it and omit or adapt that section. Examples (adjust for OS and target—Linux server, macOS, Docker, embedded):
   - **OS:** `cat /etc/os-release` (or equivalent)
   - **Kernel:** `uname -a`, `cat /proc/version`
   - **CPU / board:** `cat /proc/cpuinfo` (model, revision; on embedded, device-tree model if present)
   - **Memory:** `free -h`, `cat /proc/meminfo` (head)
   - **Storage:** `df -h /`, `lsblk`
   - **Firmware/config (if applicable):** e.g. on Raspberry Pi: `vcgencmd` and `/boot/firmware/config.txt`; on other platforms use the relevant config path
   - **Interfaces (if applicable):** e.g. `ls /dev/` for serial, GPIO, I2C, SPI; `lsmod` for loaded modules; omit on pure software targets
   - **User / permissions:** `whoami`, `id`, `hostname`
   - **Runtimes:** `python3 --version`, `node --version`, or whatever the project uses
   - **Git:** `git --version`, optionally `gh --version`
3. **Rewrite `agent/system-environment.md`** with the new data. Keep the same structure; fill in values for **this** run environment. Remove or adapt sections that don't apply (e.g. no pinout on a pure server; no platform-specific commands on a different OS).

### 2. Update `agent/index.md` if needed

If you added or removed docs or module folders, add or remove rows in `agent/index.md` with path and a one-line description. The index is more useful than the raw file structure because descriptions let an agent decide what to open without reading multiple files first.

### 3. You're done

- **Don't** change intro.md, new.md, cleanup.md, or the template unless the new project has different rules.
- The user can now start a chat with intro + a WIP doc, or use new.md to start a WIP/module, or cleanup.md to clean up. system-environment.md now correctly describes this project's machine.
