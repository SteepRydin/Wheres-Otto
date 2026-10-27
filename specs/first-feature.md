# First feature — Collect the stage door key, unlock backstage, resume

Covers PT01 (resume), PT02, PT03, PT R1, PT R2, PT R3 and scenarios A1–A4 of `docs/product-brief.md`. The full story is in `docs/story.md` (Oslo Opera House horror).

## Why

As a player, I want to find the stage door key, use it to open the locked door backstage, and pick the game up again after closing it, so that my choices matter and I never lose progress.

## What

Story content for this feature (more scenes come in later features):

- Scenes: `foyer` (start), `box_office`, `backstage` (locked).
- Item: `stage_door_key`, found in the `box_office` drawer. Reusable, never consumed.
- Routes: `foyer` ↔ `box_office` are always open. `foyer` → `backstage` requires `stage_door_key`. `box_office` has no direct route to `backstage`.

Logic API (the tests are written against this; every function takes the path of the SQLite file):

- `logic.new_game(db_path)` → state; `logic.load_game(db_path)` → state, or `None` when no save exists.
- `logic.go_to(db_path, scene_id)` and `logic.take_item(db_path, item_id)` → `{"ok": bool, "message": str}`.
- `logic.takeable_items(db_path)` → ids of items that can still be taken in the current scene.
- A state is `{"scene": str, "inventory": list[str], "ending": None}`.

Checklist:

- [ ] A new game starts in `foyer` with an empty inventory.
- [ ] The current scene and its available actions are shown; every accepted action returns a visible message.
- [ ] In `box_office` the player can take the `stage_door_key` once. Afterwards the drawer offers no second key and the inventory holds exactly one (A3, R3).
- [ ] The key cannot be taken anywhere except the box office (R2).
- [ ] Without the key, going to `backstage` is rejected with an explanation; scene and inventory do not change (A1, R1).
- [ ] With the key, going to `backstage` works and the key stays in the inventory (A2).
- [ ] After every accepted action the state (scene, inventory) is saved in SQLite.
- [ ] After stopping and restarting the app, "Resume" restores scene and inventory, and the same routes are available (A4).
- [ ] A rejected action leaves the saved data unchanged.

## Out of scope

- Endings, the second item, the remembered decision (PT04, PT05, A5), the `stage` and `roof` scenes.
- "New game" confirmation and restart (PT01 restart, A6), next feature.
- Images, sound, a story editor.

## Done when

- The reviewed tests in `tests/` are green and were not weakened.
- In the running Streamlit app I can: try `backstage` without the key (rejected), take the key, take it again (still one), enter `backstage`, then stop the app, start it again and resume in the same place.
- The work is on a branch called `first-feature` and pushed.
