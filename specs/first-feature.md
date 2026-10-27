# First feature — Collect a key, unlock a route, resume

Covers PT01 (resume), PT02, PT03, PT R1, PT R2, PT R3 and scenarios A1–A4 of `docs/product-brief.md`.

## Why

As a player, I want to find a key, use it to open a locked door, and pick the game up again after closing it, so that my choices matter and I never lose progress.

## What

Story content for this feature (more scenes come in later features):

- Scenes: `foyer` (start), `library`, `study` (locked).
- Item: `brass_key`, found in the `library` drawer. Reusable, never consumed.
- Route: `foyer` → `study` requires `brass_key`.

Checklist:

- [ ] A new game starts in `foyer` with an empty inventory.
- [ ] The current scene and its available actions are shown; every accepted action shows a visible result.
- [ ] In `library` the player can take the `brass_key` once. Afterwards the drawer offers no second key and the inventory holds exactly one `brass_key` (A3, R3).
- [ ] Without the key, going to `study` is rejected with an explanation; the scene and inventory do not change (A1, R1).
- [ ] With the key, going to `study` works and the key stays in the inventory (A2).
- [ ] After every accepted action the game state (current scene, inventory) is saved in SQLite.
- [ ] After stopping and restarting the app, "Resume" restores the scene and inventory, and the same routes are available (A4).
- [ ] A rejected action leaves the saved data unchanged.

## Out of scope

- Endings, the second item, the remembered decision (PT04, PT05, A5).
- "New game" confirmation and restart (PT01 restart, A6) — next feature.
- Images, sound, a story editor.

## Done when

- The reviewed tests in `tests/` are green and were not weakened.
- In the running Streamlit app I can: try `study` without the key (rejected), take the key, take it again (still one), enter `study`, then stop the app, start it again and resume in the same place.
- The work is on a branch called `first-feature` and pushed.
