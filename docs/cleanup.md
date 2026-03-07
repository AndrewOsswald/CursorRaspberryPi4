# cleanup.md — doc sync pass

When the user says to clean up according to this file, run through the steps below. This is a final pass to catch anything that wasn’t updated during the session. During normal work, the agent should already be updating docs as it goes (see intro); this file is for an explicit cleanup at the end.

---

## 1. Feature docs and active task files

- **Review all work done in this session** (code changes, wiring, new scripts, config, completed or in-progress steps).
- **Update the active feature doc(s)** (`docs/<feature-folder>/feature.md` and any deeper docs in that folder):
  - **Active state:** wiring, code paths, what’s working, what isn’t. Make sure it matches the current state of the feature.
  - **Overview / deeper docs:** If you added or changed functionality, wiring, or design, reflect it in the main feature doc or in linked docs.
- **Update the active task doc(s)** (`docs/<feature-folder>/task-<slug>.md`):
  - Move items between **Planned**, **In progress**, and **Completed** so they match what was actually done.
  - Add or fix references to code files, config, or other docs where useful.
- If more than one feature or task was touched, repeat for each relevant feature folder and task doc.

---

## 2. System environment and docs index

- **Review whether anything changed that affects the rest of the project:**
  - **Software installed or removed** (system packages, pip, tools like git/gh): update `docs/system-environment.md` (e.g. Software reference table, versions).
  - **Folder or file structure under `docs/`** (new feature folder, new doc, renamed or removed doc): update `docs/docs-index.md` (Core docs table if a new top-level doc was added, **Current structure** tree so it lists all existing `docs/` contents).
- **Apply those updates** so the env file and the index accurately describe the current system and doc layout.

---

## 3. Push to the task branch

- **Branch:** There is one branch per task. The active task doc should note its branch (e.g. **Branch:** `main--add-second-led`). Use that branch name. If missing, infer from the task doc filename: `task-<slug>.md` → branch `main--<slug>`.
- **Actions:** Ensure all doc and code changes are committed. Checkout that task’s branch if not already on it. Push to origin (e.g. `git push -u origin <branch>` if the branch isn’t set upstream yet, otherwise `git push`).
- If work touched more than one task, push the branch for the primary task the user cared about, or push each task branch that has new commits.

---

## 4. Done

- When steps 1–3 are done, documentation and the index/env are in sync and the task branch has been pushed. Confirm briefly to the user what you updated and that you pushed to the branch.
