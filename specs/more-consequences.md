# More consequences — you can lose, and choices decide how

Extends `specs/full-game.md`. All existing tests stay as written and stay green.

## Why

As a player, I want my choices to change what is possible and to be able to lose, so that the mystery feels dangerous and each playthrough can end differently.

## What

A second remembered decision, a third item and two losing endings.

- Decision `lights` (once, in the `foyer`): `on` (flood the house with light) or `off` (stay in the dark).
- New item `music_box` in `backstage`. It can only be found when `lights = on`; in the dark taking it is rejected with an explanation.
- The `singer` choices on the stage now depend on earlier play. A choice whose conditions are not met is hidden:
  - `answer`: always offered. Ends the game, **lost** (`encore`).
  - `silent`: only when the lights are **not** on.
  - `rush` (sprint for the stair): only when `lights = on`. Ends the game, **lost** (`caught`).
  - `offer` (wind the music box): only when holding the `music_box`. Ends the game, **survived** (`lullaby`, the best ending).
- Existing way out stays: lights not on + mask + `silent` → roof → `escape`, **survived**.
- Every ending has a `result`: `survived` or `lost`, shown to the player.
- Scene text reacts to the `lights` decision (foyer, backstage, stage).

## Out of scope

Health, timers, combat, random events, more scenes.

## Done when

- `tests/test_consequences.py` is green and no existing test was changed.
- All four endings can be reached in the running app, and the lights decision survives a restart of the app.
- The work is on a branch called `more-consequences` and pushed.
