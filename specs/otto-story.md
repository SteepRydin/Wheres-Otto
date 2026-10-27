# Where's Otto? — new story and pixel-art look

Replaces the story content of Last Curtain (still in git history on branch `more-consequences`). The engine behaviour required by `docs/product-brief.md` is unchanged: every requirement PT01–PT05, R1–R4 and scenario A1–A6 is tested again, against the new content. The old tests named the old scenes and items, so they are replaced by `tests/test_otto.py`.

## Why

As a player, I want to play Benjamin Ernesto Aaron Hajdarpasic, minding his friend's golden retriever Otto on a windy autumn day in St. Hanshaugen, Oslo, who flirts with Sofie while Otto sneaks off, so that I can track Otto down with detective work, and my choices decide whether Otto is safe and whether Sofie falls for him.

## What

Seven scenes: `bench` (start), `pond`, `kiosk`, `playground`, `hill`, `carstreet` (dead end), `tramstreet`.
Two reusable items: `sausage` (kiosk), `binoculars` (playground).

Decisions (each once, remembered):

- `sofie` at the bench: `help` (tell her and ask her to help) or `flirt` (keep flirting). The bench exits stay locked until it is made. Her help gives a clue at the pond; her mood decides the end.
- `scan` on the hill, only with the binoculars: reveals Otto on the tram tracks and unlocks the way to `tramstreet`.
- `rescue` at `tramstreet`: `treat` (needs the sausage), `grab` or `shout`.
- `finish` once Otto is safe: `thank` (only if `sofie = help`), `apologize` (only if `sofie = flirt`) or `brag`.

Endings, each with a `result` of `won` or `lost`:

- `love` (won, best): help, rescue calmly, thank her. Sofie falls for Benjamin.
- `nonumber` (won): Otto is safe, but brag or apologize, and Sofie leaves without giving her number.
- `tram` (lost): `grab`, Otto bolts along the tracks and is hit by a tram.
- `car` (lost): `shout`, Otto bolts into the road and is hit by a car.

Look: pixel art. Buttons are pixel dog paws. The background is a pixelated autumn park with orange and yellow leaves blown by the wind. Benjamin, Sofie and Otto (white golden retriever with a teal leash, running away) are pixel sprites that change with the story.

## Out of scope

Story editor, extra mysteries, sound, a timer, real map data.

## Done when

- `tests/test_otto.py` is green.
- I play all four endings in the running app, and a mid-game restart of the server resumes correctly.
- The work is on a branch called `otto-story` and pushed.
