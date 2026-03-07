# intro.md — agent context

You have no prior context. **Read in order:** (1) task doc — path from user or search `docs/**/task-*.md`; (2) feature doc in that folder — `docs/<feature-folder>/feature.md`; (3) if the task involves hardware/GPIO/pins/host — `docs/system-environment.md`. To find any doc: `docs/docs-index.md`.

## Context sources

- **Current task state (planned / in progress / completed):** Task doc. User will give path or say "the task doc"; search `docs/**/task-*.md` if needed. Do not assume state; read the doc.
- **Feature description and active state:** Main feature doc in the same folder as the task doc: `docs/<feature-folder>/feature.md`. It outlines the feature in full and references other docs in that folder for deeper explanations. Read the main doc first to keep context low; follow references to other docs only when you need more detail. Task doc(s) in that folder reference it.
- **Hardware, pinout, 3.3V, OS, tools:** `docs/system-environment.md`. Do not guess.
- **List of all docs:** `docs/docs-index.md`.
- **Starting a new task or creating a new feature:** See **`docs/new.md`** (layout, task format, create feature folder, add task to existing feature). Multiple task docs per feature allowed. Each task has its own branch (`main--<task-slug>`, noted in the task doc); cleanup pushes to that branch.

## How to read feature folder docs

- **Start with the main feature doc** (`feature.md` in that folder). It outlines the feature in full (overview, active state). Do not skip it; do not assume state or wiring from the task doc alone.
- **Follow references to other docs in the folder only when you need deeper detail** (e.g. wiring diagram, protocol spec). This keeps required context low; read those linked docs when the task or the user’s question requires it.
- **Do not expect feature docs to tell you how to read them.** Reading order and when to follow links are defined here (intro); the feature docs themselves contain only feature content.

## Keeping docs in sync

- **As you work,** try to update feature docs and task docs at each step: when you change wiring, code, or complete a step, update the relevant feature doc (active state) and task doc (Planned / In progress / Completed) so they stay accurate. When you install or remove software or change the layout under `docs/`, update `docs/system-environment.md` or `docs/docs-index.md` as needed.
- **Final pass:** When the user asks you to clean up (e.g. "clean up according to cleanup.md"), follow **`docs/cleanup.md`**: review work done, update feature and task docs, update env and index if needed, then push to the task’s branch.

## Paths

- Repo root = project root.
- `docs/` contains: intro.md, new.md, docs-index.md, system-environment.md, cleanup.md, setup.md, template-new-feature/ (feature.md + task-gpio-led-blink.md), and one folder per feature (each with feature.md as the main outline and zero or more other docs for deeper detail, plus one or more task-<slug>.md). Code/config paths come from the task doc or feature doc or repo. For creating a new feature or task, see `docs/new.md`. For initializing a new project after copying this docs folder, see `docs/setup.md`.

## Rules

- Get current task state only from the task doc. Get hardware/pinout/environment only from system-environment.md. Do not guess.
- When working on a task, work on that task’s branch: checkout the branch noted in the task doc (**Branch:** `main--<task-slug>`) so commits land on the right branch before cleanup pushes.

## Best practices

- **Wiring:** When you ask the user to set up or change wiring, give a detailed explanation of the process: what to connect where (pin numbers, names), in what order if it matters (e.g. power off first, connect GND before signal), and what each wire does. Do not assume prior experience; spell out the steps.
- **Safety:** Always warn the user about any unsafe behaviors that are possible in the steps you suggest (e.g. risk of short circuits, connecting 5 V to a GPIO, hot-plugging, reversing polarity, exceeding current limits). State the risk and how to avoid it. Refer to `docs/system-environment.md` for hardware constraints when giving wiring or hardware instructions.

