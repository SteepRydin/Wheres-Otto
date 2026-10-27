# Web version — one HTML file anyone can play

## Why

As someone with a link, I want to play Where's Otto? in my browser, with nothing to install and no server, so that anyone can try it and come back to their saved game.

## What

A single self-contained file, `docs/index.html`, built from the sources in `web/` by `build_web.py`.

- The rules from `logic.py` are ported to JavaScript (`web/engine.js`). The story data is exactly `story.py`, exported to `web/story.json` and embedded, so the two versions can never drift apart.
- The game is saved in the browser (`localStorage`) after every accepted action, instead of SQLite. Rejected actions save nothing. If the browser blocks storage the game still plays, it just cannot resume.
- The pixel art is the same art as the Streamlit version: the park background, the scene pictures, the paw buttons and the blowing leaves.
- Works on a phone, with keyboard only, and respects "reduce motion".
- No server, no build step for the player, no tracking. The only outside request is the pixel fonts from Google Fonts, with a monospace fallback.

## Tests (`tests/test_web.py`)

- The embedded story data is exactly the current `story.py`, and the committed page is exactly what `build_web.py` produces.
- The page is self-contained (no external scripts).
- The JavaScript engine behaves exactly like `logic.py`: hundreds of random action sequences give identical results, messages, saved state, decisions and screens, and all four endings are reached.
- The saved game survives "restarting" (a new engine on the same storage) and bad saved data is ignored.
- The scene pictures drawn in JavaScript match the Python pictures pixel for pixel, for every scene and decision.

## Out of scope

Sound, accounts, sharing scores, a story editor, changing the story or the rules.

## Done when

- `uv run pytest` is green.
- I play all four endings in the browser from `docs/index.html`, reload the page mid-game and resume.
- The work is on a branch called `web-version` and pushed.
