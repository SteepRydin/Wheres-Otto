# Story — "Where's Otto?"

A windy autumn day in St. Hanshaugen park, Oslo. Benjamin Ernesto Aaron Hajdarpasic is minding his friend's white golden retriever Otto for the weekend. He is flirting with Sofie on a bench when Otto slips away with his teal leash. Benjamin has to use his detective skills to find him before something terrible happens.

Look: pixel art. Dog-paw buttons, a pixelated autumn park with wind-blown orange and yellow leaves, and pixel sprites of Benjamin (dark hair, light stubble, dark green Barbour-style coat with the collar up, jeans, black leather boots), Sofie and Otto.

## Scenes (7)

| id | Scene | Notes |
|----|-------|-------|
| `bench` | The Bench (start) | Decision `sofie`. Exits stay locked until it is made. |
| `pond` | The Pond | Sofie finds paw prints only if she is helping. |
| `kiosk` | The Hot-Dog Kiosk | Item `sausage`. |
| `playground` | The Playground | Item `binoculars` (a child's toy pair). |
| `hill` | The Top of the Hill | Decision `scan` (needs the binoculars) shows Otto on the tram tracks and unlocks `tramstreet`. |
| `carstreet` | The Busy Road | Safe dead end with a hint from a delivery driver. |
| `tramstreet` | The Tram Tracks | Decision `rescue`, then `finish`. |

## Items (reusable, never consumed)

- `sausage`: lets Benjamin lure Otto calmly.
- `binoculars`: lets Benjamin spot Otto from the hill.

## Decisions (each once, remembered)

- `sofie`: `help` or `flirt`.
- `scan`: `tram` (only with the binoculars).
- `rescue`: `treat` (only with the sausage), `grab`, or `shout`.
- `finish` (after a calm rescue): `thank` (only if she helped), `apologize` (only if he kept flirting) or `brag`.

## Endings

| id | Result | How |
|----|--------|-----|
| `love` | won (best) | help, scan, treat, thank: Sofie writes her number on his hand. |
| `nonumber` | won | Otto is safe but Benjamin brags or apologizes: she leaves without her number. |
| `tram` | lost | `grab`: Otto bolts along the tracks and is hit by a tram. |
| `car` | lost | `shout`: Otto bolts into the road and is hit by a car. |
