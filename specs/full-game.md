# Full game — Last Curtain (masked horror at the Oslo Opera House)

Builds the complete first release of `docs/product-brief.md`. The first-feature slice (key, locked door, resume) is included and its tests stay as they are.

## Why

As a player, I want a short, spooky mystery in a masked, dark Oslo Opera House where what I carry and what I choose decides whether I escape, so that I can play it in ten minutes, leave midway, and come back to the same game.

## What

Content (`story.py`): six scenes, two reusable items, two endings, one remembered decision. Story in `docs/story.md`.

- Scenes: `foyer` (start), `box_office`, `backstage` (needs the key), `wardrobe`, `stage`, `roof` (ending scene).
- Items: `stage_door_key` (box office), `porcelain_mask` (wardrobe).
- Decision `singer` on the `stage`: `answer` or `silent`. Made once, remembered.
- Routes: `stage` → `roof` needs `singer = silent` **and** `porcelain_mask`; each missing condition has its own explanation.
- Endings: `escape` (reaching the roof) and `encore` (choosing `answer`).

Requirement checklist, each one covered by a test in `tests/` and by playing the running app:

- [x] PT01 Start and resume: new game; resume when a save exists; starting over asks for confirmation.
- [x] PT02 Explore: current scene and its actions are shown; every accepted action gives a visible result.
- [x] PT03 Collect and use: inventory can be inspected; the key unlocks backstage and the mask unlocks the roof; no duplicates.
- [x] PT04 Consequences: the `singer` decision changes what is possible and decides the ending; blocked actions are explained.
- [x] PT05 Finish and replay: each ending is identified; after an ending story actions stop; the outcome can be reviewed or a new game started.
- [x] R1 Blocked actions do not move the player or change the inventory.
- [x] R2 Items are collected only where available, once per game, reusable.
- [x] R3 Revisited scenes reflect remembered changes (empty drawer, blank mannequin).
- [x] R4 A new game resets progress but keeps the story; both endings are reachable from a new game.
- [x] A1–A6 acceptance scenarios, in tests and by hand.
- [x] Save after every accepted action in SQLite; rejected actions leave the save untouched.

## Out of scope

Story editor, extra mysteries, images and sound, multiplayer, combat, live AI.

## Done when

- All tests in `tests/` are green and none were weakened.
- I play both endings in the running app, including stopping and restarting the server in the middle and resuming.
- The work is on a branch called `full-game` and pushed.
