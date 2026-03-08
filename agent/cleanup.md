# cleanup.md — doc sync pass

**For agents:** When the user says "clean up according to cleanup.md", run steps 1–3 below. Goal: a new agent can pick up from intro + WIP doc + README with no missing context.

**Humans:** Ask the agent to "clean up according to cleanup.md" at end of session so docs are synced and pushed to the WIP branch.

---

## 1. Module docs and WIP files

- Review work done this session (code, config, wiring if applicable, completed steps).
- **context/current-state.md** — Update wiring, code, working, not working, next/refs to match the module. If the module's purpose, place in the project, or rules (best practices, what not to do) changed, update those sections too. This is the agent entry for the module.
- **Module README** (for humans): Update overview or how-to if functionality or steps changed. Do not duplicate current-state bullets in the README.
- **WIP doc(s):** Move items between **Planned**, **In progress**, **Completed** to match what was done. Add refs to code/config/docs where useful. Repeat for each module/WIP touched.

## 2. System environment and project index

- **`agent/system-environment.md`** — Update if software was installed/removed or run environment changed (versions, OS, hardware refs).
- **`agent/index.md`** — Update if folder or key files changed (new module, new context doc, renames). Add path + one-line description for any new file so the index stays useful for choosing what to read instead of scanning the tree.
- **README** (root or module) — Update if project scope, doc usage, or how to run changed.

## 3. Push to the WIP branch

- **Branch:** From WIP doc (**Branch:** `main--<slug>`) or infer `wip-<slug>.md` → `main--<slug>`.
- Commit uncommitted changes; checkout that branch if needed; push to origin. If multiple WIPs touched, push the primary WIP branch (or each with new commits).

## 4. Done

Docs and index/env are in sync; WIP branch pushed. Confirm briefly to the user what you updated and that you pushed.
