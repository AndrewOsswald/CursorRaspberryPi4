# new.md — start a new task or create a new feature

**Humans:** When you want to start a new task or feature, point an agent at intro and this file (e.g. “read intro and new.md, then create a new feature for X”).

When the user asks you to start a new task or create a new feature, follow this file. For general context (where to get task/feature state, how to read docs), see `docs/intro.md`.

---

## What is a task?

A **task** is a unit of work tracked in a task doc (Planned / In progress / Completed). Two common kinds of tasks:

- **Creating a new feature** — the task is to bring a new feature into the project (new folder, feature doc, first task doc, branch). Use the workflow below for a **new feature (new folder)**.
- **Making a change to a feature** — the task is to change or extend an existing feature (e.g. add a second LED, add CLI args). Use the workflow below for a **new task (existing feature)**.

Both are tasks; the difference is whether the feature already exists. Pick the workflow that matches.

---

## Documentation layout: feature folders

- **One folder per feature** (e.g. `docs/gpio-led-blink/`). That folder can hold **multiple docs** about the feature; one is the **main feature doc** that agents read first. It can also hold **multiple task docs** (one or more `task-<slug>.md`). There may be multiple in-progress tasks for a single feature; the user will try to avoid that, but it is allowed.
- **Main feature doc** (`feature.md` in the folder): Outlines the feature in full (overview, active state: wiring, code, what works) and **references other docs in the folder** for deeper explanations. Update it as the feature changes.
- **Other feature docs** (any other .md in the folder except task docs): Deeper dives (e.g. wiring diagram, protocol details, design notes). The main feature doc links to them.
- **Task doc(s)** (`task-<slug>.md` in the same folder): Each tracks progress for one task on that feature (Planned / In progress / Completed). A feature folder can contain more than one task doc. Each task doc should reference the main feature doc for feature details and active state.
- **Audience:** All docs inside a feature folder are written for **both humans and AI**. When you create or edit them, optimize for both: clear structure and headings for parsing, explicit file paths and state for context, readable prose and examples for humans.
- **Template to copy:** `docs/template-new-feature/` (contains `feature.md` and `task-gpio-led-blink.md`). Copy the whole folder when starting a **new feature**; rename folder and files to match. When adding only a **new task** to an existing feature, add a new `task-<slug>.md` in that feature folder (see below).

---

## Task doc format

- **Sections (exactly three):** **Planned** (not started), **In progress** (current work), **Completed** (done; add file paths when useful). Respect when reading or updating.
- **Path:** `docs/<feature-folder>/task-<slug>.md`. Slug: short, lowercase, hyphenated (e.g. `gpio-led-blink`, `add-second-led`). Task doc lives in the same folder as `feature.md` for that feature. Multiple task docs in one folder are allowed.
- Task docs may reference the feature doc and other files (code, config, other markdown); follow those references.

---

## Branch naming: one branch per task

- **One branch per task, not per feature.** Every task gets its own branch. Multiple tasks on the same feature = multiple branches.
- **Convention:** `main--<task-slug>`. The task slug is the slug of that task’s doc (e.g. `task-gpio-led-blink.md` → branch `main--gpio-led-blink`; `task-add-second-led.md` → branch `main--add-second-led`). Branch is created off `main`.
- **Note the branch in the task doc** (e.g. at the top: **Branch:** `main--<task-slug>`). Cleanup pushes to the branch named in the active task doc.

---

## Task: create a new feature (new folder)

When the task is to **create a new feature** (feature doesn’t exist yet):

1. Create feature folder `docs/<feature-folder>/` (name from feature, e.g. `docs/gpio-led-blink/`). Copy structure from `docs/template-new-feature/`.
2. Create `docs/<feature-folder>/feature.md` as the **main** feature doc: outline the feature in full (overview, Active state), and add a section that references other docs in the folder for deeper detail (create those other docs when needed). Write for both humans and AI (clear structure, explicit paths/state, readable prose). Use `docs/template-new-feature/feature.md` as reference.
3. Create `docs/<feature-folder>/task-<slug>.md` with exactly three level-2 headers: `## Planned`, `## In progress`, `## Completed`. Add a line at the top that the feature doc in this folder holds feature details and active state. Copy structure from `docs/template-new-feature/task-gpio-led-blink.md` or use minimal content.
4. Update `docs/docs-index.md` **Current structure** if needed so the new folder is listed.
5. **Create the task branch:** Checkout `main`, pull from remote so main is up to date (e.g. `git checkout main`, `git pull origin main`), then create and checkout branch `main--<task-slug>` — use the slug of the task doc you created (for this first task it’s usually the same as the feature folder name, e.g. `main--gpio-led-blink`). **Note the branch in the task doc** (e.g. at the top: **Branch:** `main--<task-slug>`).

---

## Task: change an existing feature (new task doc)

When the task is to **make a change to an existing feature** (folder and feature.md already exist; add a new task doc for this work):

1. Create `docs/<feature-folder>/task-<slug>.md` in that feature folder. Use a new slug for this task (e.g. existing `task-gpio-led-blink.md`, new task `task-add-second-led.md` → slug `add-second-led`).
2. Use exactly three level-2 headers: `## Planned`, `## In progress`, `## Completed`. Add at the top: feature doc in this folder holds feature details and active state, and **Branch:** `main--<task-slug>` (e.g. `main--add-second-led`). Copy structure from `docs/template-new-feature/task-gpio-led-blink.md` or use minimal content. Fill **Planned** with the user’s goals or steps for this task.
3. **Create the task branch:** Checkout `main`, pull from remote so main is up to date (e.g. `git checkout main`, `git pull origin main`), then create and checkout branch `main--<task-slug>` (e.g. `main--add-second-led`). This task gets its own branch; do not reuse another task’s branch.
4. Optionally add a reference to the new task doc from the main feature doc (e.g. under "Related task doc(s)") so it’s discoverable.

---

## After creating

- Update the task doc as work moves (Planned → In progress → Completed). Update the feature doc when the feature's state changes (wiring, code, working/not working). See `docs/intro.md` (Keeping docs in sync) and `docs/cleanup.md` for final pass.
