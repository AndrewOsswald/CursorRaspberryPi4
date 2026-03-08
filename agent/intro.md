# intro.md — agent context

**For agents:** You have no prior context. Read this file first, then the WIP doc path the user gives. The WIP doc lists read order (README, system-environment if needed, other context). Follow that order. **`agent/index.md`** lists every doc with a short description of what's in it—use it to choose what to read instead of opening the file structure to guess (saves steps and tokens).

**Humans:** Give agents this intro and a WIP doc path so they can load context efficiently.

---

## Context sources (where to get what)

| Need | Source |
|------|--------|
| WIP state (Planned / In progress / Completed) | WIP doc. User gives path or "the WIP doc"; search `**/context/wip-*.md` if needed. Do not assume; read the doc. |
| Module intro, rules, and state (for agents) | **`context/current-state.md`** in the module folder. Start here for this module: what the code is and does, how it fits in the project, rules (best practices, what not to do), then wiring/code/working/not/next. You don't need the whole-project description—just this file for this module. |
| Module overview, how to run (for humans) | **README** in the module folder. Human-oriented; open for narrative and run steps when needed. |
| Execution environment (OS, hardware, config, interfaces) | **`agent/system-environment.md`** when the WIP involves host or run environment. Module README may also specify (e.g. "runs in Docker", env vars). Do not guess. |
| List of docs and what's in each | **`agent/index.md`**. Path + one-line description per file so you can pick what to read without opening files to peek. |
| Start new WIP or create new module | **`agent/new.md`**. One branch per WIP (`main--<wip-slug>`); cleanup pushes to that branch. |

## How to read module docs

- **This module (agents):** Read **`context/current-state.md`** first. It's the agent entry for this module: what the code is and does, how it fits in the project, rules for working here (best practices, what not to do), then wiring, code, working, not working, next/refs. You don't need the whole project—just this file for this module. Do not infer state from the WIP doc alone.
- **Overview and how to run:** **README** in the module folder is for humans; use it when you need narrative or run steps.
- **Open other `context/` files** (WIP doc, wiring, test-summary, API spec, config notes, etc.) as the WIP doc or task requires.

## Execution environment

**Where code runs is not assumed.** The project may target a laptop, a server, a container, or embedded hardware. The WIP doc and module current-state (and, when relevant, **`agent/system-environment.md`**) describe the run environment—what host or container, what config or interfaces are available. Read those; do not assume a specific OS or environment.

## Paths

- **Repo root** = project root.
- **`agent/`** — Shared agent docs only: intro.md, new.md, index.md, system-environment.md, cleanup.md, setup.md. No module-specific content. **index.md** = paths + descriptions of what's in each file (use it instead of scanning the tree to decide what to open).
- **Modules** — One folder per module at repo root (e.g. `my-service/`, `cli-tool/`). Each has README, **context/** (WIP docs, notes), and code. New-module layout: **`agent/new.md`**.
- **New project init:** **`agent/setup.md`**.

## Rules

- WIP state only from the WIP doc. Run environment (OS, hardware, config) only from system-environment or the module. Do not guess.
- Work on the WIP's branch: **Branch:** `main--<wip-slug>` in the WIP doc; commits and cleanup push to that branch.

## Keeping docs in sync

- **As you work:** Update **context/current-state.md** and WIP doc (Planned / In progress / Completed); update README when overview or how-to changes. If you change agent/ or context/ layout or install/remove software, update **`agent/system-environment.md`** or **`agent/index.md`**.
- **Final pass:** User says "clean up according to cleanup.md" → follow **`agent/cleanup.md`** (sync docs, push to WIP branch).

## Best practices

**Per-module:** Each module's **context/current-state.md** states rules and best practices for that module. **Run environment:** **`agent/system-environment.md`** when the WIP involves host, hardware, or config.
