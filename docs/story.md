# Story — "Last Curtain" (working title)

Horror, ~10 minutes. Set in the Oslo Opera House (Operahuset) in Bjørvika, with the Barcode skyline glowing across the water.

You are a night cleaner. After the final performance of the season the doors lock themselves and the lights in the Barcode towers outside go out one by one. Something is still singing on the stage.

## Scenes (5)

| id | Scene | Notes |
|----|-------|-------|
| `foyer` | Main Foyer — start | Glass wall facing the fjord, the oak "Wave Wall". Exits: box office, backstage (locked), roof terrace (later). |
| `box_office` | Box Office | Drawer holds the **stage door key**. |
| `backstage` | Backstage corridor — locked | Needs the stage door key. Leads to the stage (later). |
| `stage` | Main stage (later feature) | The singer. Remembered decision: answer her or stay silent. |
| `roof` | The white marble roof (later feature) | Escape route towards the Barcode towers. |

## Items (2, reusable, never consumed)

- `stage_door_key` — in the box office drawer. Unlocks `backstage`.
- `music_box` — (later feature) backstage. Calms or angers the singer depending on the decision.

## Endings (2, later feature)

- **Escape:** the player wears the `porcelain_mask`, kept the lights off and stayed silent on stage, so the singer lets them reach the roof.
- **Encore:** the player answered her; she takes the final bow with them.

(The final design, with four endings, is described under "Consequences" below.)

## First feature (this task)

Only `foyer`, `box_office`, `backstage` and `stage_door_key`. The rest comes in later features.

## Consequences (more-consequences branch)

Two remembered decisions steer the night:

- **Lights** (foyer, once): `on` or `off`.
  - `on` lets you find the **tin music box** backstage, but the singer is then watching: standing still is no longer possible.
  - `off` keeps you hidden, but the music box is out of reach in the dark.
- **The singer** (stage, once). Which options appear depends on the lights and your items:
  - Answer her → **Encore** (lost).
  - Say nothing (lights not on) + porcelain mask → climb to the roof → **The Last Curtain** (survived).
  - Sprint for the stair (lights on) → **Caught in the Light** (lost).
  - Wind the music box (holding it) → **The Last Aria** (survived, best ending).

Four endings: two survived, two lost.
