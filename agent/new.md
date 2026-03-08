# new.md — start a new WIP or create a new module

**For agents:** Use when the user asks to start a new WIP or create a new module. Follow the workflow that matches (new module = new folder; change to existing module = new WIP doc). General context: `agent/intro.md`.

**Humans:** Point an agent at intro and this file (e.g. "read intro and new.md, then create a new module for X").

---

## What is a WIP?

A **WIP** (work in progress) is a unit of work tracked in a WIP doc (Planned / In progress / Completed). Two common kinds of WIPs:

- **Creating a new module** — the WIP is to bring a new module into the project (new folder, README, context folder, first WIP doc, branch). Use the workflow below for a **new module (new folder)**.
- **Making a change to a module** — the WIP is to change or extend an existing module (e.g. add a feature, add CLI args, add an API endpoint). Use the workflow below for a **new WIP (existing module)**.

Both are WIPs; the difference is whether the module already exists. Pick the workflow that matches.

---

## Documentation layout: one folder per module

- **Every module has its own folder** at repo root (e.g. `my-service/`, `cli-tool/`, `hardware-test/`). There is **no** module-specific context stored inside `agent/`; all module context lives in that module's folder.
- Each module folder contains: **README.md** (main module doc), **context/** (WIP docs and other context), and the **code** for that module (scripts, drivers, etc.).
- **Audience:** All docs are written for **both humans and AI**. Use clear structure and headings for parsing, explicit file paths and state for context, and readable prose for humans.

---

## Module format (detailed)

This format ensures that when the user gives an agent **intro + WIP doc path**, the agent has a clear handoff: intro explains the system, the WIP doc points to the README and lists exactly what else to read so a fresh agent can continue with full context. A project may have a single module or many; the format is the same.

### Folder layout

```
<module-folder>/           e.g. my-feature/, api-server/, or cli-tool/
  README.md                main module doc (project, best practices, overview, current state, how to run, refs)
  context/
    current-state.md      agent entry for this module: intro, how it fits, rules, then state (wiring, code, working, not, next/refs)
    wip-<slug>.md         one file per WIP (planned / in progress / completed; "For a fresh agent" handoff)
    (optional: wiring.md, test-summary.md, datasheet-notes.md, etc.)
  (code: .py, config, etc.)
```

**context/current-state.md** — For agents. **Start here for this module**; an agent doesn't need the whole-project description, just this module. This file is the first place the agent learns what the code is and does. Sections (in order):

1. **Opening** — One line: this file is the agent entry for this module; read it first for this part of the project.
2. **What this module is** — Broad introduction to this part of the project: what the code is, what it does, what it's for. Module can be anything (hardware test, CLI, service, library); describe it so a fresh agent understands scope and purpose.
3. **How it fits in the project** — One or two sentences: how this module relates to the rest of the repo (e.g. "This repo may have one or several modules; this one is the minimal example" or "One of several modules; others might be different services, CLIs, or boards"). No need to describe the whole project—just enough context so the agent knows where this module sits.
4. **Rules for working on this module** — Coding best practices, what not to do, module-specific discipline. Examples (adapt to the module): spell out steps and don't assume experience; follow existing code style and conventions; respect env vars or config; for hardware modules: wiring, safety, one process per pin or BUSY/NSS discipline, refer to `agent/system-environment.md` for constraints; for services: port, logging, graceful shutdown. List what an agent must follow when editing or suggesting code.
5. **Wiring** — What's connected (or ref to wiring.md). Use only if the module has hardware; for software modules, replace with **Config / env** (how to configure, required env vars, config file paths) or omit.
6. **Code** — Paths and one-line each. Update as files change.
7. **Working** — What passes or is done. Update as tests or features land.
8. **Not working / limitations** — What's broken or not yet done.
9. **Next / refs** — Pointers to WIP doc, test-summary, datasheet notes, system-environment, etc.

Keep this file updated as the module changes. Humans get overview and how-to from the README; agents get intro, rules, and state from this file.

**Context note files** (wiring, test-summary, API spec, config notes, etc.): For human and agent scanning, start each with a one-line **Contains:** or **When to read:** that says what's inside (e.g. "**Contains:** Connection table and safety notes." or "**Contains:** API endpoints and request format."). Then the index and the file itself both tell the reader whether to open it without reading the whole doc.

- **Slug:** Short, lowercase, hyphenated (e.g. `my-feature`, `add-api-endpoint`). Use the same slug in the WIP filename and the branch: `wip-my-feature.md` → branch `main--my-feature`.

### README.md — for humans

The README is the main entry for **human** readers: what the module is, how to run it (and how to wire or configure it if applicable), and where to find more. Write it in clear prose. **Current state for agents** lives in **`context/current-state.md`** (structured for agents); the README does not duplicate that. Sections (in order):

1. **Title** — `# Module: <name>` (or a short human-friendly title).
2. **## Project** — What kind of project this is and what this module does. One or two sentences.
3. **## Best practices** — What applies when working on this module (run steps, safety if applicable, code/style discipline). Refer to `agent/system-environment.md` when the WIP involves host or hardware.
4. **## Overview** — What the module does (narrative or bullets).
5. **How to run** (and **how to wire** or **how to configure** if applicable) — Step-by-step for humans: what you need, run commands, config or wiring order. Can be one section or several.
6. **## Deeper docs (in context/)** — List context files (include `context/current-state.md` — "Current state (for agents)") and other notes. One line each.
7. **## Related WIP doc(s)** — `context/wip-<slug>.md` — brief label.

Optional: a short "Main scripts" or "Files" list if it helps humans find the code. Do not put a long agent-style "Current state" section in the README; that belongs in **context/current-state.md**.

### context/wip-<slug>.md — sections

1. **Title and opening block**
   - `# WIP: <description>`
   - **Module details and current state:** See **`context/current-state.md`** in this folder (wiring, code, what works, what doesn't). README in parent folder is for humans (overview, how to run).
   - **Branch:** `main--<wip-slug>`. One branch per WIP; cleanup pushes to this branch.
   - **Run environment:** `agent/system-environment.md` (when the WIP involves host or hardware; omit if not).
   - **For a fresh agent:** Exact read order so a new agent has full context. Example: "Read `agent/intro.md`, then this WIP doc and **`context/current-state.md`** (and `../README.md` for overview/run if needed). For run environment (e.g. wiring, pins, env vars), read `agent/system-environment.md` when relevant. That set gives you the context needed to continue." For a complex WIP, add a **## Context for next session** section below with what's done, current failure, and what to try next; the "For a fresh agent" line can then say "… then this WIP doc and `../README.md`, then <list of context files>. See **Context for next session** below."

2. **## Planned** — Not yet started. Bullet list.

3. **## In progress** — Current work. Move items here when you start; move to Completed when done.

4. **## Completed** — Done. Add file paths or short notes when useful. Append new items as work completes.

Optional for complex WIPs: **## Context for next session** — Summary for handoff (what's done, what failed, what to try next, key refs). Keeps the WIP doc self-contained for a fresh chat.

### Handoff in practice

- User tells the agent: "Read intro and the WIP doc" (and gives the path to the WIP doc, e.g. `sx1262_gpio_test/context/wip-sx1262-ping-test.md`).
- Agent reads intro → learns the system and that it has no prior context.
- Agent reads the WIP doc → gets branch, state (Planned / In progress / Completed), and the **For a fresh agent** line (and **Context for next session** if present).
- Agent follows that read order (current-state, README if needed, then any listed context files, and system-environment when the WIP involves run environment) → has module intro, rules, current state, and what to do next.

---

## New module template (structure)

When starting a **new module**, create a folder at repo root and use the format above. You can copy from an existing module (e.g. `gpio-led-blink/`) and rename. Checklist:

**context/current-state.md:** Opening (agent entry for this module) → What this module is → How it fits in the project → Rules for working on this module → Wiring or Config/env (if applicable) → Code → Working → Not working / limitations → Next / refs. Agent-only; update as module changes.

**README.md:** For humans. Title → ## Project → ## Best practices → ## Overview → how to run (and wire/config if applicable) → ## Deeper docs (in context/) (include current-state.md) → ## Related WIP doc(s).

**context/wip-<slug>.md:** Opening block (Module details, Branch, Run environment if needed, **For a fresh agent:** read order) → ## Planned → ## In progress → ## Completed.

When adding only a **new WIP** to an existing module (module folder and README already exist), add a new **context/wip-<slug>.md** with the same WIP doc structure; add a line under **Related WIP doc(s)** in the README so the new WIP is discoverable.

---

## WIP doc format

- **Sections (exactly three):** **Planned** (not started), **In progress** (current work), **Completed** (done; add file paths when useful). Respect when reading or updating.
- **Path:** `<module-folder>/context/wip-<slug>.md`. Slug: short, lowercase, hyphenated (e.g. `my-feature`, `add-api-endpoint`). Multiple WIP docs in one module are allowed.
- WIP docs may reference the README and other files (code, config, other markdown); follow those references.

---

## Branch naming: one branch per WIP

- **One branch per WIP, not per module.** Every WIP gets its own branch. Multiple WIPs on the same module = multiple branches.
- **Convention:** `main--<wip-slug>`. The WIP slug is the slug of that WIP's doc (e.g. `wip-my-feature.md` → branch `main--my-feature`; `wip-add-config.md` → branch `main--add-config`). Branch is created off `main`.
- **Note the branch in the WIP doc** (e.g. at the top: **Branch:** `main--<wip-slug>`). Cleanup pushes to the branch named in the active WIP doc.

---

## WIP: create a new module (new folder)

When the WIP is to **create a new module** (module doesn't exist yet), follow the **Module format (detailed)** and **New module template (structure)** above. Concretely:

1. **Choose a slug** — Short, lowercase, hyphenated (e.g. `my-feature`, `api-server`). The WIP file will be `wip-<slug>.md` and the branch `main--<slug>`.

2. **Create the module folder** at repo root (e.g. `my_feature/`). Optionally copy an existing module folder and rename it and its contents.

3. **Write README.md** — For humans. Title; ## Project; ## Best practices; ## Overview; how to wire/run; ## Deeper docs (in context/) including current-state.md; ## Related WIP doc(s). No "Current state" section in README; that goes in context/current-state.md.

4. **Create context/** — **context/current-state.md** (full structure: What this module is, How it fits, Rules, then Wiring or Config/env if applicable, Code, Working, Not working, Next/refs). **context/wip-<slug>.md**: title; **Module details and current state:** See `context/current-state.md`; **Branch:** `main--<slug>`; **Run environment:** `agent/system-environment.md` when the WIP involves host or hardware; **For a fresh agent:** read order (intro → this WIP doc → current-state.md, README if needed, system-environment when relevant). Then ## Planned, ## In progress, ## Completed.

5. **Update agent/index.md** — Add the new module and each key file (README, WIP doc, any new context files) with a one-line description of what's in it. The index is useful because agents can choose what to read from descriptions instead of opening the file structure; keep it up to date when you add modules or context files.

6. **Create the WIP branch** — From repo root: `git checkout main`, `git pull` (if applicable), then `git checkout -b main--<slug>`. Ensure the WIP doc's **Branch:** line matches. Commits for this WIP go on this branch; cleanup pushes to it.

---

## WIP: change an existing module (new WIP doc)

When the WIP is to **make a change to an existing module** (add a new WIP doc for this work):

1. Create **<module-folder>/context/wip-<slug>.md** with a new slug. Use exactly three level-2 headers; add at the top: module details in parent README; **Branch:** `main--<wip-slug>`.
2. **Create the WIP branch:** Checkout `main`, pull, then create and checkout `main--<wip-slug>`. This WIP gets its own branch.
3. Optionally add a reference to the new WIP doc from the module README (e.g. under "Related WIP doc(s)") so it's discoverable.

---

## After creating

- Update the WIP doc as work moves (Planned → In progress → Completed). Update **context/current-state.md** when the module's state changes (wiring, config, code, working/not); update the README when overview or how-to steps change. See `agent/intro.md` (Keeping docs in sync) and `agent/cleanup.md` for final pass.
