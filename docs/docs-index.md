# docs-index.md — map of docs

**Humans:** Use this as a table of contents for the docs folder.

Use this when you need to find a specific doc or see the full layout. User references **intro.md** first when starting a chat.

**Core docs**

| Path | Purpose |
|------|--------|
| docs/intro.md | Where to get context (task doc, feature doc, system-environment), how to read feature docs, keeping docs in sync, rules, best practices. Read first (user references it). For new task/feature see new.md. |
| docs/new.md | Start a new task or create a new feature. Layout (feature folders, task format), create new feature folder, add new task to existing feature. Multiple tasks per feature allowed. Reference when user says to start a new task or create a new feature. |
| docs/system-environment.md | Hardware, Pi 4, OS, pinout, 3.3V constraints, config path, GPIO/I2C/SPI/UART. Use when task involves hardware or host. |
| docs/cleanup.md | Final doc-sync pass: review work done, update feature and task docs, update env and index if software or folder structure changed. Reference when user says e.g. "clean up according to cleanup.md". |
| docs/setup.md | How the doc system is set up and how to initialize a new project. Regenerate system-environment.md for this machine; optionally update docs-index. Reference when user says e.g. "set yourself up" after copying docs to a new project. |
| docs/docs-index.md | This file. Map of docs. |

**Feature folders:** One folder per feature under `docs/`. Each has a **main** doc `feature.md` (outlines the feature in full, active state; references other docs for deeper detail—read those only when needed). Folder can contain other feature docs and one or more `task-<slug>.md` (multiple tasks per feature allowed). Read `feature.md` first. Current task = path from user or search `docs/**/task-*.md`. To create a new feature or task: `docs/new.md`. Template: `docs/template-new-feature/`.

**Current structure**

```
docs/
  intro.md
  new.md
  docs-index.md
  system-environment.md
  cleanup.md
  setup.md
  template-new-feature/
    feature.md
    task-gpio-led-blink.md
  gpio-led-blink/
    feature.md
    task-gpio-led-blink.md
  sx1262-ping-test/
    feature.md
    task-sx1262-ping-test.md
    wio-sx1262-module.md
    wiring.md
    SPI_TEST_EXPLAINED.md
    PING_TEST_SUMMARY.md
```

(Feature folders added under `docs/` as needed; user gives task doc path when starting a chat.)
