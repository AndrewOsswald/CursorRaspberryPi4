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

## Modules

*(Template branch: no modules yet. When you create modules with `agent/new.md`, add each module and its key files here with a one-line description.)*

Modules live at repo root. Each has a **README** (for humans), **context/** (current-state.md, WIP docs, notes), and code. Add a row per key file so agents can choose what to read.
